import json
from random import choice
from templates.text import TextTemplate

quotes_SOURCE_FILE = 'data/quotes.json'

def process():
    output = {}
    with open(quotes_SOURCE_FILE) as quotes_file:
        quotes = json.load(quotes_file)
        quotes_list = quotes['quotes']
        message = TextTemplate(choice(quotes_list)).get_message()
        output['input'] = input
        output['output'] = message
        output['success'] = True 
    return output['output']        