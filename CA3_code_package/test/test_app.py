"""Module for testing functionality of the program

Includes Unit testing for each function and external tests for API calls
"""

import unittest
import json
import requests
from CA3_code_package import weather
from CA3_code_package import covid_19
from CA3_code_package import news
from CA3_code_package import main
from CA3_code_package import global_vars


def test_api():
    """function for testing if the program is able call the restful APIs from external sources"""

    base_weather_url = "http://api.openweathermap.org/data/2.5/weather?q="
    base_news_url = "https://newsapi.org/v2/top-headlines?"

    with open('config.json', 'r') as config_file:
        json_config = json.load(config_file)
        weather_config = json_config['weather_api']
        weather_api_key = weather_config['api_key']
        weather_city = weather_config['city']
        news_config = json_config['news_api']
        news_api_key = news_config['api_key']
        news_country = news_config['country']

    weather_url = base_weather_url + weather_city + "&appid=" + weather_api_key
    news_url = base_news_url + "country=" + news_country + "&apiKey=" + news_api_key
    weather_response = requests.get(weather_url)
    news_response = requests.get(news_url)
    assert weather_response.status_code == 200
    assert news_response.status_code == 200


class TestWeather(unittest.TestCase):
    """Class for unit testing the get_weather function in the weather module"""

    def test_weather_none(self) -> None:
        """test whether the function: get_weather returns a value and is not None"""

        weather_dict = weather.get_weather()
        self.assertIsNotNone(weather_dict)

    def test_weather_dict(self) -> None:
        """test whether the function: get_weather returns a Dictionary value"""

        weather_dict = weather.get_weather()
        self.assertIsInstance(weather_dict, dict)

    def test_weather_append_to_notif_list(self) -> None:
        """test if the function: get_weather appends its return value to the notification list"""

        weather_dict = weather.get_weather()
        self.assertIn(weather_dict, global_vars.current_notifs)


class TestCovid(unittest.TestCase):
    """Class for unit testing the get_covid_info function in the covid_19 module"""

    def test_covid_none(self) -> None:
        """test whether the function: get_covid_info returns a value and not None"""

        covid_dict = covid_19.get_covid_info()
        self.assertIsNotNone(covid_dict)

    def test_covid_dict(self) -> None:
        """test whether the function: get_covid_info returns a Dictionary value"""

        covid_dict = covid_19.get_covid_info()
        self.assertIsInstance(covid_dict, dict)

    def test_covid_append_to_notif_list(self) -> None:
        """test if the function: get_covid_info appends its return value to the notification list"""

        covid_dict = covid_19.get_covid_info()
        self.assertIn(covid_dict, global_vars.current_notifs)


class TestNews(unittest.TestCase):
    """Class for unit testing the get_news function in the news module"""

    def test_news_none(self) -> None:
        """test whether the function: get_news returns a value and not None"""

        news_list = news.get_news()
        self.assertIsNotNone(news_list)

    def test_news_dict(self) -> None:
        """test whether the function: get_news returns a Dictionary value"""

        news_list = news.get_news()
        self.assertIsInstance(news_list, list)


class TestNotif(unittest.TestCase):
    """Class for unit testing the notification functions in the main module"""

    def test_auto_add_notif_append(self) -> None:
        """test whether the function: auto_add_notif adds its argument to the current_notifs list"""

        articles = [{'title': 'article'}]
        main.auto_add_notif(articles)
        self.assertIn(articles[0], global_vars.current_notifs)

    def test_auto_remove_notif(self) -> None:
        """test whether the function: auto_remove_notif removes its argument from the current_notifs
         list"""

        global_vars.current_notifs = [{'title': 'article'}, {'title': 'article2'}]
        article = {'title': 'article'}
        main.auto_remove_notifs(article)
        self.assertNotIn(article, global_vars.current_notifs)


if __name__ == '__main__':
    test_api()
    unittest.main()
