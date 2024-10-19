from dotenv import load_dotenv, find_dotenv

from openai import OpenAI
load_dotenv()
client = OpenAI()




def run_querry(final_promt):
    global client
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"{final_promt}"
        }
    ]
    )   
    print(completion.choices[0].message)



def querry_gpt(user_querry, data, id):
    return ""

run_querry("Imagine you've gotten a .json file including sustainablity data. Now create the code that creates a matplotlib grafic to visualize this data. Make sure to only"+
            "include the python code as a string and nothing else. Within the python code make sure to save the created plot in file called result.png")

