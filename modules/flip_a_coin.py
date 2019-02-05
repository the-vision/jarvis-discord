import random
import discord
import requests

def process():
    num = random.randint(1,2)
    switcher = {
        1: 'images/coin_head.png',
        2: 'images/coin_tails.png'
    }
    result = switcher.get(num,"Invalid")
    return result