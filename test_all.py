from app import queue_check_test, check_cases_change, notifications_format_test, hhmm_to_seconds, app
from dataget import weather_test, news_test, get_national_covid_json


def test_time_conversion():
    """
    This tests to see if the time extraction and conversion from HH:MM to
    seconds is working correctly
    """
    assert hhmm_to_seconds("20/10/2020 T 15:25") == 55500


def test_queue_exists():
    """
    This checks to see if the sched queue is empty on runtime
    """
    assert queue_check_test()


def test_notifications_format():
    """
    This test ensures that the notifications file has the correct format for
    the provided html template
    """
    assert notifications_format_test()


def test_weather_api():
    """
    This function tests the weather API response, if it is a 200 or a 301,
    the test has been passed.
    """
    assert weather_test() == 200 or weather_test() == 301


def test_news_api():
    """
    This function tests the news API response, if it is a 200 or a 301,
    the test has been passed.
    """
    assert news_test() == 200 or news_test() == 301


def covid_test_api():
    """
    This function will check to see if the covid.json file has anything within
    the list of dictionaries. If there is an item within the 'data': key of the
    covid.json file, then the API is working well.
    """
    assert get_national_covid_json()['data'][0] != {}
