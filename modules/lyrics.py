import os

import requests

import config
from templates.text import TextTemplate

MUSIXMATCH_API_KEY = os.environ.get('MUSIXMATCH_API_KEY', config.MUSIXMATCH_API_KEY)


def process(message):
    output = {}
    try:
        # Search in title
        r = requests.get('http://api.musixmatch.com/ws/1.1/track.search', params={
                         'apikey': MUSIXMATCH_API_KEY,
                         'q_track': message,
                         's_track_rating': 'desc',
                         'f_has_lyrics': '1'
                         })
        data = r.json()
        # Search inside lyrics if no results found in title search
        if int(data['message']['header']['available']) == 0:
            r = requests.get('http://api.musixmatch.com/ws/1.1/track.search', params={
                             'apikey': MUSIXMATCH_API_KEY,
                             'q_lyrics': message,
                             's_track_rating': 'desc',
                             'f_has_lyrics': '1'
                             })
            data = r.json()
        track = data['message']['body']['track_list'][0]['track']
        track_id = track['track_id']
        track_name = track['track_name']
        artist_name = track['artist_name']
        lyrics_url = track['track_share_url']

        r = requests.get('http://api.musixmatch.com/ws/1.1/track.lyrics.get', params={
                         'apikey': MUSIXMATCH_API_KEY,
                         'track_id': track_id
                         })
        data = r.json()
        lyrics = data['message']['body']['lyrics']['lyrics_body']
        string1 = ('Here are the lyrics of ' + track_name + ' by ' + artist_name + ':\n' + lyrics
                   + '\n- Powered by MusiXmatch')
        string2 = '\nFull Lyrics: ' + lyrics_url
        output['output'] = string1 + string2
        output['success'] = True
    except Except:
        error_message = 'I couldn\'t find any lyrics matching your query.'
        error_message += '\nPlease ask me something else, like:'
        error_message += '\n  - paradise lyrics'
        error_message += '\n  - lyrics of the song hall of fame'
        error_message += '\n  - What are the lyrics to see you again?'
        output['error_msg'] = TextTemplate(error_message).get_message()
        output['success'] = False
    return output
