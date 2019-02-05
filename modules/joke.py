import json
from random import choice
from templates.text import TextTemplate

JOKES_SOURCE_FILE = 'data/jokes.json'

def process():
    output = {}
    with open(JOKES_SOURCE_FILE) as jokes_file:
        jokes = json.load(jokes_file)
        jokes_list = jokes['jokes']
        message = TextTemplate(choice(jokes_list)).get_message()
        output['input'] = input
        output['output'] = message
        output['success'] = True 
    return output['output']        