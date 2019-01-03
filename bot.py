import settings
import os
import discord
import requests

from discord.ext import commands
from random import randint

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
        r = requests.get('http://xkcd.com/info.0.json')
        data = r.json()

            # Get a random comic between the first and the latest one
        r = requests.get('http://xkcd.com/%d/info.0.json' % randint(1, data['num']))
        data = r.json()

        title = data['title']
        item_url = 'http://xkcd.com/' + str(data['num']) + '/'
        explanation_url = 'http://explainxkcd.com/' + str(data['num']) + '/'
        image_url = data['img'].replace('\\', '')
        subtitle = data['alt']

        embed = discord.Embed(title=title,
                type='rich',
                description="{0}\n{1}".format(subtitle, explanation_url),
                url=item_url,
                image=image_url).set_image(url=image_url)

        await ctx.send(embed=embed)

    except Exception as e:
        print(e)
        await ctx.send("Sorry, something went wrong.")


bot.run(TOKEN)
