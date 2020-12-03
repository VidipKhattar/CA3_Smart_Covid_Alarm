"""Retrieving Covid-19 information

This module gets Covid-19 information through a third party API using the python library:
uk_covid19 which is supplied by Public Health England and formats the information as an update to
be use as a notification for an alarm announcement
"""

import json
import logging
from uk_covid19 import Cov19API
from CA3_code_package import global_vars

logging.basicConfig(filename='sys.log', format='%(asctime)s  - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def get_covid_info() -> dict:
    """Retrieves the parameters defined in config.json to filter covid data needed by the user.

    areaCode as defined in config.json gives the area in the UK the user wants covid data for.
    cases_and_death defines the specific type of covid data the user requires.
    These 2 parameters along with sorting by latest date are the arguments used to retrieve a JSON
    file with the relevant covid data.
    This data is applied to a dictionary type with the keys: title, content and announcement.
    This dictionary is added to a list of current notifications to be displayed.
    """

    # Validating and Retrieving parameters for the covid info JSON file
    filter_param = []
    with open('config.json', 'r') as config_file:
        json_config = json.load(config_file)
    try:
        covid_api = json_config["covid_api"]
        filter_param = [covid_api["areaCode"]]
    except KeyError as excep:
        logging.error("area code or covid dictionary is missing in JSON file %s", excep)
    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeaths28DaysByPublishDate": "newDeaths28DaysByPublishDate",
        "cumDeaths28DaysByPublishDate": "cumDeaths28DaysByPublishDate",
        "cumDeaths28DaysByDeathDateRate": "cumDeaths28DaysByDeathDateRate"
    }
    # Retrieves JSON file of user-defined parameters
    api = Cov19API(filters=filter_param, structure=cases_and_deaths, latest_by="date")
    covid_json = api.get_json()
    covid_data = covid_json['data']
    # Gives a threshold of 20 cases as that is the average
    if int(covid_data[0]['newCasesByPublishDate']) >= 20:
        threshold = ". There is a relatively substantial increase in new cases. "
    else:
        threshold = ". This is a normal increase in new cases. "
    # Creates dictionary to be added to notification list with appropriate information
    covid_notif = {
        "title": "Covid Update: " + covid_data[0]['date'] + " " + covid_data[0]["areaName"],
        "content": str(covid_data[0]['newCasesByPublishDate']) +
        " new cases today in " + covid_data[0]["areaName"] + threshold + "(" +
        str(covid_data[0]['cumCasesByPublishDate']) + " total) " + str(
            covid_data[0]["newDeaths28DaysByPublishDate"]) + " new deaths (" + str(
            covid_data[0]["cumDeaths28DaysByPublishDate"]) + " total)",
        "announcement": "There are " + str(covid_data[0]['newCasesByPublishDate'])
                        + " new cases today in " + covid_data[0]["areaName"] + threshold +
                        ". A total of " + str(covid_data[0]['cumCasesByPublishDate']) +
                        " cases. There has been" + str(
            covid_data[0]["newDeaths28DaysByPublishDate"]) + " new deaths. A total of " + str(
            covid_data[0]["cumDeaths28DaysByPublishDate"]) + " deaths"}
    # Check to see if covid notif isn't already in the list of current notifications
    if covid_notif not in global_vars.covid_notif:
        global_vars.covid_notif.append(covid_notif)
        global_vars.current_notifs.append(covid_notif)
    return covid_notif
