"""Retrieving current Top news stories

This module gets up to date current Top news stories through an API supplied by "newsapi.org".
It formats the information as an news story to be use as a notification and an announcement in the
alarm and its interface
"""

import json
import logging
import requests
from flask import Markup
from CA3_code_package import global_vars

logging.basicConfig(filename='sys.log', format='%(asctime)s  - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def get_news() -> list or None:
    """Retrieves parameters defined in config.json, filters and formats weather data for the alarm.

    It retrieves a user-defined JSON file through a URL containing the newsapi link, the
    specific country/region for the news data, as well as an API key given by newsapi.org.
    This data is applied accordingly to a dictionary type with the keys: title, content and
    announcement to notify users clearly of top news stories in the country.
    This dictionary is added to a list of current notifications to be displayed and/or voiced.
    """

    news_list = []
    base_url = "https://newsapi.org/v2/top-headlines?"
    # Validating and Retrieving a country and an API key from config.json for the news json file
    with open('config.json', 'r') as config_file:
        api_config = json.load(config_file)
        news_config = api_config['news_api']
        api_key = news_config['api_key']
        country = news_config['country']
    # forming complete URL containing a news json file from user-defined components
    complete_url = base_url + "country=" + country + "&apiKey=" + api_key
    # Retrieve and validates news JSON file
    response = requests.get(complete_url)
    if response.status_code == 200:
        try:
            articles = response.json()["articles"]
        except KeyError as excep:
            logging.error("JSON file cannot be retrieved as invalid URL or API key %s", excep)
            return None
        for article in articles:
            # filters articles that contain covid or coronavirus in the title
            if "covid" in article["title"].lower() or "coronavirus" in article["title"].lower():
                check_news_list = [{"title": article["title"],
                                    "content": Markup("<a href=" + article["url"] + ">"
                                                      + article["url"] + "<a>")}]
                # Checks if article has not already been a notification
                if check_news_list not in global_vars.old_notifs:
                    # Creates dictionary to be added to notif list with article title and its link
                    news_list.append({"title": article["title"],
                                      "content": Markup("<a href=" + article["url"] + ">"
                                                        + article["url"] + "<a>")})
                    break
    return news_list
