import random


def display_strategy_comparison(selected_driver_name, laps, strategies, tire_types, selected_strategy_time, pit_stop_time):
    print(f"\n--- Strategy Comparison for {selected_driver_name} ---")
    results = []
    for strategy in strategies:
        strategy_copy = strategy.copy()
        total_time, fastest_lap = simulate_race(selected_driver_name, strategy_copy, laps, tire_types, pit_stop_time)
        time_diff = total_time - selected_strategy_time
        time_diff_percentage = (time_diff / selected_strategy_time) * 100
        strategy_desc = f"Start Tire: {strategy['start_tire']}, Pit Laps: {strategy['pit_laps']}, Onto: {strategy['next_tires']}"
        results.append({
            "strategy": strategy_desc,
            "total_time": total_time,
            "time_diff": time_diff,
            "time_diff_percentage": time_diff_percentage
        })

    results.sort(key=lambda x: x["total_time"])

    for idx, result in enumerate(results, start=1):
        print(f"{idx}. {result['strategy']} | Total Time: {result['total_time']:.3f}s | "
              f"Time Diff: {result['time_diff']:+.3f}s ({result['time_diff_percentage']:+.2f}%)")


def display_timing_board(cars):
    timingBoard = []
    print("\n--- Timing Board ---")
    print(f"{'Position':<10}{'Car':<10}{'Driver':<15}{'Pit Stops':<12}{'Fastest Lap':<15}{'Total Race Time':<20}")
    cars.sort(key=lambda x: x['time'])
    for position, car in enumerate(cars, start=1):
        total_time_str = f"{car['time']:.3f}s"
        fastest_lap_str = f"{car['fastest_lap']:.3f}s"
        print(f"{position:<10}{car['car_id']:<10}{car['driver_name']:<15}{car['pit_stops']:<12}{fastest_lap_str:<15}{total_time_str:<20}")

        timingBoard.append({
            "position": position,
            "car_id": car['car_id'],
            "driver_name": car['driver_name'],
            "pit_stops": car['pit_stops'],
            "fastest_lap": car['fastest_lap'],
            "total_time": car['time']
        })

    return timingBoard

def simulate_race(driver, strategy, laps, tire_types, pit_stop_time=22):
    current_tire = strategy['start_tire']
    pit_laps = strategy['pit_laps'][:]
    next_tires = strategy['next_tires'][:]
    total_time = 0
    fastest_lap = float('inf')
    wear_level = 0

    for lap in range(1, laps + 1):
        # Pit stop logic
        if pit_laps and lap == pit_laps[0]:
            pit_laps.pop(0)
            total_time += pit_stop_time
            wear_level = 0
            if next_tires:
                current_tire = next_tires.pop(0)

        # Lap time calculation with random variation
        base_lap_time = tire_types[current_tire]['base_lap_time']
        degradation = wear_level * tire_types[current_tire]['degradation_rate']
        variation = random.uniform(-0.5, 0.5)
        lap_time = base_lap_time + degradation + variation

        fastest_lap = min(fastest_lap, lap_time)
        total_time += lap_time
        wear_level += 1

    return total_time, fastest_lap

