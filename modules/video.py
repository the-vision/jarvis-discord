import os

import requests
import requests_cache
import urllib.parse
import urllib.request
import re
import config
from templates.text import TextTemplate

YOUTUBE_DATA_API_KEY = os.environ.get('YOUTUBE_DATA_API_KEY', config.YOUTUBE_DATA_API_KEY)


def process(message):
    output = {}
    try:
        query = urllib.parse.urlencode({'search_query': message})
        content = urllib.request.urlopen('http://www.youtube.com/results?' + query)
        search = re.findall('href=\"\\/watch\\?v=(.{11})', content.read().decode())
        output['output'] = 'http://www.youtube.com/watch?v=' + search[0]
        output['success'] = True
    except Except:
        error_message = 'I couldn\'t find any videos matching your query.'
        error_message += '\nPlease ask me something else, like:'
        error_message += '\n  - sia videos'
        error_message += '\n  - videos by eminem'
        error_message += '\n  - video coldplay'
        output['error_msg'] = TextTemplate(error_message).get_message()
        output['success'] = False
    return output
