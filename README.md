# CA3: COVID-19 Smart Alarm Clock
___
### Introduction
___

This Application is a smart alarm clock for daily use through the times of COVID-19. It allows the user to set one or more alarms throughout the day and based on your requirements, the alarm can notify you about covid statistics, weather forecast and current top news stories in your area. The alarm can perform this as announcements when the alarm is triggered, and it can do it silently through text-based notifications. This smart alarm clock will prove useful through these tough times, keeping the user up to date and aware of the happenings in your area.  

### Prerequisites
___

This application was written in Python3.7 programming language, therefore your machine must have a working Python3.7 or higher interpreter. You can download it at [https://www.python.org/downloads/].

To run this application, you will need a web browser preferably google chrome, you can download it here https://www.google.com/chrome/. Other Web browsers may not execute the application as required.

This program makes use of many built-in and 3rd party Python libraries (modules) which can be found on 'PyPI' (Python Package Index). The list of libraries are as follows:

These are built-in modules that you most likely have installed already with Python
- datetime
- time
- sched
- logging
- json

These are 3rd party modules that you need to install if you don't have them
- flask
- pyttsx3
- uk_covid19
- requests

The instructions for installing these libraries will be in the instruction section in this READEME file.

To be able to retrieve all the weather and news information which are taken from external sources, you must use an API, and for it you need an API key from both [https://openweathermap.org/] and [https://newsapi.org/] respectively. Instructions for accessing the API keys and implementing them in the program will be in the instructions section.

You will also need an area code to get covid 19 data from a specific region in the UK. Use [https://findthatpostcode.uk/areatypes/rgn.html] to find one specific to you.

To install the libraries as well as get and use the API keys in the application, you will require and internet connection. Anything above 2mbps will be fine. The faster the connection, the faster the API response time is.


### Installation
___

 To access these libraries required to run the program, you must install them through your machines command line interpreter using pip3 ([More pip3 information here](https://pip.pypa.io/en/stable/)), some you may already have installed. If so, you will receive a message in the command line saying that it is already installed, you can then move on to installing the next library.
 
 There are 2 ways to install them
 
 1. Navigate to the project folder using `cd` in the command line. Then run `pip3 install -r requirements.txt` in the command line 
 
 2. You can open up the command line and manually install them one at a time
```sh
$ pip3 install flask
$ pip3 install pyttsx3
$ pip3 install uk_covid19
$ pip3 install requests
```

To get the API keys you must go to [https://openweathermap.org/] for the weather API key and [https://newsapi.org/] for the news API key, create free accounts in both and get a unique API key from both (you must keep these keys private as if it is comprised, it can ruin the integrity of the application). Once you have both keys you must open the `'config.json'` file in the Smart Alarm System package. It will look like this:

```json
{
    "weather_api":{
        "api_key": "",
        "city": "exeter"
    },

    "news_api":{
        "api_key": "",
        "country": "gb"
    },
    "covid_api":{
        "areaCode": "areaCode=E07000041"
    }
}
```

Where it says `"weather_api"`, directly below it, is a key named `"api_key"`. After the `:`, copy the weather API key you got from [https://openweathermap.org/] and paste it between the quotation marks `""`. You can choose the city of choice for the weather data by changing the value of the `"city"` key, currently it is `"exeter"`

Where it says `"news_api`", directly below it, is a key named `"api_key"`, after the colon, copy the weather API key from [https://newsapi.org/] and paste it between the quotation marks `""`. You can choose the country of choice for the news data by changing the value of the `"country"` key. Currently it is `"gb"` for Great Britain

Directly below the `"Covid API"` key is a `"areaCode"`. This is the code for the specific regions in the UK you want Covid 19 data for. Currently, the code is for Exeter `"areaCode": "areaCode=E07000041"`. Then replace `areaCode=E07000041"` with `"areaCode=(your chosen postcode)"`

Save the `config.json` file and close it
### Getting Started
___
Through your command line interface, navigate to the directory `CA3_project` which is the program folder. And run the following command

```sh
$ python3 -m CA3_code_package.main
```
You should see something like this message appear
```sh
Serving Flask app "main" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Once you see this message, go to your web browser (preferably google chrome) and enter in the search at the top: `127.0.0.1:5000`.

You will see an interface load into the browser like this:
![alt text for screen readers](CA3_code_package/static/images/Interface.png "Text to show on mouseover")

On the left is will display a list with the current alarms that have been set and are yet to go off. The right will display a list with notifications for Covid, News and weather data. Each element of both lists will have a `X` button on them to remove the element from the list. The certain contains the form to set an alarm. The first textbox requires the time you would like the alarm to go off at. Press the Calendar icon on the right-hand side of the textbox, this will trigger a colander to appear which you can use to set the date and time of the alarm down to the second. The next textbox gives the alarm a name which can be anything. Finally, there are 2 checkboxes, one states `Include news briefing?` and the other states `Include weather briefing?`. Checking these boxes will make so that the alarm's verbal announcement will have either a news brief, weather brief, both or none. All alarms have a Covid data announcement as that is a pressing issue. Once you press submit you will see an alarm notification come up on the left-hand side like this ![alt text for screen readers](CA3_code_package/static/images/alarm_ex.png "Text to show on mouseover"). 

Once this alarms time is up, you will hear a voice announcement containing the briefs you chose or not as well as a silent text-based notification on the left similar to the . You will notice that news stories will automatically appear in the notification list and disappear. These news stories are set to appear every 2 minutes and leave every 5 minutes

Disclaimer: There may be a delay of up to one minute on the alarm triggering since the refresh rate for the application to check the time is 60 seconds.


### Testing
___

This program has extensive testing to make sure that the program is running smoothly. Using the `unittest` framework, `try....except` statements and more. These test cover:

- API statuses
- Correct function outputs
- Transfer of data from one function to another

There is a package in `CA3_code_package` called `test` which contains `test_app`: A module that test the status of the called APIs as well as using the `unittest` framework.

When the program is run, these checks are automatically done to make sure the user will not run into any errors during the program.

Using the command line interpreter, you can do these tests without needing to run the program itself. First you must navigate to the project folder, `CA3_project ` through the command line and then use the following command:

```sh
 $ python3 -m pytest
```

If all tests are done correctly, the response should have all green dots and look like this:
![alt text for screen readers](CA3_code_package/static/images/pytest_ex.png "Text to show on mouseover")

If some of the dots are red, it means some of the test have gone wrong. Which is very unlikely


### Developer Documentation
___

This program package contains a number of files:

- Template folder which contains the HTML template for the program
- Static folder containing images etc
- config.json is a persistent file containing private and important data which can change the workings of the program
- sys.log logs all events performed by the application including every time the page refreshes
- covid_19.py is the module for retrieving and formatting the covid data from the covid 19 API
- weather.py is the module for retrieving and formatting the weather data from the weather API
- weather.py is the module for retrieving and formatting the top news data from the news API
- global_vars.py contains the variables used by all other modules together
- main.py is the module in which the code can be run from, it is the module that directly deals with updating the interface e.g., setting and deleting alarms
- test_app.py is the module that contains the testing framework for the program making sure everything is working fine

If you would like to change the data received and displayed from the news, weather and Covid API you can edit the functions to retrieve them. For instance, currently, the weather module will respond with average temperature and a forecast. However, you can change these by adding wind speed from the weather json through changing the `get_weather` function in the `weather` module. 

### Details
___

##### Authors
- Vidip Khattar - Python backend
- University of Exeter Computer Science Department - HTML template frontend

##### Acknowledgements
- [Python Package Index](https://pypi.org/)
- [GitHub](https://github.com/)
- [Postcode Finder]([https://findthatpostcode.uk/areatypes/rgn.html])


For the latest version of this program code, [click here](https://github.com/VidipKhattar/CA3_Smart_Covid_Alarm.git) to access the GitHub repository with the latest updated code

&copy; Vidip Khattar, University of Exeter

Licensed under the [MIT License](License)
