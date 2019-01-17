import discord

import asyncio
import aiohttp
import os


async def process(search_arg):

        '''Searches for a image related to the search arg '''
        url = 'https://www.googleapis.com/customsearch/v1'
        params = {
                'key': os.getenv('GOOGLE_API_KEY'), 
                'cx': os.getenv('GOOGLE_CUSTOM_SEARCH_ENGINE_ID'),
                'searchType': 'image', 'q': search_arg, "num": 1, 'safe': 'active'}
        async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as resp:
                        if resp.status == 403:
                                return 'Limit exceeded'
                        data = await resp.json()
                        image_url = data['items'][0]['link']
                        # TODO: Check if response is empty?
                        return discord.Embed(
                                title=f'{search_arg}'.capitalize(),
                                image=image_url).set_image(url=image_url)
