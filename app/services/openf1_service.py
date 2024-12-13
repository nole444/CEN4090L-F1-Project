# app/services/openf1_service.py

from urllib.request import urlopen
import json
from datetime import datetime, timedelta
import random


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


def findracestart(session_key):
    """
    Fetches the race start time based on the session key.

    Parameters:
        session_key (int): Unique identifier for the session.

    Returns:
        str or None: Race start date-time in ISO format if found, else None.
    """
    try:
        url = f'https://api.openf1.org/v1/intervals?gap_to_leader<0.5&gap_to_leader>0&session_key={session_key}'
        response = urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        if isinstance(data, list) and data:
            return data[0].get('date')
        return None
    except Exception as e:
        print(f"Error in findracestart: {e}")
        return None


def poll_positions(race_start, current_time):
    """
    Fetches the real race positions from the API.

    Parameters:
        race_start (str): The race start date-time in ISO format.
        current_time (str): The current date-time in ISO format.

    Returns:
        list: Sorted list of real race results.
    """
    try:
        # Define the time window for fetching positions
        datewindowbegin = datetime.fromisoformat(race_start) - timedelta(hours=2)
        formattedwindow = datewindowbegin.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
        formatted_date = datetime.fromisoformat(current_time).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]

        # Fetch positions within the time window
        url = f'https://api.openf1.org/v1/position?date>={formattedwindow}&date<={formatted_date}'
        response = urlopen(url)
        data = json.loads(response.read().decode('utf-8'))

        # Handle response structure
        if isinstance(data, dict) and 'results' in data:
            data = data['results']

        positions = []
        seen_positions = set()

        for entry in reversed(data):
            position = entry.get("position")
            driver_number = int(entry.get("driver_number", 0))

            if position not in seen_positions and driver_number in driver_dict:
                driver_name = driver_dict[driver_number]
                race_time = entry.get("time", "N/A")  # Adjust based on actual API response
                positions.append({"position": position, "driver_name": driver_name, "time": race_time})
                seen_positions.add(position)

        # Sort positions based on the 'position' key
        sorted_positions = sorted(positions, key=lambda x: x["position"])

        return sorted_positions
    except Exception as e:
        print(f"Error in poll_positions: {e}")
        return []


def fetch_race_results(session_key):
    """
    Fetches all race results for a specific session.

    Parameters:
        session_key (int): Unique identifier for the session.

    Returns:
        list: List of race result entries.
    """
    try:
        url = f'https://api.openf1.org/v1/race-results?session_key={session_key}'
        response = urlopen(url)

        if response.getcode() != 200:
            print(f"Failed to fetch race results: HTTP {response.getcode()}")
            return []

        data = json.loads(response.read().decode('utf-8'))

        # Handle response structure
        if isinstance(data, dict) and 'results' in data:
            data = data['results']

        return data  # Assuming it's a list of race results

    except Exception as e:
        print(f"Error fetching race results: {e}")
        return []


def fetch_participating_drivers(session_key):
    """
    Fetches the list of participating drivers for a specific race session via the /drivers endpoint.
    """
    try:
        url = f'https://api.openf1.org/v1/drivers?session_key={session_key}'
        response = urlopen(url)
        if response.getcode() != 200:
            print(f"Failed to fetch drivers: HTTP {response.getcode()}")
            return []

        data = json.loads(response.read().decode('utf-8'))

        # Check the structure of `data`.
        # If it's a list, iterate through it and extract driver_number.
        participating_drivers = []
        for driver_entry in data:
            driver_number = driver_entry.get("driver_number")
            # Check if driver_number exists in your driver_dict
            if driver_number in driver_dict:
                participating_drivers.append(driver_number)

        return participating_drivers

    except Exception as e:
        print(f"Error fetching participating drivers: {e}")
        return []

