import random
import discord

tail_image_url = "https://urlzs.com/UXXyP"
dice_shows_1_url = "https://urlzs.com/8zuPx"
dice_shows_2_url = "https://urlzs.com/mtafi"
dice_shows_3_url = "https://urlzs.com/q3zXc"
dice_shows_4_url = "https://urlzs.com/Mf4ps"
dice_shows_5_url = "https://urlzs.com/Q5iKb"
dice_shows_6_url = "https://urlzs.com/YLwh2"


def easyDiscordEmbed(result, image_url):
    embed = discord.Embed(title=result, type="rich", image=image_url).set_image(
        url=image_url
    )
    return embed


def rollDice():
    dieHeads = [random.randint(1, 6) for r in range(1)]
    for object in dieHeads:
        if object == 1:
            embeded = easyDiscordEmbed(object, dice_shows_1_url)
        elif object == 2:
            embeded = easyDiscordEmbed(object, dice_shows_2_url)
        elif object == 3:
            embeded = easyDiscordEmbed(object, dice_shows_3_url)
        elif object == 4:
            embeded = easyDiscordEmbed(object, dice_shows_4_url)
        elif object == 5:
            embeded = easyDiscordEmbed(object, dice_shows_5_url)
        elif object == 6:
            embeded = easyDiscordEmbed(object, dice_shows_6_url)
    return embeded
