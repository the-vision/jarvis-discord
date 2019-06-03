import random
import discord

head_image_url = "https://www.thespecialgiftcompany.com/wp-content/uploads/2017/10/tails-head-coin.jpg"
tail_image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQrUfZKS5OsMPCEPPQMfRLY8cNGC5Pr8pysA1hP2gvGC75kKaJuVQ"


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
