import settings
import os
from modules import news, image, youtube_music as music

import discord
from discord.ext import commands
from modules import xkcd

TOKEN = os.getenv('DISCORD_BOT_API_TOKEN')
bot = commands.Bot(command_prefix='$', description='Just A Rather Very Intelligent System, now on Discord!')
musicPlayer = music.MusicPlayer()


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


@bot.command(name='connect',
             description='Connects to this voiceChannel',
             brief='Connects to this voice channel')
async def yt(ctx):
    channel = bot.get_channel(ctx.message.author.voice.channel.id)
    await musicPlayer.connect(channel)


@bot.command(name='disconnect',
             description='Disconnects from this voiceChannel',
             brief='Disconnects from this voice channel')
async def yt(ctx):
    await musicPlayer.disconnect()


@bot.command(name='add_song',
             description='Download an mp3 song youtube and adding to a queue ',
             brief='Plays a song')
async def yt(ctx, url):
    await musicPlayer.add_song(url, ctx)


@bot.command(name='pause',
             description='Pause a song that is already being played ',
             brief='Pause the song')
async def yt(ctx):
    await musicPlayer.pause_song(ctx)


@bot.command(name='resume',
             description='Resume a song that has been stopped ',
             brief='Resume the song')
async def yt(ctx):
    await musicPlayer.resume_song(ctx)


@bot.command(name='stop',
             description='Stop playing songs ',
             brief='Stop the songs')
async def yt(ctx):
    await musicPlayer.stop(ctx)


@bot.command(name='next',
             description='Stop playing songs ',
             brief='Stop the songs')
async def yt(ctx):
    await musicPlayer.next(ctx)


@bot.command(name='play',
             description='Starts playing songs from the queue if already being added',
             brief='Starts playing songs')
async def yt(ctx):
    channel = bot.get_channel(ctx.message.author.voice.channel.id)
    await musicPlayer.play(ctx, channel)


bot.run(TOKEN)
