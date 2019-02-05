import settings
import random
import os
import discord
import requests
import config
from discord.ext import commands
from modules import xkcd
from modules import roll
from modules import ping_google
from modules import weather
from modules import time_in
from modules import joke
from modules import fact
from modules import quote
from modules import flip_a_coin
from os import system
from weather import Weather, Unit

import json
from random import choice
import modules
from templates.quick_replies import add_quick_reply
from templates.text import TextTemplate

TOKEN = os.environ.get('TOKEN', config.TOKEN)
bot = commands.Bot(command_prefix='$', description='Just A Rather Very Intelligent System, now on Discord!')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def greet(ctx):
    await ctx.send(":smiley: :wave: Hello, there!")

@bot.command(name='xkcd',
        description='Retrieves a random xkcd comic through external API call',
        brief='Retrieves a random xkcd comic')
async def get_xkcd(ctx):
    try:
        embed=xkcd.process()
        await ctx.send(embed=embed)

    except Exception as e:
        print(e)
        await ctx.send("Sorry, something went wrong.")

#Called when $roll is typed. Num gets the value of a random integer from 1 to 6
#and returns the according image. Images are on the 'images' folder.
@bot.command(name='roll')
async def get_roll(ctx):
    try:
        result = roll.process()
        await ctx.channel.send(file=discord.File(result))
    except Exception as e:
        print(e)
        await ctx.send("Sorry, something went wrong.")
    
#Called when $ping_google is typed. Checks google's status(up/down)    
@bot.command(name = 'ping_google')
async def get_ping_google(ctx):
    try:
        str = ping_google.process()
        await ctx.send(str)
    except Exception as e:
        print(e)
        await ctx.send("Sorry, something went wrong.")
    
#Called when $weather CITYNAME is typed. Gets the weather from OpenWeatherMap API.
@bot.command(pass_context=True, name = 'weather')
async def get_weather(ctx,*,message):
    try:
        output = weather.process(message)
        await ctx.send(output['text'])
    except Exception as e:
        print(e)
        await ctx.send("Sorry, something went wrong.")

#Called when $time_in CITYNAME is typed. Gets city's longitude and latitude from MapQuest API and uses
#them to get the weather from OpenWeatherMap API.                   
@bot.command(pass_context=True, name = 'time_in')
async def get_time_in(ctx,*, message):
        try:
            output = time_in.process(message)
            await ctx.send(output['text'])
        except Exception as e:
            print(e)
            await ctx.send("Sorry, something went wrong.")
                    

#Called when $joke is typed. Opens the jokes.json file and chooses one joke.                    
@bot.command(name = 'joke')
async def get_joke(ctx): 
    output = joke.process()        
    await ctx.send(output['text'])

#Called when $fact is typed. Opens the facts.json file and chooses one fact.    
@bot.command(name = 'fact')
async def get_fact(ctx):
    output = fact.process()        
    await ctx.send(output['text'])
    
#Called when $quote is typed. Opens the quotes.json file and chooses one quote.
@bot.command(name = 'quote')
async def get_quote(ctx):
    output = quote.process()        
    await ctx.send(output['text'])
    
#Called when $flip_a_coin is typed. Images are on the 'images' folder.    
@bot.command(name = 'flip_a_coin')
async def get_flip_a_coin(ctx):
    result = flip_a_coin.process()
    await ctx.channel.send(file=discord.File(result))
    
bot.run(TOKEN)