def simEngine(APIdata, strat_select, grid):
    results = {}

    driver_dict = {
        1: "Max Verstappen", 10: "Pierre Gasly", 11: "Sergio Pérez", 14: "Fernando Alonso",
        16: "Charles Leclerc", 18: "Lance Stroll", 2: "Logan Sargeant", 20: "Kevin Magnussen",
        22: "Yuki Tsunoda", 23: "Alexander Albon", 24: "Zhou Guanyu", 27: "Nico Hülkenberg",
        3: "Daniel Ricciardo", 31: "Esteban Ocon", 37: "Isack Hadjar", 50: "Oliver Bearman",
        4: "Lando Norris", 40: "Ayumu Iwasa", 44: "Lewis Hamilton", 43: "Franco Colapinto",
        55: "Carlos Sainz", 61: "Jack Doohan", 63: "George Russell", 77: "Valtteri Bottas",
        81: "Oscar Piastri", 97: "Robert Shwartzman", 30: "Liam Lawson"
    }

    track_dict = [
        {"circuit_key": 63,"track_name": "Bahrain International Circuit", "track_length_miles": 3.363, "number_of_laps": 57},
        {"circuit_key": 149,"track_name": "Jeddah Corniche Circuit", "track_length_miles": 3.836, "number_of_laps": 50},
        {"circuit_key": 10,"track_name": "Albert Park Circuit", "track_length_miles": 3.295, "number_of_laps": 58},
        {"circuit_key": 46,"track_name": "Suzuka International Racing Course", "track_length_miles": 3.609, "number_of_laps": 53},
        {"circuit_key": 49,"track_name": "Shanghai International Circuit", "track_length_miles": 3.388, "number_of_laps": 56},
        {"circuit_key": 151,"track_name": "Miami International Autodrome", "track_length_miles": 3.362, "number_of_laps": 57},
        {"circuit_key": 6,"track_name": "Autodromo Enzo e Dino Ferrari (Imola)", "track_length_miles": 3.050, "number_of_laps": 63},
        {"circuit_key": 22,"track_name": "Circuit de Monaco", "track_length_miles": 2.074, "number_of_laps": 78},
        {"circuit_key": 23,"track_name": "Circuit Gilles Villeneuve", "track_length_miles": 2.710, "number_of_laps": 70},
        {"circuit_key": 23,"track_name": "Circuit de Barcelona-Catalunya", "track_length_miles": 2.892, "number_of_laps": 66},
        {"circuit_key": 19,"track_name": "Red Bull Ring", "track_length_miles": 2.683, "number_of_laps": 71},
        {"circuit_key": 2,"track_name": "Silverstone Circuit", "track_length_miles": 3.661, "number_of_laps": 52},
        {"circuit_key": 4,"track_name": "Hungaroring", "track_length_miles": 2.722, "number_of_laps": 70},
        {"circuit_key": 7,"track_name": "Circuit de Spa-Francorchamps", "track_length_miles": 4.352, "number_of_laps": 44},
        {"circuit_key": 55,"track_name": "Circuit Zandvoort", "track_length_miles": 2.647, "number_of_laps": 72},
        {"circuit_key": 39,"track_name": "Autodromo Nazionale Monza", "track_length_miles": 3.600, "number_of_laps": 53},
        {"circuit_key": 144,"track_name": "Baku City Circuit", "track_length_miles": 3.730, "number_of_laps": 51},
        {"circuit_key": 61,"track_name": "Marina Bay Street Circuit", "track_length_miles": 3.146, "number_of_laps": 61},
        {"circuit_key": 9,"track_name": "Circuit of the Americas", "track_length_miles": 3.426, "number_of_laps": 56},
        {"circuit_key": 65,"track_name": "Autódromo Hermanos Rodríguez", "track_length_miles": 2.674, "number_of_laps": 71},
        {"circuit_key": 14,"track_name": "Interlagos Circuit", "track_length_miles": 2.677, "number_of_laps": 71},
        {"circuit_key": 152,"track_name": "Las Vegas Strip Circuit", "track_length_miles": 3.852, "number_of_laps": 50},
        {"circuit_key": 150,"track_name": "Lusail International Circuit", "track_length_miles": 3.367, "number_of_laps": 57},
        {"circuit_key": 70,"track_name": "Yas Marina Circuit", "track_length_miles": 3.281, "number_of_laps": 58}
    ]

    tire_types = {
        'soft': {'base_lap_time': 95, 'degradation_rate': 0.17, 'wear_limit': 12},
        'medium': {'base_lap_time': 95.8, 'degradation_rate': 0.10, 'wear_limit': 20},
        'hard': {'base_lap_time': 96.8, 'degradation_rate': 0.07, 'wear_limit': 35},
    }

    strategies = [
        {'start_tire': 'soft', 'pit_laps': [20, 40], 'next_tires': ['medium', 'hard']},
        {'start_tire': 'soft', 'pit_laps': [20], 'next_tires': ['hard']},
        {'start_tire': 'soft', 'pit_laps': [15, 45], 'next_tires': ['hard', 'hard',]},
        {'start_tire': 'medium', 'pit_laps': [25], 'next_tires': ['hard']},
        {'start_tire': 'medium', 'pit_laps': [20, 50], 'next_tires': ['hard', 'soft']},
        {'start_tire': 'hard', 'pit_laps': [30, 47], 'next_tires': ['medium', 'medium']},
        
    ]

    selected_driver_id = APIdata['driver_number']
    selected_driver_name = driver_dict[APIdata['driver_number']]

    selected_track = next((track for track in track_dict if track["circuit_key"] == APIdata['circuit_key']), None)
    if not selected_track:
        raise ValueError(f"Track with circuit key {APIdata['circuit_key']} not found!")
    laps = selected_track['number_of_laps']

    print(f"You selected {selected_track['track_name']} ({laps} laps).\n")

    cars = []
    selected_driver_result = None

    for position, car_id in enumerate(grid):
        driver_name = driver_dict[grid[position]]
        #timing_offset = position * .5
        position += 1
        if car_id == selected_driver_id:

            strategy = strategies[strat_select - 1]
        else:
            strategy = random.choice(strategies)

        total_time, fastest_lap = simulate_race(driver_name, strategy, laps, tire_types)
        car_data = {
            "car_id": car_id,
            "driver_name": driver_name,
            "pit_stops": len(strategy['pit_laps']),
            "fastest_lap": fastest_lap,
            "time": total_time
        }
        if car_id == selected_driver_id:
            car_data["strategy"] = strategy
            selected_driver_result = car_data
        cars.append(car_data)

    #print(f"Debug: Selected Driver Result - {selected_driver_result}")
    
    results = display_timing_board(cars)

    simulated_strategies = {}
    optimal_time = float('inf')

    for strategy in strategies:
        strategy_key = str(strategy)
        if strategy_key not in simulated_strategies:
            # Simulate the race for this strategy if not already done
            total_time, _ = simulate_race(selected_driver_result['driver_name'], strategy, laps, tire_types)
            #print(f"{total_time}")
            simulated_strategies[strategy_key] = total_time
        else:
            total_time = simulated_strategies[strategy_key]
    
        optimal_time = min(optimal_time, total_time)

    # Calculate chosen strategy's accuracy
    chosen_time = selected_driver_result['time']
    accuracy = (optimal_time / chosen_time) * 100

    return{
        "timing_board": results,
        "strategy_accuracy": accuracy
    }