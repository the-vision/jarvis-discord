import discord
import requests
import os
import config
from templates.text import TextTemplate

OPEN_WEATHER_MAP_TOKEN = os.environ.get('OPEN_WEATHER_MAP_TOKEN', config.OPEN_WEATHER_MAP_TOKEN)

def process(message):
    output = {}
    url = 'http://api.openweathermap.org/data/2.5/weather?appid=' + OPEN_WEATHER_MAP_TOKEN + '&q=' + message
    r = requests.get(url).json()
    Weather = r['weather'][0]['description']
    FahreneitTemperature = int((int(r['main']['temp']) * 9/5) - 459.67)
    CelsiusTemperature = int(5/9 * (int(FahreneitTemperature) - 32))
    name = r['name']
    country = r['sys']['country']
    output['output'] = TextTemplate("Location: " + name + "," + country + "\n"
                   "Weather: " + Weather + "\n"
                   "Temperature: " + str(CelsiusTemperature) + "°C / " + str(FahreneitTemperature) + "°F\n"
                   "-Info provided by OpenWeatherMap").get_message()
    return output['output']