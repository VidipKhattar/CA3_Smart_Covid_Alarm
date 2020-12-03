"""Module for global variables that all modules access

alarms_list contains all the alarms that have been set by the user and haven't been set off yet
current_notifs contains all the notifications currently displayed in the notifications column
old_notifs contains notifications that were removed from current_notifs automatically or by the user
to make sure notifications are not repeated
covid_notif contains all the covid related updates that have been displayed as a notification
weather_notif contains all the weather related updates that have been displayed as a notification
"""

alarms_list = []
current_notifs = []
old_notifs = []
covid_notif = []
old_weather_notifs = []
