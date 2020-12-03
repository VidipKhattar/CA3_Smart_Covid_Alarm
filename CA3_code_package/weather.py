"""Retrieving Covid-19 information

This module gets up to date weather information through an API supplied by "openweathermap.org".
It formats the information as an update to be use as a notification for an alarm announcement if it
is not already there
"""

import json
import logging
import requests
from CA3_code_package import global_vars

logging.basicConfig(filename='sys.log', format='%(asctime)s  - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def get_weather() -> dict:
    """Retrieves parameters defined in config.json, filters and formats weather data for the alarm.

        It retrieves a user-defined JSON file through a URL containing the openweathermap link, the
        specific city/region for the weather data, as well as an API key given by openweathermap .
        This data is applied accordingly to a dictionary type with the keys: title, content and
        announcement to notify the user of weather data. This dictionary is added to a list of
        current notifications to be displayed.
        """

    base_url = "http://api.openweathermap.org/data/2.5/weather?q="
    # Validating and Retrieving a region and an API key from config.json for the weather json file
    with open('config.json', 'r') as config_file:
        json_config = json.load(config_file)
        weather_config = json_config['weather_api']
        api_key = weather_config['api_key']
        city = weather_config['city']
    # forming complete URL containing a weather json file from user-defined components
    complete_url = base_url + city + "&appid=" + api_key
    # Retrieves JSON file of user-defined parameters
    response = requests.get(complete_url)
    if response.status_code == 200:
        weather_json = response.json()
        try:
            main_weather = weather_json["weather"]
            forecast_description = main_weather[0]["description"]
            main = weather_json["main"]
            temp = main["temp"]
        except KeyError as excep:
            logging.error("%s Valid JSON file cannot be retrieved as likely invalid API key", excep)
            forecast_description = "Unable to get weather info"
            temp = 0
        # Creates dictionary to be added to notification list with appropriate information
        weather_notif = {"title": "Weather Update",
                         "content": forecast_description + ", average temperature: " +
                         str(int(temp - 273)) + "°C",
                         "announcement": " Today's forecast is " + forecast_description +
                                         ". The average temperature is " + str(int(temp - 273))
                                         + " degrees celsius"}
        # Check to see if weather notification isn't already in the list of current notifications
        if weather_notif not in global_vars.old_weather_notifs:
            global_vars.old_weather_notifs.append(weather_notif)
            global_vars.current_notifs.append(weather_notif)
    return weather_notif
