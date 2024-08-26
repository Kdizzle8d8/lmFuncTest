from datetime import datetime

import requests
from aifunc import aifunc, functions
from chat import chatLoop 
from index import *

@aifunc
def add(a:int,b:int):
    """
    Add two numbers
    a: first number
    b: second number
    """
    return a+b

@aifunc
def get_today():
    """
    Returns the current date
    """
    return datetime.now().strftime("%Y-%m-%d")

# Example of how you can call and api. This runs on my local server
@aifunc
def orange_or_blue(month:int,day:int):
    """
    Returns whether the day is orange or blue according to the user's school schedule
    month: the month to check
    day: the day to check
    """
    result = requests.get(f"http://100.100.141.53:8080/date/{month}/{day}")
    return result.text

if __name__ == "__main__":
    chatLoop(functions)

