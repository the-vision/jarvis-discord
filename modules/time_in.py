import discord
import requests
import os
import config
from templates.text import TextTemplate
from datetime import datetime

TIMEZONEDB_TOKEN = os.environ.get('TIMEZONEDB_TOKEN', config.TIMEZONEDB_TOKEN)
MAPQUEST_CONSUMER_KEY = os.environ.get('MAPQUEST_CONSUMER_KEY', config.MAPQUEST_CONSUMER_KEY)

def process(message):
        output = {}
        r = requests.get(
            'http://open.mapquestapi.com/nominatim/v1/search.php?key=' + MAPQUEST_CONSUMER_KEY + '&format=json&q=' + message+ '&limit=1')
        location_data = r.json()
        r = requests.get('http://api.timezonedb.com/?lat=' + location_data[0]['lat'] + '&lng=' + location_data[0][
            'lon'] + '&format=json&key=' + TIMEZONEDB_TOKEN)
        time_data = r.json()
        time = datetime.utcfromtimestamp(time_data['timestamp']).strftime('%a %b %d %Y %H:%M:%S')
        output['output'] = TextTemplate('Location: ' + location_data[0]['display_name'] + '\nTime: ' + time + ' ' + time_data[
                       'abbreviation']).get_message()
        return output['output']