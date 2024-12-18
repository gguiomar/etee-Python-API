import time
from datetime import datetime
from typing import Dict, List, Any, Tuple

def process_sensor(etee, hand: str, sensor: str) -> Tuple[int, int]:
    """
    Process pull and force data for a given sensor
    Returns: (pull_value, force_value)
    """
    pull = getattr(etee, f"get_{sensor}_pull")(hand)
    force = getattr(etee, f"get_{sensor}_force")(hand)
    return pull, force

def process_all_sensors(etee, sensors: List[str]) -> Dict[str, Dict[str, Tuple[int, int]]]:
    """
    Process multiple sensors for both hands
    """
    data = {'left': {}, 'right': {}}
    for hand in ['left', 'right']:
        for sensor in sensors:
            pull, force = process_sensor(etee, hand, sensor)
            data[hand][sensor] = (pull, force)
    return data

def format_data_line(data: Dict[str, Dict[str, Tuple[int, int]]]) -> str:
    """Format sensor data into a single line with timestamp"""
    parts = [datetime.now().strftime("%H:%M:%S.%f")]
    
    for hand in ['left', 'right']:
        for sensor, (pull, force) in data[hand].items():
            pull_str = str(pull) if pull is not None else "---"
            force_str = str(force) if force is not None else "---"
            parts.append(f"{hand[0].upper()}:{sensor} pull={pull_str:>3} force={force_str:>3}")
    
    return " | ".join(parts)

if __name__ == "__main__":
    import sys
    from etee import EteeController
    
    # Initialize the etee driver and find dongle
    etee = EteeController()
    num_dongles_available = etee.get_number_available_etee_ports()
    
    if num_dongles_available > 0:
        etee.connect()     # Attempt connection to etee dongle
        time.sleep(1)
        etee.start_data()  # Attempt to send a command to etee controllers to start data stream
        etee.run()         # Start data loop
        
        # List of sensors to monitor
        sensors_to_monitor = ['index', 'thumb', 'middle', 'ring', 'pinky']
        
        try:
            while True:
                if etee.get_number_available_etee_ports() > 0:
                    data = process_all_sensors(etee, sensors_to_monitor)
                    print(format_data_line(data))
                    time.sleep(0.05)
                else:
                    print("---")
                    print("Dongle disconnected. Please reconnect and restart.")
                    etee.stop_data()
                    etee.stop()
                    sys.exit(1)
                    
        except KeyboardInterrupt:
            print("\nStopping data collection...")
            etee.stop_data()
            etee.stop()
            sys.exit(0)
    else:
        print("No dongle found. Please insert an etee dongle and restart.")
        sys.exit(1)