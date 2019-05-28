import settings
import os
from modules import news, image

import discord
from discord.ext import commands
from modules import xkcd, flip_a_coin, roll_a_dice

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
        embed = xkcd.process()
        await ctx.send(embed=embed)

    except Exception as e:
        print(e)
        await ctx.send("Sorry, something went wrong.")


@bot.command(name='news',
             description='Retrieves a random top headline from NewsAPI',
             brief='Retrieves a top headline')
async def cmd_news(ctx):
    await ctx.send(embed=news.top_headlines())


@bot.command(
    name='image',
    description='Searches an image from google search engine',
    brief='Search an image')
async def search_image(ctx, search_arg):
    try:
        embed = await image.process(search_arg)
        await ctx.send(embed=embed)

    except Exception as e:
        print(e)
        await ctx.send("Sorry, something went wrong.")


@bot.command(
    name="flip_a_coin",
    description="Flip a coin game",
    brief="flip a coin and send head to tails",
)
async def flip_coin(ctx):
    try:
        embed = flip_a_coin.coinToss()
        await ctx.send(embed=embed)

    except Exception as e:
        print(e)
        await ctx.send("Sorry, something went wrong.")


@bot.command(
    name="roll_a_dice",
    description="Roll a dice game",
    brief="Roll a dice and send result of the head",
)
async def roll_dice(ctx):
    try:
        embed = roll_a_dice.rollDice()
        await ctx.send(embed=embed)

    except Exception as e:
        print(e)
        await ctx.send("Sorry, something went wrong.")

bot.run(TOKEN)
