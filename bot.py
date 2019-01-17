import os

import discord
import settings
from discord.ext import commands
from modules import xkcd
from modules import image

TOKEN = os.getenv('DISCORD_BOT_API_TOKEN')
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


@bot.command(
    name='image',
    description='Searches an image from istockphoto',
    brief='Search an image')
async def search_image(ctx, search_arg):
    try:
        embed = await image.process(search_arg)
        await ctx.send(embed=embed)

    except Exception as e:
        print(e)
        await ctx.send("Sorry, something went wrong.")


bot.run(TOKEN)
