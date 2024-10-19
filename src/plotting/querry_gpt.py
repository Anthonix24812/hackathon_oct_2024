from dotenv import load_dotenv, find_dotenv

from openai import OpenAI
load_dotenv()
client = OpenAI()


def run_querry(user_querry, json_file):
    global client
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
        {"role": "system", "content": "You are given a JSON file containing sustainability metrics extracted from company reports. Your task is to create Python code (and only Python code) that uses the matplotlib library to generate suitable graphs, such as bar charts, pie charts, or other appropriate visualizations. The code should be able to handle the creation of one or multiple graphs within a single PNG file. \n Important requirements: \n The generated Python code should save the plot(s) in a file called **result.png**. The output must be returned strictly as a Python code string. Ensure the graphs accurately represent the data in the JSON file and that they are visually clear." + 
        "When analysing the JSON file, consider the following context, that the user wants to be considered. This will be the context question for creating the plots:" + user_querry},
        {
            "role": "user",
            "content": f"{json_file}"
            # "content": "come up with some data, the json file will come later"
        }
    ]
    )   
    message_content = completion.choices[0].message.content

    cleaned_message = message_content.strip("```python").strip("```")

    return cleaned_message


def querry_gpt(user_querry, data) -> str:
    return run_querry(user_querry, json_file)


def turn_json_into_str(json_file):
    pass

if __name__ == '__main__':
    run_querry("What is the co2 development of apple in the last 5 years?","")

