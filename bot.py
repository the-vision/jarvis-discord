import settings
import random
import os
import discord
import requests
import config
from discord.ext import commands
from modules import xkcd
from os import system
from weather import Weather, Unit
from datetime import datetime

import json
from random import choice
import modules
from templates.quick_replies import add_quick_reply
from templates.text import TextTemplate

TOKEN = os.environ.get('TOKEN', config.TOKEN)
OPEN_WEATHER_MAP_TOKEN = os.environ.get('OPEN_WEATHER_MAP_TOKEN', config.OPEN_WEATHER_MAP_TOKEN)
TIMEZONEDB_TOKEN = os.environ.get('TIMEZONEDB_TOKEN', config.TIMEZONEDB_TOKEN)
MAPQUEST_CONSUMER_KEY = os.environ.get('MAPQUEST_CONSUMER_KEY', config.MAPQUEST_CONSUMER_KEY)
JOKES_SOURCE_FILE = 'data/jokes.json'
FACTS_SOURCE_FILE = 'data/facts.json'
QUOTES_SOURCE_FILE = 'data/quotes.json'
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
@bot.command()
async def roll(ctx):
    client = ctx.channel
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
    await client.send(file=discord.File(result))
    
#Called when $ping_google is typed. Checks google's status(up/down)    
@bot.command()
async def ping_google(ctx):
    result = system("ping www.google.com")
    if (result == 0):
     str = "Google up and running"
    else:
     str = "There might be some problem"
    await ctx.send(str)
    
#Called when $weather CITYNAME is typed. Gets the weather from OpenWeatherMap API.
@bot.command(pass_context=True)
async def weather(ctx,*,message):
    url = 'http://api.openweathermap.org/data/2.5/weather?appid=' + OPEN_WEATHER_MAP_TOKEN + '&q=' + message
    r = requests.get(url).json()
    Weather = r['weather'][0]['description']
    FahreneitTemperature = int(r['main']['temp'])
    CelsiusTemperature = int(5/9 * (int(FahreneitTemperature) - 32))
    name = r['name']
    country = r['sys']['country']
    await ctx.send("Location: " + name + "," + country + "\n"
                   "Weather: " + Weather + "\n"
                   "Temperature: " + str(CelsiusTemperature) + "°C / " + str(FahreneitTemperature) + "°F\n"
                   "-Info provided by OpenWeatherMap")

#Called when $time_in CITYNAME is typed. Gets city's longitude and latitude from MapQuest API and uses
#them to get the weather from OpenWeatherMap API.                   
@bot.command(pass_context=True)
async def time_in(ctx,*, message):
        r = requests.get(
            'http://open.mapquestapi.com/nominatim/v1/search.php?key=' + MAPQUEST_CONSUMER_KEY + '&format=json&q=' + message+ '&limit=1')
        location_data = r.json()
        r = requests.get('http://api.timezonedb.com/?lat=' + location_data[0]['lat'] + '&lng=' + location_data[0][
            'lon'] + '&format=json&key=' + TIMEZONEDB_TOKEN)
        time_data = r.json()
        time = datetime.utcfromtimestamp(time_data['timestamp']).strftime('%a %b %d %Y %H:%M:%S')
        await ctx.send('Location: ' + location_data[0]['display_name'] + '\nTime: ' + time + ' ' + time_data[
                       'abbreviation'])
                    

#Called when $joke is typed. Opens the jokes.json file and chooses one joke.                    
@bot.command()
async def joke(ctx):
    output = {}
    with open(JOKES_SOURCE_FILE) as jokes_file:
        jokes = json.load(jokes_file)
        jokes_list = jokes['jokes']
        message = TextTemplate(choice(jokes_list)).get_message()
        output['input'] = input
        output['output'] = message
        output['success'] = True     
    await ctx.send(output['output']['text'])

#Called when $fact is typed. Opens the facts.json file and chooses one fact.    
@bot.command()
async def fact(ctx):
    output = {}
    with open(FACTS_SOURCE_FILE) as facts_file:
            facts = json.load(facts_file)
            facts_list = facts['facts']
            message = TextTemplate(choice(facts_list)).get_message()
            output['input'] = input
            output['output'] = message
            output['success'] = True 
    await ctx.send(output['output']['text']) 
    
#Called when $quote is typed. Opens the quotes.json file and chooses one quote.
@bot.command()
async def quote(ctx):
    output = {}
    with open(QUOTES_SOURCE_FILE) as quotes_file:
            facts = json.load(quotes_file)
            facts_list = facts['facts']
            message = TextTemplate(choice(facts_list)).get_message()
            output['input'] = input
            output['output'] = message
            output['success'] = True 
    await ctx.send(output['output']['text'])        
    
#Called when $flip_a_coin is typed. Images are on the 'images' folder.    
@bot.command()
async def flip_a_coin(ctx):
    client = ctx.channel
    num = random.randint(1,2)
    switcher = {
        1: 'images/coin_head.png',
        2: 'images/coin_tails.png'
    }
    result = switcher.get(num,"Invalid")
    await client.send(file=discord.File(result))
    
bot.run(TOKEN)
