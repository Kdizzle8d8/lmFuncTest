import json
import os
import textwrap
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
            content_lines = response.choices[0].message.content.split('\n')
            for content_line in content_lines:
                wrapped_lines = textwrap.wrap(content_line, width=72)
                for line in wrapped_lines:
                    print(f"\033[92m│ {line:<72} │\033[0m")
            print("\033[92m└" + "─" * 74 + "┘\033[0m")