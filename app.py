#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This is the app module of the Smart Daily Briefings Website. This contains a
range of functions, and is responsible for the hosting of the flask web server.
"""
import sched
import time
import datetime
import json
import logging
import pyttsx3
from apscheduler.schedulers.background import BackgroundScheduler
from flask.logging import create_logger
from flask import Flask, render_template, request, redirect, Markup
from dataget import weather, news, get_national_covid_json

app = Flask(__name__)
log = create_logger(app)
logging.basicConfig(filename='log.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s : %(message)s'
                    )
s = sched.scheduler(time.time, time.sleep)
schedd = BackgroundScheduler()  # This initializes the APScheduler

schedd.add_job(func=weather, trigger='interval', hours=1)
schedd.add_job(func=news, trigger='interval', hours=1)
schedd.add_job(func=get_national_covid_json, trigger='interval',
               hours=1)
# Weather, News, and Covid data is updated once per hour with APScheduler

weather()  # Updates the weather on runtime

news()  # Updates the news on runtime

get_national_covid_json()  # Updates the covid data on runtime


def current_time_refresh() -> str:
    """
    This functions main job is to make sure the current time is always up
    to date for the alarms to be set accurately.
    It uses an Advanced Python Scheduler outside of
    the function to update the current time once every 60 seconds.
    """

    now = datetime.datetime.now()
    current_time = now.strftime('%D/%M/%Y T %H:%M')
    return current_time


schedd.add_job(func=current_time_refresh, trigger='interval',
               seconds=60)


def tts(announcement, *args):
    """
    The tts function takes one argument, announcement, and uses pyttsx3 to
    announce the required information. The function tries to end the
    pyttsx3 engine loop, but if there is an error, it passes. Then the
    announcement is made, and the user is redirected back to the /index page.
    """
    engine = pyttsx3.init()
    try:
        engine.endLoop()
    except BaseException:
        pass
    engine.say(announcement)
    engine.runAndWait()
    engine.stop()
    return redirect('/index')


def hhmm_to_seconds(time_value: str) -> int:
    """
    This function takes the argument of time_value with the format
    d/m/y T hh:mm with the T being a separator between date and time.
    The function extracts the integer values of the hours and minutes,
    multiplies them by 3600 and 60 respectively, and returns this value.
    """

    time_val_list = time_value.split('T')
    time_val_list1 = time_val_list[1]
    ':'.join(time_val_list1)
    time_val_list1 = str(time_val_list1)
    (hours, minutes) = time_val_list1.split(':')
    return int(hours) * 3600 + int(minutes) * 60


def extract_data_for_notifications():
    """
    This function is responsible for extracting the articles from the
    news.json file and the covid case statistics from the covid.json file.
    Notifications is created here as a list of dictionaries,
    based on the length of the number of articles, plus one for the covid
    update. The uk_covid19 module can return updates where the deaths display
    as null or None, and I have observed this for up to the past two updates.
    As a defensive measure I have implemented type checking to
    ensure that only numbers are displayed in the notification, and not a null
    or None value. The function dumps the relevant data to a notifications.json
    file. This function is also run with the Advanced Python Scheduler every
    hour to update the notifications.json file.
    """

    news_json = open('news.json', 'r')
    covid = open('covid.json', 'r')
    log.info('news.json and covid.json have been opened in read mode')
    interim = json.load(covid)
    covid_data = interim['data']
    news_json = json.load(news_json)
    art = news_json['articles']
    notifications = [{} for x in range(len(art) + 1)]
    i = 1
    for article in art:
        new2 = notifications[i]
        new2['title'] = article['title']
        url = article['url']
        desc = article['description']
        new2['content'] = Markup("<a href='" + url + "'>" + desc
                                 + '</a>')
        i += 1
    log.info('Articles have been updated from json')
    today = covid_data[0]
    previous_update_1 = covid_data[1]
    previous_update_2 = covid_data[2]
    new4 = notifications[0]
    new4['title'] = 'Coronavirus Data Update'
    if isinstance(today['newDeathsByDeathDate'], int) \
            or isinstance(today['cumDeathsByDeathDate'], int):
        new4['content'] = "Today's New Cases: " \
            + str(today['newCasesByPublishDate']) + '\tTotal Cases: ' \
            + str(today['cumCasesByPublishDate']) \
            + "\nToday's New Deaths: " \
            + str(today['newDeathsByDeathDate']) + '\nTotal Deaths: ' \
            + str(today['cumDeathsByDeathDate'])
    elif isinstance(previous_update_1['newDeathsByDeathDate'], int) \
            or isinstance(previous_update_1['cumDeathsByDeathDate'], int):
        new4['content'] = "Today's New Cases: " \
            + str(today['newCasesByPublishDate']) + '\tTotal Cases: ' \
            + str(today['cumCasesByPublishDate']) \
            + "\nToday's New Deaths: " \
            + str(previous_update_1['newDeathsByDeathDate']) \
            + '\nTotal Deaths: ' \
            + str(previous_update_1['cumDeathsByDeathDate'])
    else:
        new4['content'] = "Today's New Cases: " \
            + str(today['newCasesByPublishDate']) + '\nTotal Cases: ' \
            + str(today['cumCasesByPublishDate']) \
            + "\nToday's New Deaths: " \
            + str(previous_update_2['newDeathsByDeathDate']) \
            + "\nToday's New Deaths: " \
            + str(previous_update_2['cumDeathsByDeathDate'])
    with open('notifications.json', 'w') as ofile:
        json.dump(notifications, ofile, sort_keys=True, indent=4)


extract_data_for_notifications()  # Extracts most recent data from the API's on
# runtime.
schedd.add_job(func=extract_data_for_notifications, trigger='interval',
               hours=1)  # Updates notifications hourly.


def extract_data() -> list:
    """
    This function opens the notifications.json file and creates another list
    of dictionaries called notifications. It then uses the
    file to populate the dictionaries, and then returns the list for use later.
    """

    with open('notifications.json', 'r') as notif:
        notif = json.load(notif)
        notifications = [{} for i in range(len(notif))]
        i = 0
        for element in notif:
            notifs = notifications[i]
            notifs_file = notif[i]
            notifs['title'] = notifs_file['title']
            notifs['content'] = Markup(notifs_file['content'])
            i += 1
        return notifications


extract_data()  # Updates the notifications data structure on runtime in order
# to make sure the displayed notifications are the most recent.


def news_for_alarms() -> list:
    """
    This function opens the news.json file and creates a list called
    articles. Here it appends the article titles for reading by the
    announcement.It returns this list for use in s.enter later on.
    """

    with open('news.json', 'r') as news_data:
        log.info('News.json has been opened for an alarm')
        news_data = json.load(news_data)
        art = news_data['articles']
        i = 0
        articles = []
        for article in art:
            article = article['title']
            article = str(article)
            articles.append(article)
            i += 1
        return articles


def store_data():
    """
    This function is run by the Advanced Python Scheduler every 12 hours.
    It opens the covid json file as read, and opens a textfile named
    local_covid_store as write.It then adds the current case count to
    the local_covid_store file.
    """

    with open('covid.json', 'r') as covid:
        with open('local_covid_store.txt', 'w') as local_covid:
            log.info(
                'covid.json and local_covid_store.txt have been opened'
                'as read and write respectively')
            interim = json.load(covid)
            covid_data = interim['data']
            today = covid_data[0]
            today_cases = today['newCasesByPublishDate']
            today_cases = str(today_cases)
            local_covid.write(today_cases)


schedd.add_job(
    func=store_data,
    trigger='interval',
    hours=12)  # This creates an
# APScheduler instance calls the store_data function to store the most
# recent case data.


def check_cases_change():
    """
    This function is also run every 1 hour by the Advanced Python Scheduler.
    It opens both the covid.json file and the local_covid_store.txt files
    in read mode. It then compares the values, if the increase in cases
    since the last update is more than 30%,it uses tts to announce this.
    Otherwise it returns false.
    """

    with open('covid.json', 'r') as covid:
        with open('local_covid_store.txt', 'r') as local_covid:
            log.info(
                'covid.json and local_covid_store.txt have been opened as read')
            interim = json.load(covid)
            covid_data = interim['data']
            today_ap = covid_data[0]
            today_api = today_ap['newCasesByPublishDate']
            today_local = local_covid.read()
            today_local = int(today_local)
            file = open('config.json', 'r')
            file = json.load(file)
            user_number = file['user_threshold_number']
            if (today_api - today_local) / today_api >= user_number:
                today_api = str(today_api)
                log.info('Case increse by more than ' + str(user_number)
                         + 'percent since last update!')
                return tts(
                    'COVID Alert, Cases have increased by ' + str(user_number)
                    + 'percent or more since the last update.', 'dummy_arg')
            else:
                return 'False'


check_cases_change()
schedd.add_job(func=check_cases_change, trigger='interval', minutes=60)
# This once again uses APScheduler to check if the cases have increased
# by a percentage value set by the user every hour.


def s_since_epoch(arg: float) -> str:
    """
    This function takes an argument called arg, and converts it
    from seconds since the epoch (1 Jan 1970) to m/d/y hh:mm format
    """

    return time.strftime('%m/%d/%y %H:%M', time.gmtime(arg))


weather = weather()
news_for_alarm = news_for_alarms()


@app.route('/index', methods=['GET'])
def event_schedule():
    """
    This function begins with starting the sched instance. Then variables are assigned from the
    request return values of the alarm time box, the label box, and the two tick boxes.
    Then, if an alarm is set, the notifications variable is assigned to the return value of
    the function named extract_data, then there are some if statements to check which boxes
    have been checked. Depending on this, an alarm with the desired functionality is created
    and added to the queue. Then, a list of dictionaries named alarms is created, populated
    with the values from the sched queue, which was assigned to the variable name queue.
    This then returns the template index.html with alarms and notifications defined as
    themselves in order to display them on the website. When the page is loaded normally
    and an alarm has not been created, the notifications are also loaded from the return
    value of the extract_data function, and then the list of dictionaries named alarms is
    created, populated with the values from the sched queue, which is assigned to the
    variable named queue.
    """

    s.run(blocking=False)
    alarm_time = request.args.get('alarm')
    current_time = current_time_refresh()
    if alarm_time:
        yes_no_weather = request.args.get('weather')
        log.info('weather checkbox status requested from server')
        yes_no_news = request.args.get('news')
        log.info('news checkbox status requested from server')
        notifications = extract_data()
        current_time = current_time_refresh()
        alarm_label = request.args.get('two')
        log.info('Alarm label requested from server')
        notif = request.args.get('notif')
        both = (weather, news_for_alarm)
        delay = hhmm_to_seconds(alarm_time) \
            - hhmm_to_seconds(current_time)
        if yes_no_weather:
            if not yes_no_news:
                s.enter(int(delay), 1, tts, [weather, alarm_label])
                log.info('Alarm added')
            else:
                s.enter(int(delay), 1, tts, [both, alarm_label])
                log.info('Alarm added')
        elif yes_no_news:
            if not yes_no_weather:
                s.enter(int(delay), 1, tts, [news_for_alarm,
                                             alarm_label])
                log.info('Alarm added')
        else:
            s.enter(int(delay), 1, tts, [alarm_label + ' Has Finished',
                                         alarm_label])
            log.info('Alarm added')
        queue = s.queue
        alarms = [{} for x in range(len(queue))]
        i = 0
        if notif:
            notif_1 = open('notifications.json', 'r')
            notif_loaded = json.load(z)
            i = 0
            for element in notif_loaded:
                notification = element['title']
                if notification == notif:
                    log.info(
                        notification +
                        ' has been dismissed for one hour.')
                    notif_loaded.pop(i)
                    i += 1
                else:
                    i += 1
            with open('notifications.json', 'w') as data_file:
                json.dump(notif_loaded, data_file)
        for alarm in alarms:
            alarm_item_1 = queue[i]
            alarm_item_data = alarm_item_1[3]
            alarm['title'] = str(alarm_item_data[1])
            alarm['content'] = str(s_since_epoch(alarm_item_1[0]))
            i += 1
        return render_template('index.html', alarms=alarms,
                               image='kek.png',
                               notifications=notifications)
    else:
        notifications = extract_data()
        i = 0
        queue = s.queue
        alarms = [{} for x in range(len(queue))]
        alarm_label = request.args.get('two')
        notif = request.args.get('notif')
        current_time = current_time_refresh()
        if notif:
            notif_1 = open('notifications.json', 'r')
            notif_loaded = json.load(notif_1)
            i = 0
            for element in notif_loaded:
                notification = element['title']
                if notification == notif:
                    log.info(
                        notification +
                        ' has been dismissed for one hour.')
                    notif_loaded.pop(i)
                    i += 1
                else:
                    i += 1
            with open('notifications.json', 'w') as data_file:
                json.dump(notif_loaded, data_file)
        for alarm in alarms:
            alarm_item_1 = queue[i]
            alarm_item_data = alarm_item_1[3]
            alarm['title'] = str(alarm_item_data[1])
            alarm['content'] = str(s_since_epoch(alarm_item_1[0]))
            i += 1
        return render_template('index.html', alarms=alarms,
                               image='kek.png',
                               notifications=notifications)


schedd.start()


def queue_check_test():
    x = s.empty()
    return x


def notifications_format_test() -> bool:
    with open('notifications.json', 'r') as file:
        notifications = json.load(file)
        notifications = notifications[0]
        if notifications['title'] == notifications['title'] and \
                notifications['content'] == notifications['content']:
            return True
        else:
            return False


@app.route('/')
def index():
    """
    Finally, the index function just redirects the user from the /
    route to the /index route.
    """

    return redirect('/index')


if __name__ == '__main__':
    app.run(debug=True)
