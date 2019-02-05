import random
import discord
import requests

def process():
    num = random.randint(1,6)
    switcher = {
        1: 'images/1.png',
        2: 'images/2.png',
        3: 'images/3.png',
        4: 'images/4.png',
        5: 'images/5.png',
        6: 'images/6.png'
    }
    result = switcher.get(num,"Invalid")
    return result