def racefinder(date):
    """
    Fetches races occurring on the given date along with participating drivers and real-life results.

    Parameters:
        date (str): Date in 'YYYY-MM-DD' format.

    Returns:
        list: List of races with details including circuit information and participating drivers.
    """
    try:
        # Fetch sessions for the specific date
        url = f'https://api.openf1.org/v1/sessions?date_start={date}&date_end={date}'
        response = urlopen(url)

        # Check for successful response
        if response.getcode() != 200:
            print(f"Failed to fetch data: HTTP {response.getcode()}")
            return []

        data = json.loads(response.read().decode('utf-8'))
        print("API Response Data:", json.dumps(data, indent=4))  # Debugging Statement

    except Exception as e:
        print(f"Error fetching race data: {e}")
        return []

    results = []

    for session in data:
        try:
            # Debugging: Print the entire session data to inspect its structure
            print("Session Data:", json.dumps(session, indent=4))

            # Parse start and end dates
            date_start_str = session.get('date_start')
            date_end_str = session.get('date_end')

            if not date_start_str or not date_end_str:
                print("Missing date information in session.")
                continue

            # Parse dates with timezone
            try:
                date_start = datetime.strptime(date_start_str, "%Y-%m-%dT%H:%M:%S%z")
                date_end = datetime.strptime(date_end_str, "%Y-%m-%dT%H:%M:%S%z")
            except ValueError as ve:
                print(f"Error parsing dates: {ve}")
                continue

            # Extract circuit details
            circuit_key = session.get('circuit_key')
            circuit_name = session.get('circuit_short_name') or session.get('location') or 'Unknown Circuit'

            # Fetch participating drivers using 'session_key'
            session_key = session.get('session_key')
            if not session_key:
                print("Missing session key in session data.")
                continue

            participating_drivers = fetch_participating_drivers(session_key)

            if not participating_drivers:
                print("No participating drivers found for this race.")
                continue

            # Fetch real-life race results
            race_start = findracestart(session_key)
            if not race_start:
                print("No race start time found.")
                real_results = []
            else:
                real_results = poll_positions(race_start, race_start)  # Adjust parameters as needed

            race_details = {
                'circuit_details': {
                    'circuit_key': circuit_key,
                    'circuit_name': circuit_name
                },
                'participating_drivers': participating_drivers,
                'real_results': real_results
            }

            results.append(race_details)

        except Exception as e:
            print(f"Error processing session: {e}")
            continue

    return results

def getcardata(driver_number, date):
    try:
        datewindowbegin = datetime.fromisoformat(date) - timedelta(seconds=1)
        formattedwindow = datewindowbegin.strftime('%Y-%m-%dT%H:%M:%S.%f')
        response = urlopen(f'https://api.openf1.org/v1/car_data?driver_number={driver_number}&date>={formattedwindow}&date<={date}')
        data = json.loads(response.read().decode('utf-8'))
        return data[-1] if data else {}
    except Exception as e:
        print(f"Error in getcardata: {e}")
        return {}

def getintervaldata(driver_number, date):
    try:
        datewindowbegin = datetime.fromisoformat(date) - timedelta(minutes=5)
        formattedwindow = datewindowbegin.strftime('%Y-%m-%dT%H:%M:%S.%f')
        response = urlopen(f'https://api.openf1.org/v1/intervals?driver_number={driver_number}&date>={formattedwindow}&date<={date}')
        data = json.loads(response.read().decode('utf-8'))
        return data[-1] if data else {}
    except Exception as e:
        print(f"Error in getintervaldata: {e}")
        return {}

def getlapdata(driver_number, date):
    try:
        datewindowbegin = datetime.fromisoformat(date) - timedelta(hours=4)
        formattedwindow = datewindowbegin.strftime('%Y-%m-%dT%H:%M:%S.%f')
        response = urlopen(f'https://api.openf1.org/v1/laps?driver_number={driver_number}&date_start>={formattedwindow}&date_start<={date}')
        data = json.loads(response.read().decode('utf-8'))
        return data[-1] if data else {}
    except Exception as e:
        print(f"Error in getlapdata: {e}")
        return {}

def getdriverdata(driver_number):
    try:
        response = urlopen(f'https://api.openf1.org/v1/drivers?driver_number={driver_number}&session_key=latest')
        data = json.loads(response.read().decode('utf-8'))
        return data[0] if data else {}
    except Exception as e:
        print(f"Error in getdriverdata: {e}")
        return {}

def getmeetingdata(meeting_key):
    try:
        response = urlopen(f'https://api.openf1.org/v1/meetings?meeting_key={meeting_key}')
        data = json.loads(response.read().decode('utf-8'))
        return data[0] if data else {}
    except Exception as e:
        print(f"Error in getmeetingdata: {e}")
        return {}

