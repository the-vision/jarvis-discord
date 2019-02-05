import json
from random import choice
from templates.text import TextTemplate

FACTS_SOURCE_FILE = 'data/facts.json'

def process():
    output = {}
    with open(FACTS_SOURCE_FILE) as facts_file:
        facts = json.load(facts_file)
        facts_list = facts['facts']
        message = TextTemplate(choice(facts_list)).get_message()
        output['input'] = input
        output['output'] = message
        output['success'] = True 
    return output['output']        