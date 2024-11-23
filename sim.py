def simulate_race(strategy, tire_types, laps, pit_stop_time):
    current_lap = 0
    total_time = 0
    pit_count = 0
    wear_level = 0
    current_tire = strategy['start_tire']
    next_pit_lap = strategy['pit_laps'].pop(0) if strategy['pit_laps'] else laps

    while current_lap < laps:
        # pitstop check
        if current_lap == next_pit_lap:
            pit_count += 1
            total_time += pit_stop_time
            wear_level = 0  # Reset wear level after pit stop
            current_tire = strategy['next_tires'][pit_count - 1]  # Switch to the next tire
            next_pit_lap = strategy['pit_laps'].pop(0) if strategy['pit_laps'] else laps
        
        # Calculate lap time with current tire and wear level
        total_time += lap_time(current_tire, wear_level, tire_types)
        wear_level += 1
        current_lap += 1

    return total_time

def lap_time(tire_type, wear_level, tire_types):
    base_time = tire_types[tire_type]['base_lap_time']
    degradation = wear_level * tire_types[tire_type]['degradation_rate']
    return base_time + degradation

def display_menu():
    print("\n--- F1 Race Simulator ---")
    print("1. Choose Starting Tire")
    print("2. Select Strategy")
    print("3. Simulate Race")
    print("4. Compare Strategies")
    print("5. Exit")
    choice = int(input("Enter your choice: "))
    return choice

def main():
    # Race configuration
    laps = 56  # Race length based on COTA
    pit_stop_time = 22.3  # Time spent in the pit (lane + stop)

    # Tire properties
    tire_types = {
        'c5': {'base_lap_time': 94.7, 'degradation_rate': 0.17, 'wear_limit': 8},
        'c4': {'base_lap_time': 95, 'degradation_rate': 0.13, 'wear_limit': 12},
        'c3': {'base_lap_time': 95.1, 'degradation_rate': 0.10, 'wear_limit': 15},
        'c2': {'base_lap_time': 95.6, 'degradation_rate': 0.08, 'wear_limit': 20},
        'c1': {'base_lap_time': 96.0, 'degradation_rate': 0.05, 'wear_limit': 25},
    }

    # Strategy options
    strategies = [
        {'start_tire': 'c1', 'pit_laps': [20, 40], 'next_tires': ['c3', 'c4']},
        {'start_tire': 'c2', 'pit_laps': [25], 'next_tires': ['c3']},
        {'start_tire': 'c3', 'pit_laps': [15, 30, 45], 'next_tires': ['c4', 'c4', 'c5']},
    ]

    selected_tire = None
    selected_strategy = None

    while True:
        choice = display_menu()

        if choice == 1:
            print("\nAvailable Tires:")
            for tire in tire_types.keys():
                print(f"- {tire}")
            selected_tire = input("Enter the starting tire: ")
            if selected_tire not in tire_types:
                print("Invalid tire choice. Please try again.")
                selected_tire = None

        elif choice == 2:
            print("\nAvailable Strategies:")
            for i, strategy in enumerate(strategies):
                print(f"{i + 1}. Start Tire: {strategy['start_tire']}, Pit Laps: {strategy['pit_laps']}")
            strategy_index = int(input("Enter the strategy number: ")) - 1
            if 0 <= strategy_index < len(strategies):
                selected_strategy = strategies[strategy_index]
                selected_strategy['start_tire'] = selected_tire or selected_strategy['start_tire']
            else:
                print("Invalid strategy choice. Please try again.")

        elif choice == 3:
            if selected_strategy:
                total_time = simulate_race(selected_strategy.copy(), tire_types, laps, pit_stop_time)
                print(f"Race completed using the selected strategy. Total race time: {total_time:.2f} seconds")
            else:
                print("No strategy selected. Please select a strategy first.")

        elif choice == 4:
            print("\nComparing All Strategies:")
            for strategy in strategies:
                strategy['start_tire'] = selected_tire or strategy['start_tire']
                total_time = simulate_race(strategy.copy(), tire_types, laps, pit_stop_time)
                print(f"Strategy (Start Tire: {strategy['start_tire']}, Pit Laps: {strategy['pit_laps']}): Total Time = {total_time:.2f} seconds")

        elif choice == 5:
            print("Exiting the simulator. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
