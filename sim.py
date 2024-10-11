def simulate_race(strategy, tire_types, laps, pit_stop_time,):
    current_lap = 0
    total_time = 0
    pit_count = 0
    wear_level = 0
    current_tire = strategy['start_tire']
    next_pit_lap = strategy['pit_laps'].pop(0) if strategy['pit_laps'] else laps

    while current_lap < laps:
        # Check if it's time for a pit stop
        if current_lap == next_pit_lap:
            pit_count += 1
            total_time += pit_stop_time
            wear_level = 0  # Reset wear level after pit stop
            current_tire = 'medium'  # Example: switching to medium tires after pit
            next_pit_lap = strategy['pit_laps'].pop(0) if strategy['pit_laps'] else laps
        
        # Calculate lap time with current tire and wear level
        total_time += lap_time(current_tire, wear_level, tire_types)
        wear_level += 1  # Increase wear level for next lap
        current_lap += 1

    return total_time

def pit_stop_time(pit_count, pit_stop_time):
    return pit_count * pit_stop_time

def lap_time(tire_type, wear_level, tire_types):
    base_time = tire_types[tire_type]['base_lap_time']
    degradation = wear_level * tire_types[tire_type]['degradation_rate']
    return base_time + degradation

def main():
    # Race configuration
    laps = 56 #race and lap distance based on COTA
    lap_distance = 5.514
    race_distance = laps * lap_distance

    # Tire properties
    tire_types = {
        'c5': {
            'base_lap_time': 94.7,
            'degradation_rate': 0.17,
            'wear_limit': 8
        },
        'c4': {
            'base_lap_time': 95,
            'degradation_rate': 0.13,
            'wear_limit': 12
        },
        'c3': {
            'base_lap_time': 95.1,
            'degradation_rate': 0.10,
            'wear_limit': 15
        },
        'c2': {
            'base_lap_time': 90,
            'degradation_rate': 0.08,
            'wear_limit': 20
        },
        'c1': {
            'base_lap_time': 95.6,
            'degradation_rate': 0.05,
            'wear_limit': 25
        },
        'inter': {
            'base_lap_time': 95.9,
            'degradation_rate': 0.04,
            'wear_limit': 20
        },
        'wet': {
            'base_lap_time': 99,
            'degradation_rate': 0.04,
            'wear_limit': 20
        },
    }
    

    # Pit stop time
    time_in_pit_lane = 20  # Time in seconds spent driving through the pit lane - not including the stop itself
    time_stopped = 2.3 # Time spent actually stopped. Will have some variation

    # Strategy options (example)
    strategies = [
        {'start_tire': 'c1', 'pit_laps': [15, 30]},  # This is an example - need to figure out if we want fixed strategy choices or if we want to keep it open
    ]

if __name__ == "__main__":
    main()
