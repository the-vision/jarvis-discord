#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from imdbparser import IMDb

import requests
import requests_cache

import config
from templates.text import TextTemplate

# from utils.YouTube import YouTubeUtil

# This product uses the TMDb API but is not endorsed or certified by TMDb.

TMDB_API_KEY = os.environ.get('TMDB_API_KEY', config.TMDB_API_KEY)


def process(message):
    output = {}
    try:

        # movie = entities['movie'][0]['value']

        with requests_cache.enabled('movie_cache', backend='sqlite',
                                    expire_after=86400):

            # Make a search request to the API to get the movie's TMDb ID

            r = \
                requests.get('https://api.themoviedb.org/3/search/movie?api_key='
                              + TMDB_API_KEY + '&query=' + str(message))

            # r1 = requests.get('https://api.themoviedb.org/3/search/movie?api_key='+TMDB_API_KEY+'&query=lord+of+the+rings')
                # '&include_adult': False

            data = r.json()
            assert len(data['results']) > 0
            tmdb_id = str(data['results'][0]['id'])

            # Make another request to the API using the movie's TMDb ID to get the movie's IMDb ID

            r = requests.get('https://api.themoviedb.org/3/movie/'
                             + tmdb_id,
                             params={'api_key': TMDB_API_KEY,
                             'append_to_response': 'videos'})
            data = r.json()

        # Fetch movie rating from IMDb

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

        # Append first Trailer URL if one exists
        # for video in videos:
            # if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                # template.add_web_url('YouTube Trailer', YouTubeUtil.get_video_url(video['key']))
                # break

        # output['input'] = input

        output['output'] = TextTemplate('Title: ' + data['title']
                + '\nYear: ' + (data['release_date'])[:4]
                + '\nIMDb Rating: ' + str(imdb_movie.__dict__['rating'
                ]) + ' / 10' + '\nOverview: ' + data['overview']
                + '\nIMDb Link', 'https://www.imdb.com/title/'
                + data['imdb_id'] + '/').get_message()
        output['success'] = True
    except:
        error_message = 'I couldn\'t find that movie.'
        error_message += '\nPlease ask me something else, like:'
        error_message += '\n  - batman movie'
        error_message += '\n  - iron man 2 movie plot'
        error_message += '\n  - What is the rating of happyness movie?'
        output['error_msg'] = TextTemplate(error_message).get_message()
        output['success'] = False
    return output
