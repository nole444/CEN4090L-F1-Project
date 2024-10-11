# app/services/openf1_service.py


from urllib.request import urlopen
import json
from datetime import datetime, timedelta


def racefinder(date):
    response = urlopen('https://api.openf1.org/v1/sessions?date_start='+date)
    data = json.loads(response.read().decode('utf-8'))

    results = []

    for i in range(len(data)):
        results.append(data[i])

    return results


def findracestart(session_key):
    response = urlopen(
        'https://api.openf1.org/v1/intervals?gap_to_leader<0.5&gap_to_leader>0&session_key='+session_key)
    data = json.loads(response.read().decode('utf-8'))

    return data[0]['date']


def getcardata(driver_number, date):
    datewindowbegin = datetime.fromisoformat(date) - timedelta(seconds=1)

    formattedwindow = datewindowbegin.strftime('%Y-%m-%dT%H:%M:%S.%f')

    response = urlopen('https://api.openf1.org/v1/car_data?driver_number=' +
                       driver_number+'&date>='+formattedwindow+'&date<='+date)

    data = json.loads(response.read().decode('utf-8'))

    return data[len(data) - 1]


def getintervaldata(driver_number, date):
    datewindowbegin = datetime.fromisoformat(date) - timedelta(minutes=5)

    formattedwindow = datewindowbegin.strftime('%Y-%m-%dT%H:%M:%S.%f')

    response = urlopen('https://api.openf1.org/v1/intervals?driver_number=' +
                       driver_number+'&date>='+formattedwindow+'&date<='+date)

    data = json.loads(response.read().decode('utf-8'))

    return data[len(data) - 1]


def getlapdata(driver_number, date):
    datewindowbegin = datetime.fromisoformat(date) - timedelta(hours=4)

    formattedwindow = datewindowbegin.strftime('%Y-%m-%dT%H:%M:%S.%f')

    response = urlopen('https://api.openf1.org/v1/laps?driver_number=' +
                       driver_number+'&date_start>='+formattedwindow+'&date_start<='+date)

    data = json.loads(response.read().decode('utf-8'))

    if data:
        return data[len(data) - 1]
    else:
        return []


def getdriverdata(driver_number):
    response = urlopen('https://api.openf1.org/v1/drivers?driver_number=' +
                       driver_number+'&session_key=latest')
    data = json.loads(response.read().decode('utf-8'))

    return data[0]


def getmeetingdata(meeting_key):
    response = urlopen(
        'https://api.openf1.org/v1/meetings?meeting_key='+meeting_key)

    data = json.loads(response.read().decode('utf-8'))

    return data[0]


def getsessiondata(session_key):
    response = urlopen(
        'https://api.openf1.org/v1/sessions?session_key='+session_key)

    data = json.loads(response.read().decode('utf-8'))

    return data[0]


def getpitdata(driver_number, date):
    datewindowbegin = datetime.fromisoformat(date) - timedelta(hours=4)

    formattedwindow = datewindowbegin.strftime('%Y-%m-%dT%H:%M:%S.%f')

    response = urlopen('https://api.openf1.org/v1/laps?driver_number=' +
                       driver_number+'&date>='+formattedwindow+'&date<='+date)

    data = json.loads(response.read().decode('utf-8'))

    if data:
        return data[len(data) - 1]
    else:
        return []


def getpositiondata(driver_number, date):
    datewindowbegin = datetime.fromisoformat(date) - timedelta(hours=4)

    formattedwindow = datewindowbegin.strftime('%Y-%m-%dT%H:%M:%S.%f')

    response = urlopen('https://api.openf1.org/v1/position?driver_number=' +
                       driver_number+'&date>='+formattedwindow+'&date<='+date)

    data = json.loads(response.read().decode('utf-8'))

    return data[len(data) - 1]


def getstintdata(driver_number, session_key):
    response = urlopen('https://api.openf1.org/v1/stints?driver_number=' +
                       driver_number+'&session_key='+session_key)

    data = json.loads(response.read().decode('utf-8'))

    if data:
        return data[len(data) - 1]
    else:
        return []


def getweather(date):
    datewindowbegin = datetime.fromisoformat(date) - timedelta(minutes=3)

    formattedwindow = datewindowbegin.strftime('%Y-%m-%dT%H:%M:%S.%f')

    response = urlopen(
        'https://api.openf1.org/v1/weather?&date>='+formattedwindow+'&date<='+date)
    data = json.loads(response.read().decode('utf-8'))

    return data[len(data) - 1]


def getalldata(driver_number, date):
    cardata = getcardata(driver_number, date)
    driverdata = getdriverdata(driver_number)
    intervaldata = getintervaldata(driver_number, date)
    lapdata = getlapdata(driver_number, date)
    meetingdata = getmeetingdata(str(cardata['meeting_key']))
    pitdata = getpitdata(driver_number, date)
    positiondata = getpositiondata(driver_number, date)
    sessiondata = getsessiondata(str(cardata['session_key']))
    stintdata = getstintdata(driver_number, str(cardata['session_key']))

    weather = getweather(date)

    print("Driver:", driverdata['full_name'])
    print("Number:", driverdata['driver_number'])
    print("Team:", driverdata['team_name'])

    alldata = [cardata, driverdata, intervaldata, lapdata, meetingdata,
               pitdata, positiondata, sessiondata, stintdata, weather]

    results = {}

    for data in alldata:
        results.update(data)

    results['race_start'] = findracestart(str(cardata['session_key']))

    return results


"""These are function prototypes that we will need
   for handling get requests for race results"""


"""class OpenF1Service:
    def __init__(self):
        self.api_key = os.getenv('OPENF1_API_KEY')
        self.base_url = 'https://api.openf1.org'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def get_race_schedule(self):

        # Fetch the race schedule from the OpenF1 API.

    def get_race_results(self, race_id):

        # Fetch race results for a specific race.

    def get_driver_stats(self, driver_id):

        # Fetch statistics for a specific driver.

    def update_database_with_race_schedule(self):

        # Fetch race schedule and update the database.

    def update_database_with_race_results(self, race_id):

        # Fetch race results and update the database.

    def fetch_and_store_driver_stats(self, driver_id):

        # Fetch driver statistics and store/update in the database."""
