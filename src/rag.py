import os
import requests
import PyPDF2
import pandas as pd
from dotenv import load_dotenv
import json
import os
import openai
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from openai import OpenAI
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document

# load openai key
if not load_dotenv():
    raise Exception('Error loading .env file. Make sure to place a valid OPEN_AI_KEY in the .env file.')

REPORTS_SAVE_PATH = 'data/sample_reports'

DB_FAISS_PATH = 'src/Extraction/vectorstore/db_faiss'

# See https://openai.com/api/pricing/
MODEL = "gpt-4o-mini"


def qa_result(query):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    
    # Increase the number of retrieved documents
    retrieved_docs = db.similarity_search(query, k=5)
    
    # Concatenate the content with separators
    context = "\n---\n".join([doc.page_content for doc in retrieved_docs])
    
    # Optionally, limit the context length if needed
    max_length = 3000  # You can adjust this based on token limits
    context = context[:max_length]
    
    print("Context retrieved:\n", context)
    
    return context

#context = build_context_from_docs(dummy_docs)


def rag_service(human_input: str) -> str:


# Load the LLM
    llm = ChatOpenAI(
    model_name=MODEL,
    temperature=0,
    max_tokens=1000,
    ).bind(response_format={"type": "json_object"})


# Load the LLM-Buzzword-Maker
    llm_B = ChatOpenAI(
    model_name=MODEL,
    temperature=0.1,
    max_tokens=1000,
    )


# Answer with retrieved context
    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. You help to retrieve information from sustainability reports and output it as a json object.",
        ),
        ("human", """
        I have the following question: {question}\n\n
        Retrieve all relevant information about the question from the following text in triple backticks:\n\n```{context}```\n\n
        The information should be output as a json object. All numeric values should be converted to numbers. One field should containt the unit of the value.
        """),
    ]
    )

    queryBuzzword = ""+""

    prompt_b = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. You help to generate a simplified list of potential buzzword that a seperate service will look for in a vector database. optimize the query for that.",
        ),
        ("human", """
        I have the following question: {question}\n\n
        You help to generate a simplified list based on the question above. Create a list of potential buzzwords that a seperate service will use for search in a vector database.
         ONLY RETURN THE ACTUAL BUZZWORDS,word after word, seperated by space
        """),
    ]
    )
    chain_b = prompt_b | llm_B
    buzzwordAnswer = chain_b.invoke(
        {
            "question": human_input,
        }
    )
    print(buzzwordAnswer)

    #What are the reported levels of recycled tin in Apple products for 2021 and 2022?
    context = qa_result("What are the reported levels of recycled tin in Apple products for 2021 and 2022?")

    realLifeQuestion = ""
    chain = prompt | llm
    answer = chain.invoke(
        {
            "question": human_input,
            "context": context,
        }
    )
    return answer.content