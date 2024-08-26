import datetime
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


if __name__ == "__main__":
    chatLoop(functions)

