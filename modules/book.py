import os
from xml.etree import ElementTree
import config
import requests
import requests_cache
from templates.text import TextTemplate
from html2text import html2text

import config

GOODREADS_ACCESS_TOKEN = os.environ.get('GOODREADS_ACCESS_TOKEN', config.GOODREADS_ACCESS_TOKEN)


def process(message):
    output = {}
    try:
        with requests_cache.enabled('book_cache', backend='sqlite', expire_after=86400):
            response = requests.get('https://www.goodreads.com/book/title.xml?key=' +
                                    GOODREADS_ACCESS_TOKEN + '&title=' + message)
            data = ElementTree.fromstring(response.content)
        book_node = data.find('book')
        author = book_node.find('authors').find('author').find('name').text
        title = book_node.find('title').text
        description = html2text(book_node.find('description').text)
        average_rating = book_node.find('average_rating').text
        link = book_node.find('link').text
        goodreads_attribution = '- Powered by Goodreads'

        output['output'] = TextTemplate('Title: ' + title + '\nAuthor: ' + author + '\nDescription: ' + description +
                                        '\nAverage Rating: ' + average_rating + ' / 5' + '\n'
                                        + goodreads_attribution).get_message()
        output['success'] = True
    except Except:
        error_message = 'I couldn\'t find any book matching your query.'
        error_message += '\nPlease ask me something else, like:'
        error_message += '\n  - book timeline'
        error_message += '\n  - harry potter book plot'
        error_message += '\n  - little women book rating'
        output['error_msg'] = TextTemplate(error_message).get_message()
        output['success'] = False
    return output
