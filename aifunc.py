import inspect
import json

functions=[]
real_functions=[]

def aifunc(function):
    signature = inspect.signature(function)
    properties={}
    required=[]
    tool={
        "name":function.__name__,
        "description":getDescription(function)["main_description"],
        "parameters":{
            "type":"object",
            "properties":properties
        },
        "required":required
    }
    paramDescriptions=getDescription(function)["parameters"]
    for param in signature.parameters.values():
        properties[param.name]={"type":getJsonType(param.annotation),"description":paramDescriptions[param.name]}
        if param.default==inspect.Parameter.empty:
            required.append(param.name)
    functions.append(tool)
    real_functions.append(function)
def getDescription(function)->{"main_description":str,"parameters":{str:str}}:
    docstring = function.__doc__
    if docstring:
        lines = docstring.split("\n")
        main_description = lines[1].strip()
        parameters = {}
        for line in lines[1:]:
            if ":" in line:
                param, desc = line.split(":", 1)
                parameters[param.strip()] = desc.strip()
                
        return {"main_description": main_description, "parameters": parameters}
    return {"main_description": "", "parameters": {}}

def getFunctionAndExecute(name,args):
    args=json.loads(args)
    for function in real_functions:
        if function.__name__==name:
            if(args):
                return function(**args)
            else:
                return function()

def getJsonType(annotation):
    if annotation == int or annotation == float:
        return "number"
    elif annotation == str:
        return "string"
    elif annotation == bool:
        return "boolean"