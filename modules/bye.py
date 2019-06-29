import json
from random import choice
from templates.text import TextTemplate

BYE_SOURCE_FILE = 'data/byes.json'


def process(userName):
    output = {}
    with open(BYE_SOURCE_FILE) as bye_file:
        byes = json.load(bye_file)
        byes_list = byes['byes']
        message = TextTemplate(choice(byes_list)).get_message()
        temp = str(message).replace('{', '').replace('}', '')
        temp = temp.replace('\'text\':', '').replace('\'', '')
        temp = temp.replace('\\n', '\n').replace('"', '')
        temp = temp.replace('sir', userName)
        output['output'] = temp
        output['success'] = True
    return output['output']
