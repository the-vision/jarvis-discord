import pyshorteners
from pyshorteners import Shortener
import discord


def urlShortner(search_args):
    shortener = Shortener('Tinyurl', timeout=9000)
    short_url = shortener.short('http://'+search_args)
    return (discord.Embed(
            title=short_url, type='rich'))
