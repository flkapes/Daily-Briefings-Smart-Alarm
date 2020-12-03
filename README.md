Faris Lawrence Kapes	Smart Daily Briefings Website	01/12/2020


This is the documentation for my Daily Briefing website, written in python with Flask. Its main functionalities include the setting of alarms, with the option to add news and/or weather updates that are announced with text-to-speech. In addition, it has the functionality to detect if a large change in COVID-19 cases has happened, if it detects this it uses text-to-speech to announce this. The top headlines from the BBC are shown on the right side of the website along with the most recent COVID-19 statistics. Logs are saved to the log.log file.


The prerequisites are as follows:

* Python 3.8 or higher
* Flask
* Pyttsx3
* Datetime
* APScheduler
* Requests
* UK_COVID19


All relevant settings are changeable in the config.json file included in the zip file. Two API keys are also needed. These are OpenWeatherMap and NewsAPI and again, can be added or changed in the config.json file. 
The default value for the covid_area_type is is nation, but the possible values are:

1. overview - Overview data for the United Kingdom
2. nation - Nation data (England, Northern Ireland, Scotland, and Wales)
3. region - Region data
4. nhsRegion - NHS Region data
5. utla - Upper-tier local authority data
6. ltla - Lower-tier local authority data

The default value for covid_area_name is England, but this can be changed in line with the covid_area_type.
The weather_city_name can be updated to any city name, but please check https://openweathermap.org/ for the way the city is named on the API.
The threshold for a COVID case announcement can also be adjusted by changing the user_threshold_number in the config.json file. The range is between 0 and 1.
Once config file is updated, you can navigate to http://127.0.0.1:5000/ and begin adding alarms and briefings. Notification data will be updated once per hour, and alarms will go off at any time you set. 



------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



Copyright 2020 Faris L Kapes
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
