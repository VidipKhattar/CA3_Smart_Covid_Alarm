""" Main Flask module to run the application and deals with alarms and notifications

This module is the main module that uses the Flask Library to run this python code on the HTML
Template as well as directly inject and interact with the Interface such as creating, deleting and
announcing alarms with relevant text notifications. Automatically and Manually add and remove
notifications

"""

from datetime import datetime
import time
import sched
import logging
from flask import Flask, render_template, request
import pyttsx3
from CA3_code_package.covid_19 import get_covid_info
from CA3_code_package.news import get_news
from CA3_code_package.weather import get_weather
from CA3_code_package import global_vars
from CA3_code_package.test import test_app

s = sched.scheduler(time.time, time.sleep)
app = Flask(__name__)
engine = pyttsx3.init()

logging.basicConfig(filename='sys.log', filemode='a', format='%(asctime)s - %(levelname)s - '
                                                             '%(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

flask_logger = logging.getLogger('werkzeug')
SH = logging.StreamHandler()
SH.setLevel(level=logging.DEBUG)
flask_logger.addHandler(SH)


@app.route("/")
def root_to_index() -> render_template:
    """This is called every 60 seconds or if the app manually refreshes for updating the interface

    Defined by the HTML code, this will run every 60 seconds, or whenever the app interface is
    interacted with by manually deleting an alarm or notification or when an alarm is submitted
    the button, this is because when this happens, the URL changes, which triggers this function
    This functions updates the interface by using the functions which delete alarms and
    notifications and automatically add news stories to notifications. And finally renders the
    HTML template showing all the new updates
    """

    # Function to check and remove alarm if it was requested by the user
    man_delete_alarm()
    # Function to check and remove notifications if it was requested by the user
    man_delete_notif()
    # Function to automatically add news story if less than 6 notifications currently on screen
    if len(global_vars.current_notifs) <= 5:
        s.enter(60, 2, auto_add_notif, (get_news(),), )
    #   Renders HTML template with updates changes through injected code
    return render_template('index.html', title="Smart Alarm System", alarms=global_vars.alarms_list,
                           image='image.png', notifications=global_vars.current_notifs)


@app.route("/index", methods=['GET'])
def set_alarm() -> root_to_index:
    """Sets an alarm up with all its required information

    It checks if the a new alarm was requested through the submit button on the interface then it
    converts the alarm time given by the user to epoch time which is subracted by the current epoch
    time and this value is given as a delay value to know when to trigger the alarm. It also checks
    the whether to give news an/or weather briefs. This creates an alarm dictionary with all its
    information to add to the current alarm list
    """

    s.run(blocking=False)
    # Checks whether a new alarm was requested
    if request.method == 'GET':
        # Retrieving alarm data from interface
        content = request.args.get('alarm')
        title = request.args.get('two')
        if content is not None and title is not None:
            # Retrieves whether alarm contains news and/or weather brief
            news = bool(request.args.get('news'))
            weather = bool(request.args.get('weather'))
            # Formatting alarm time appropriately and converting it into an epcoh time delay
            formatted_time = datetime.strptime(content, '%Y-%m-%dT%H:%M')
            epoch_time = datetime.timestamp(formatted_time)
            delay = epoch_time - float(datetime.now().timestamp())
            # Creates dictionary of alarm with all its information to be displayed
            alarm_dict = {"title": title,
                          "content": str(formatted_time) + " News report: " + str(news)
                                     + " Weather report: " + str(weather),
                          "news": news,
                          "weather": weather,
                          "epoch_time": epoch_time}
            # Creates scheduled event in epoch time to trigger alarm announcement
            s.enter(int(delay), 1, announce_alarm, (alarm_dict,))
            global_vars.alarms_list.append(alarm_dict)
            logging.info(
                'An Alarm called %s has been set for: %s News report: %s , Weather report: %s ',
                title, str(formatted_time), str(news), str(weather))
        # Refreshes interface
    return root_to_index()


def announce_alarm(alarm_dict=None) -> None:
    """Announces alarm once it is triggered

    Variables passed = alarm_dict, contains information about an alarm, time, name, briefs.
    This function is called using the scheduled event used in set_alarm
    It take the argument alarm_dict which contains the all the data for the alarm.
    The 2 main things items are whether the alarm has a news and/or weather brief or not.
    the if statement is used to form different announcement text for each combination of the briefs
    It then performs the announcement, adds the relevant notifications and removes the alarm from
    the alarm list. The announcement is done using the pyttsx3 module
    """

    if alarm_dict is None:
        alarm_dict = {}
    # Check if pyttsx3 engine is operating
    try:
        engine.endLoop()
    except RuntimeError:
        pass
    # Condition to check that alarm hasn't been removed after event was scheduled
    if alarm_dict in global_vars.alarms_list:
        # Exception handling if there is no new news articles that haven't been read
        try:
            get_news()[0]
        except IndexError:
            print("error no more news")
            logging.warning('Could\'nt get news in announcement as there are currently no new news')
            global_vars.alarms_list.remove(alarm_dict)
            full_announcement = "The alarm, " + alarm_dict["title"] + ", has gone off. " \
                                + get_covid_info()["announcement"] + ". There are currently no " \
                                "more Headline news reports about coronavirus "
            engine.say(full_announcement)
            engine.runAndWait()
            return
        # Form announcement message and display respective notification based on the briefs wanted
        if alarm_dict["news"] and alarm_dict["weather"]:
            full_announcement = "The alarm, " + alarm_dict["title"] + ", has gone off. " + \
                                get_covid_info()["announcement"] + ".  " \
                                + get_weather()['announcement'] + ". " \
                                + "The latest news story is, " + \
                                get_news()[0]["title"]
            if get_weather() not in global_vars.current_notifs:
                global_vars.current_notifs.append(get_weather())
            global_vars.old_notifs.append(get_news())

        elif alarm_dict["news"] and not alarm_dict["weather"]:
            full_announcement = "The alarm, " + alarm_dict["title"] + ", has gone off. " + \
                                get_covid_info()[
                                    "announcement"] + ". " + "The latest news story is," + \
                                get_news()[0]["title"]
            global_vars.old_notifs.append(get_news())

        elif not alarm_dict["news"] and alarm_dict["weather"]:
            full_announcement = "The alarm, " + alarm_dict["title"] + ", has gone off. " \
                                + get_covid_info()["announcement"] + ". " \
                                + get_weather()['announcement']
            if get_weather() not in global_vars.current_notifs:
                global_vars.current_notifs.append(get_weather())

        elif not alarm_dict["news"] and not alarm_dict["weather"]:
            full_announcement = "The alarm, " + alarm_dict["title"] + ", has gone off. " \
                                + get_covid_info()["announcement"]
        else:
            logging.error("Undefined combination of briefs wanted")
            full_announcement = "Error"
        # Check if covid notification is not already in the notification list
        if get_covid_info() not in global_vars.current_notifs:
            global_vars.current_notifs.append(get_covid_info())
        # Using pyttsx3 to announce the formed message
        engine.say(full_announcement)
        engine.runAndWait()
        global_vars.alarms_list.remove(alarm_dict)
        logging.info(" Announcement for alarm: %s for %s has been sounded", alarm_dict['title'],
                     alarm_dict['content'])
        logging.info("The alarm: %s has been removed from alarm list", alarm_dict["title"])


def auto_add_notif(news_list=None) -> None:
    """When called, silently automatically add news story to notification list

    Variable passed = news_list, list(dict) contains a news story's title and a link to the story
    Function checks if there is space in the notification list, if so, it adds it to list, then the
    function triggers a scheduled another event to automatically remove this article from the list
    after a delay time
    :rtype: object
    """

    if news_list is None:
        news_list = []
    if len(global_vars.current_notifs) <= 5:
        for article in news_list:
            if article not in global_vars.old_notifs:
                global_vars.old_notifs.append(article)
                global_vars.current_notifs.append(article)
                logging.info("article: %s has been automatically added to the notification list",
                             article['title'])
                # Scheduled event to automatically remove said article using another function
                s.enter(180, 2, auto_remove_notifs, (article,), )
                break


def auto_remove_notifs(article=None) -> None:
    """Automatically removes notification given as the argument 'article

    Variable passed = article, (dict) contains a news story's title and a link to the story
    This function is called by auto_notif which automatically adds a news story, it then requires
    to automatically remove this after a given time. A scheduled event in auto_notif that takes the
    argument of the news story to be removed, calls this function to remove it.
    """

    if article is None:
        article = {}
    # Check if news story is currently in the notification list
    if article in global_vars.current_notifs:
        global_vars.current_notifs.remove(article)
        logging.info("article: %s has been automatically removed from the notification list",
                     article['title'])


def man_delete_alarm() -> None:
    """Deleting an alarm when user manually selects delete

    This is called in root_to_index which will refresh the template in the case of the user pressing
    the delete button next to the alarm name as this will change the URL which will state the name
    of the alarm to be deleted. Once this function is called in the root_to_index function, it will
    check if an alarm name is in the URL and take this name and remove it's accosciative alarm from
    from the list
    """

    # Checks if alarm name is in the URL
    if request.args.get("alarm_item"):
        alarm_to_remove = request.args.get("alarm_item")
        for alarm in global_vars.alarms_list:
            # Checks if this alarm for the alarm name is in the current alarm to be sounded list
            if alarm["title"] == alarm_to_remove:
                global_vars.alarms_list.remove(alarm)
                logging.debug("article: %s has been manually removed from the notification list",
                              alarm_to_remove)


def man_delete_notif() -> None:
    """Deleting a notification when user manually selects delete

    This is called in root_to_index which will refresh the template in the case of the user pressing
    the delete button next to the notification name as this will change the URL which will state the
    name of the notification to be deleted. Once this function is called in the root_to_index
    function, it will check if a notification name is in the URL and take this name and remove
    it's accosciative notification from the list.
    It is similar to the man_delete_alarm function
    """

    # Checks if notification name is in the URL
    if request.args.get("notif"):
        notif_to_remove = request.args.get("notif")
        for notif in global_vars.current_notifs:
            # Iterate of notification list to check if the item is there in the list
            if notif["title"] == notif_to_remove:
                global_vars.current_notifs.remove(notif)
                global_vars.old_notifs.append(notif)
                logging.info("The notification %s has been manually removed from notification list",
                             str(notif_to_remove))



if __name__ == "__main__":
    try:
        test_app.test_api()
    except AssertionError as message:
        print(message)
    app.run(debug=True)
