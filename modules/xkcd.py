from random import randint
import discord
import requests


def process():
    r = requests.get("http://xkcd.com/info.0.json")
    data = r.json()

    # Get a random comic between the first and the latest one
    r = requests.get("http://xkcd.com/%d/info.0.json" % randint(1, data["num"]))
    data = r.json()

    title = data["title"]
    item_url = "http://xkcd.com/" + str(data["num"]) + "/"
    explanation_url = "http://explainxkcd.com/" + str(data["num"]) + "/"
    image_url = data["img"].replace("\\", "")
    subtitle = data["alt"]

    embed = discord.Embed(
        title=title,
        type="rich",
        description="{0}\n{1}".format(subtitle, explanation_url),
        url=item_url,
        image=image_url,
    ).set_image(url=image_url)

    return embed
