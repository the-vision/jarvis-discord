import random
import discord

head_image_url = "https://urlzs.com/Wi46z"
tail_image_url = "https://urlzs.com/UXXyP"


def cointoss(number):
    flips = [random.randint(0, 1) for r in range(1)]
    results = []
    for object in flips:
        if object == 0:
            results.append("Heads")
        elif object == 1:
            results.append("Tails")

    return results


def coinToss():
    result = cointoss(1)[0]

    if result == "Heads":

        rembed = discord.Embed(
            title=result, type="rich", image=head_image_url
        ).set_image(url=head_image_url)
    else:
        rembed = discord.Embed(
            title=result, type="rich", image=tail_image_url
        ).set_image(url=tail_image_url)

    return rembed
