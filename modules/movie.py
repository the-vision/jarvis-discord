#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from imdbparser import IMDb

import requests
import requests_cache

import config
from templates.text import TextTemplate

TMDB_API_KEY = os.environ.get('TMDB_API_KEY', config.TMDB_API_KEY)


def process(message):
    output = {}
    try:

        with requests_cache.enabled('movie_cache', backend='sqlite',
                                    expire_after=86400):

            r = requests.get('https://api.themoviedb.org/3/search/movie?api_key=' + TMDB_API_KEY
                             + '&query=' + str(message))
            data = r.json()
            assert len(data['results']) > 0
            tmdb_id = str(data['results'][0]['id'])

            # Make another request to the API using the movie's TMDb ID to get the movie's IMDb ID

            r = requests.get('https://api.themoviedb.org/3/movie/'
                             + tmdb_id,
                             params={'api_key': TMDB_API_KEY, 'append_to_response': 'videos'})
            data = r.json()
        ia = IMDb()
        imdb_id = data['imdb_id']
        imdb_movie = ia.get_movie(imdb_id[2:])
        imdb_movie.fetch()

        template = TextTemplate('Title: ' + data['title'] + '\nYear: '
                                + (data['release_date'])[:4]
                                + '\nIMDb Rating: '
                                + str(imdb_movie.__dict__['rating'])
                                + ' / 10' + '\nOverview: '
                                + data['overview'] + '\nIMDb Link',
                                'https://www.imdb.com/title/'
                                + data['imdb_id'] + '/').get_message()
        videos = data['videos']['results']

        output['output'] = TextTemplate('Title: ' + data['title']
                                        + '\nYear: ' + (data['release_date'])[:4]
                                        + '\nIMDb Rating: ' + str(imdb_movie.__dict__['rating'])
                                        + ' / 10' + '\nOverview: ' + data['overview']
                                        + '\nIMDb Link', 'https://www.imdb.com/title/'
                                        + data['imdb_id'] + '/').get_message()
        output['success'] = True
    except Exception:
        error_message = 'I couldn\'t find that movie.'
        error_message += '\nPlease ask me something else, like:'
        error_message += '\n  - batman movie'
        error_message += '\n  - iron man 2 movie plot'
        error_message += '\n  - What is the rating of happyness movie?'
        output['error_msg'] = TextTemplate(error_message).get_message()
        output['success'] = False
    return output
