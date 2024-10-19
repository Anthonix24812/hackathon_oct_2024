import os
import openai 
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from openai import OpenAI
os.environ["TOKENIZERS_PARALLELISM"] = "false"


# Load environment variables
load_dotenv()

DB_FAISS_PATH = 'vectorstore/db_faiss'
client = OpenAI()

# Custom prompt template
custom_prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

def set_custom_prompt():
    """
    Prompt template for QA retrieval for each vectorstore.
    """
    return custom_prompt_template

# This is how you use the new OpenAI client
def load_llm_openai(query):
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant. Solve this:"},
        {
            "role": "user",
            "content": query
        }
    ]
)

    print(completion.choices[0].message)


# QA Bot Function
def qa_bot():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)

    qa_prompt = set_custom_prompt()

    # Function to handle query and retrieval
    def query_openai_with_retrieval(query):
        # Perform retrieval from FAISS vector store
        retrieved_docs = db.similarity_search(query, k=2)
        context = " ".join([doc.page_content for doc in retrieved_docs])
        # Print the context to check if it's relevant
        print("Context retrieved:\n", context)

        # Construct the final query with context
        final_query = qa_prompt.format(context=context, question=query)
        

        # Send query to OpenAI
        answer = load_llm_openai(final_query)

        return {"result": answer, "source_documents": retrieved_docs}
    
    return query_openai_with_retrieval

# Function to handle final result
def final_result(query):
    qa_result = qa_bot()
    response = qa_result(query)
    return response

# Main function to run the bot in terminal
def main():
    print("RAG Bot is running. Type your query below.")
    while True:
        user_query = input("\nYour question: ")
        if user_query.lower() == 'exit':
            break
        result = final_result(user_query)
        print("\nAnswer:", result["result"])
        sources = result["source_documents"]
        if sources:
            print("\nSources:")
            for doc in sources:
                print(f" - {doc.metadata.get('source', 'Unknown source')}")

if __name__ == "__main__":
    main()