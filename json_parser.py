import json


def load_json(path):
    with open(path,"r") as file:
        return json.load(file)

def save_json(json_f,path):
    with open(path,"w") as file:
        json.dump(json_f,file)