def getsessiondata(date):
    try:
        datewindowbegin = datetime.fromisoformat(date) - timedelta(hours=3)
        formattedwindowbegin = datewindowbegin.strftime('%Y-%m-%dT%H:%M:%S.%f')
        datewindowend = datetime.fromisoformat(date) + timedelta(hours=3)
        formattedwindowend = datewindowend.strftime('%Y-%m-%dT%H:%M:%S.%f')
        response = urlopen(f'https://api.openf1.org/v1/sessions?date_start>={formattedwindowbegin}&date_start<={formattedwindowend}')
        data = json.loads(response.read().decode('utf-8'))
        return data[0] if data else {}
    except Exception as e:
        print(f"Error in getsessiondata: {e}")
        return {}

def getpitdata(driver_number, date):
    try:
        datewindowbegin = datetime.fromisoformat(date) - timedelta(hours=4)
        formattedwindow = datewindowbegin.strftime('%Y-%m-%dT%H:%M:%S.%f')
        response = urlopen(f'https://api.openf1.org/v1/laps?driver_number={driver_number}&date>={formattedwindow}&date<={date}')
        data = json.loads(response.read().decode('utf-8'))
        return data[-1] if data else {}
    except Exception as e:
        print(f"Error in getpitdata: {e}")
        return {}

def getpositiondata(driver_number, date):
    try:
        datewindowbegin = datetime.fromisoformat(date) - timedelta(hours=4)
        formattedwindow = datewindowbegin.strftime('%Y-%m-%dT%H:%M:%S.%f')
        response = urlopen(f'https://api.openf1.org/v1/position?driver_number={driver_number}&date>={formattedwindow}&date<={date}')
        data = json.loads(response.read().decode('utf-8'))
        return data[-1] if data else {}
    except Exception as e:
        print(f"Error in getpositiondata: {e}")
        return {}

def getstintdata(driver_number, session_key):
    try:
        response = urlopen(f'https://api.openf1.org/v1/stints?driver_number={driver_number}&session_key={session_key}')
        data = json.loads(response.read().decode('utf-8'))
        return data[-1] if data else {}
    except Exception as e:
        print(f"Error in getstintdata: {e}")
        return {}

def getweather(date):
    try:
        datewindowbegin = datetime.fromisoformat(date) - timedelta(minutes=3)
        formattedwindow = datewindowbegin.strftime('%Y-%m-%dT%H:%M:%S.%f')
        response = urlopen(f'https://api.openf1.org/v1/weather?&date>={formattedwindow}&date<={date}')
        data = json.loads(response.read().decode('utf-8'))
        return data[-1] if data else {}
    except Exception as e:
        print(f"Error in getweather: {e}")
        return {}

def getalldata(driver_number, date):
    """
    Fetches comprehensive data for a driver at a specific date and time.
    """
    results = {}
    sessiondata = getsessiondata(date)
    if not sessiondata:
        print("No session data found.")
        return results

    session_key = str(sessiondata.get('session_key', ''))
    if not session_key:
        print("No session key found.")
        return results

    race_start = findracestart(session_key)
    if not race_start:
        print("No race start data found.")
        return results

    # Adjust date based on race start
    try:
        actual_start = datetime.fromisoformat(race_start)
    except ValueError:
        actual_start = None

    try:
        predicted_start = datetime.fromisoformat(sessiondata.get('date_start', ''))
    except ValueError:
        predicted_start = None

    try:
        datereal = datetime.fromisoformat(date)
    except ValueError:
        datereal = None

    if actual_start and predicted_start and datereal:
        time_diff = actual_start - predicted_start
        datereal = datereal + time_diff
        date = datereal.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]

    results['datetime'] = date

    # Fetch all relevant data
    cardata = getcardata(driver_number, date)
    meetingdata = getmeetingdata(cardata.get('meeting_key', ''))
    driverdata = getdriverdata(driver_number)
    intervaldata = getintervaldata(driver_number, date)
    lapdata = getlapdata(driver_number, date)
    pitdata = getpitdata(driver_number, date)
    positiondata = getpositiondata(driver_number, date)
    stintdata = getstintdata(driver_number, session_key)
    weather = getweather(date)

    alldata = [cardata, driverdata, intervaldata, lapdata, meetingdata,
               pitdata, positiondata, sessiondata, stintdata, weather]

    for data_item in alldata:
        if isinstance(data_item, dict):
            results.update(data_item)

    return results



