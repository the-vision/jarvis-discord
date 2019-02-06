from os import system
from urllib.parse import urlparse

import requests
import discord
#from templates.generic import *
from templates.text import TextTemplate

def process(message):
        output = {}
        url = message
        if not urlparse(url).scheme:
            url = "https://" + url
        hostname = urlparse(url).hostname
        if hostname is None:
            raise Exception("Please enter a valid hostname to check availability.")
        r = requests.get('https://isitup.org/' + hostname + '.json')
        data = r.json()
    
        status = data['status_code']
        if status == 1:
            text = hostname + ' is up.'
            image_url = 'http://fa2png.io/media/icons/font-awesome/4-7-0/check-circle/256/0/27ae60_none.png'
        elif status == 2:
            text = hostname + ' seems to be down!'
            image_url = 'http://fa2png.io/media/icons/font-awesome/4-7-0/times-circle/256/0/c0392b_none.png'
        elif status == 3:
            text = 'Please enter a valid domain to check availability.'
            image_url = 'http://fa2png.io/media/icons/font-awesome/4-7-0/exclamation-circle/256/0/f1c40f_none.png'
        else:
            raise Exception("Something unexpected happened!")
            
        embed = discord.Embed(title=text,
            type='rich',
            image=image_url).set_image(url=image_url)            
        return embed