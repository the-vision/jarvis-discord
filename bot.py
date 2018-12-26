import os

import discord
from discord.ext import commands

TOKEN = os.environ.get('DISCORD_BOT_API_TOKEN')
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

bot.run(TOKEN)
