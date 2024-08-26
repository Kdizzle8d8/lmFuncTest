import json
import os
from dotenv import load_dotenv
from openai import OpenAI

from aifunc import getFunctionAndExecute

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
model = "gpt-4o"
messages=[{"role":"system","content":"You are a helpful assistant"}]
def chatLoop(functions):
    print("type 'quit()' to exit")
    print(messages)
    while True:
        if not(messages[-1]["role"]=="function"):
            print(f"\033[94m┌─[{model}]\033[0m")
            user = input(f"\033[94m└─> \033[0m")
            messages.append({"role": "user", "content": user})
            if user == "quit()":
                break
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            functions=functions,
            function_call="auto"
        )
        if response.choices[0].message.function_call:
            function_call=response.choices[0].message.function_call
            print("Caling function",function_call.name,"...")
            function_reponse=getFunctionAndExecute(function_call.name,function_call.arguments)
            
            messages.append({"role":"function","name":function_call.name,"content":str(function_reponse)})
        else:
            messages.append({"role":"assistant","content":response.choices[0].message.content})
            print("\033[92m┌─Assistant─" + "─" * (74 - 11) + "┐\033[0m")
            print("\033[92m│  " + response.choices[0].message.content.ljust(72) + "│\033[0m")
            print("\033[92m└" + "─" * 74 + "┘\033[0m")
            

        