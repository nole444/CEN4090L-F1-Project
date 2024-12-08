# app/services/openf1_service.py


from urllib.request import urlopen
import json
from datetime import datetime, timedelta

driver_dict = {
    1: "Max Verstappen",
    10: "Pierre Gasly",
    11: "Sergio Pérez",
    14: "Fernando Alonso",
    16: "Charles Leclerc",
    18: "Lance Stroll",
    2: "Logan Sargeant",
    20: "Kevin Magnussen",
    22: "Yuki Tsunoda",
    23: "Alexander Albon",
    24: "Zhou Guanyu",
    27: "Nico Hülkenberg",
    3: "Daniel Ricciardo",
    31: "Esteban Ocon",
    37: "Isack Hadjar",
    50: "Oliver Bearman",
    4: "Lando Norris",
    40: "Ayumu Iwasa",
    44: "Lewis Hamilton",
    43: "Franco Colapinto",
    55: "Carlos Sainz",
    61: "Jack Doohan",
    63: "George Russell",
    77: "Valtteri Bottas",
    81: "Oscar Piastri",
    97: "Robert Shwartzman"
}


def racefinder(date):
    response = urlopen('https://api.openf1.org/v1/sessions?date_start='+date)
    data = json.loads(response.read().decode('utf-8'))

    results = []

    for i in range(len(data)):
        date_start = datetime.strptime(
            data[i]['date_start'], "%Y-%m-%dT%H:%M:%S+00:00")
        date_end = datetime.strptime(
            data[i]['date_end'], "%Y-%m-%dT%H:%M:%S+00:00")

        # Convert to timestamps for the slider
        data[i]['start_timestamp'] = int(date_start.timestamp())
        data[i]['end_timestamp'] = int(date_end.timestamp())
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

    print('https://api.openf1.org/v1/car_data?driver_number=' +
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


def getsessiondata(date):
    datewindowbegin = datetime.fromisoformat(date) - timedelta(hours=3)
    formattedwindowbegin = datewindowbegin.strftime('%Y-%m-%dT%H:%M:%S.%f')
    datewindowend = datetime.fromisoformat(date) + timedelta(hours=3)
    formattedwindowend = datewindowend.strftime('%Y-%m-%dT%H:%M:%S.%f')

    response = urlopen(
        'https://api.openf1.org/v1/sessions?date_start>='+formattedwindowbegin+'&'+'date_start<='+formattedwindowend)

    print('https://api.openf1.org/v1/sessions?date_start>=' +
          formattedwindowbegin+'&'+'date_start<='+formattedwindowend)

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

    results = {}

    sessiondata = getsessiondata(date)

    results['race_start'] = findracestart(str(sessiondata['session_key']))

    date_format = "%Y-%m-%dT%H:%M:%S%z"
    date_format_with_microseconds = "%Y-%m-%dT%H:%M:%S.%f%z"

    def parse_datetime(date_str):
        # List of possible formats
        formats = [
            "%Y-%m-%dT%H:%M:%S.%f%z",  # With microseconds and timezone
            "%Y-%m-%dT%H:%M:%S%z",     # Without microseconds but with timezone
            "%Y-%m-%dT%H:%M:%S.%f",    # With microseconds
            "%Y-%m-%dT%H:%M:%S",       # Without microseconds or timezone
        ]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(
            f"Date string '{date_str}' does not match expected formats.")

    try:
        actual_start = parse_datetime(results['race_start'])
    except ValueError:
        actual_start = None  # Handle invalid case if necessary

    try:
        predicted_start = parse_datetime(sessiondata['date_start'])
    except ValueError:
        predicted_start = None  # Handle invalid case if necessary

    try:
        print(date)
        datereal = parse_datetime(date)
    except ValueError:
        datereal = None  # Handle invalid case if necessary

    if actual_start and predicted_start and datereal:
        time_diff = actual_start - predicted_start
        print(datereal)
        datereal = datereal + time_diff
        print(datereal)
        print(time_diff)
        # Format the final datetime without the timezone
        # Trims milliseconds to match typical ISO 8601 format
        date = datereal.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]

    results['datetime'] = date

    cardata = getcardata(driver_number, date)
    meetingdata = getmeetingdata(str(cardata['meeting_key']))
    driverdata = getdriverdata(driver_number)
    intervaldata = getintervaldata(driver_number, date)
    lapdata = getlapdata(driver_number, date)
    pitdata = getpitdata(driver_number, date)
    positiondata = getpositiondata(driver_number, date)
    stintdata = getstintdata(driver_number, str(cardata['session_key']))

    weather = getweather(date)

    print("Driver:", driverdata['full_name'])
    print("Number:", driverdata['driver_number'])
    print("Team:", driverdata['team_name'])

    alldata = [cardata, driverdata, intervaldata, lapdata, meetingdata,
               pitdata, positiondata, sessiondata, stintdata, weather]

    for data in alldata:
        results.update(data)

    return results


def poll_positions(date, race_start):
    datewindowbegin = datetime.fromisoformat(race_start) - timedelta(hours=2)

    formattedwindow = datewindowbegin.strftime('%Y-%m-%dT%H:%M:%S.%f')

    response = urlopen(
        'https://api.openf1.org/v1/position?&date>='+formattedwindow+'&date<='+date)
    print('https://api.openf1.org/v1/position?&date>=' +
          formattedwindow+'&date<='+date)
    data = json.loads(response.read().decode('utf-8'))

    positions = []
    seen_positions = set()

    for entry in reversed(data):
        position = entry["position"]

        if position not in seen_positions:
            positions.append(
                [entry['position'], driver_dict[int(entry['driver_number'])]])
            seen_positions.add(position)

    sorted_positions = sorted(positions, key=lambda x: x[0])

    return sorted_positions


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

    def fetch_and_store_driver_stats(self, driver_id):

        # Fetch driver statistics and store/update in the database."""
