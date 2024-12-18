import time
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional

def process_finger_data(etee, hand: str, finger: str) -> Dict[str, Any]:
    """Process all data for a specific finger"""
    return {
        f"{finger}_pull": getattr(etee, f"get_{finger}_pull")(hand),
        f"{finger}_force": getattr(etee, f"get_{finger}_force")(hand),
        f"{finger}_touched": getattr(etee, f"get_{finger}_touched")(hand),
        f"{finger}_clicked": getattr(etee, f"get_{finger}_clicked")(hand)
    }

def process_trackpad_data(etee, hand: str) -> Dict[str, Any]:
    """Process all trackpad-related data"""
    return {
        "trackpad_x": etee.get_trackpad_x(hand),
        "trackpad_y": etee.get_trackpad_y(hand),
        "trackpad_pull": etee.get_trackpad_pull(hand),
        "trackpad_force": etee.get_trackpad_force(hand),
        "trackpad_touched": etee.get_trackpad_touched(hand),
        "trackpad_clicked": etee.get_trackpad_clicked(hand)
    }

def process_slider_data(etee, hand: str) -> Dict[str, Any]:
    """Process all slider-related data"""
    return {
        "slider_value": etee.get_slider_value(hand),
        "slider_touched": etee.get_slider_touched(hand),
        "slider_up": etee.get_slider_up_button(hand),
        "slider_down": etee.get_slider_down_button(hand)
    }

def process_gesture_data(etee, hand: str) -> Dict[str, Any]:
    """Process all gesture-related data"""
    return {
        "grip_pull": etee.get_grip_pull(hand),
        "grip_force": etee.get_grip_force(hand),
        "grip_touched": etee.get_grip_touched(hand),
        "grip_clicked": etee.get_grip_clicked(hand),
        "pinch_trackpad_pull": etee.get_pinch_trackpad_pull(hand),
        "pinch_trackpad_clicked": etee.get_pinch_trackpad_clicked(hand),
        "pinch_thumbfinger_pull": etee.get_pinch_thumbfinger_pull(hand),
        "pinch_thumbfinger_clicked": etee.get_pinch_thumbfinger_clicked(hand),
        "point_independent_clicked": etee.get_point_independent_clicked(hand),
        "point_excl_tp_clicked": etee.get_point_excl_tp_clicked(hand)
    }

def process_imu_data(etee, hand: str) -> Dict[str, Any]:
    """Process all IMU-related data"""
    return {
        "quaternion": etee.get_quaternion(hand),
        "euler": etee.get_euler(hand),
        "accel": etee.get_accel(hand),
        "gyro": etee.get_gyro(hand),
        "mag": etee.get_mag(hand)
    }

def process_system_data(etee, hand: str) -> Dict[str, Any]:
    """Process all system-related data"""
    return {
        "battery_level": etee.get_battery_level(hand),
        "charging": etee.get_charging_in_progress_status(hand),
        "charging_complete": etee.get_charging_complete_status(hand),
        "system_button": etee.get_system_button_pressed(hand),
        "tracker_connected": etee.get_tracker_connection(hand),
        "proximity": etee.get_proximity(hand),
        "proximity_touched": etee.get_proximity_touched(hand),
        "proximity_clicked": etee.get_proximity_clicked(hand)
    }

def process_all_data(etee, selected_inputs: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
    """
    Process all or selected etee controller data.
    
    Args:
        etee: EteeController instance
        selected_inputs: Optional list of data categories to process. 
                        Options: ['fingers', 'trackpad', 'slider', 'gestures', 'imu', 'system']
                        If None, processes all data.
    
    Returns:
        Dictionary containing all processed data for both hands
    """
    all_categories = {
        'fingers': ['thumb', 'index', 'middle', 'ring', 'pinky'],
        'trackpad': [process_trackpad_data],
        'slider': [process_slider_data],
        'gestures': [process_gesture_data],
        'imu': [process_imu_data],
        'system': [process_system_data]
    }
    
    if selected_inputs is None:
        selected_inputs = list(all_categories.keys())
        
    data = {'left': {}, 'right': {}}
    
    for hand in ['left', 'right']:
        for category in selected_inputs:
            if category == 'fingers':
                for finger in all_categories['fingers']:
                    data[hand].update(process_finger_data(etee, hand, finger))
            else:
                for processor in all_categories[category]:
                    data[hand].update(processor(etee, hand))
    
    return data

import time
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional

def process_finger_data(etee, hand: str, finger: str) -> Dict[str, Any]:
    """Process all data for a specific finger"""
    return {
        f"{finger}_pull": getattr(etee, f"get_{finger}_pull")(hand),
        f"{finger}_force": getattr(etee, f"get_{finger}_force")(hand),
        f"{finger}_touched": getattr(etee, f"get_{finger}_touched")(hand),
        f"{finger}_clicked": getattr(etee, f"get_{finger}_clicked")(hand)
    }

def process_trackpad_data(etee, hand: str) -> Dict[str, Any]:
    """Process all trackpad-related data"""
    return {
        "trackpad_x": etee.get_trackpad_x(hand),
        "trackpad_y": etee.get_trackpad_y(hand),
        "trackpad_pull": etee.get_trackpad_pull(hand),
        "trackpad_force": etee.get_trackpad_force(hand),
        "trackpad_touched": etee.get_trackpad_touched(hand),
        "trackpad_clicked": etee.get_trackpad_clicked(hand)
    }

def process_slider_data(etee, hand: str) -> Dict[str, Any]:
    """Process all slider-related data"""
    return {
        "slider_value": etee.get_slider_value(hand),
        "slider_touched": etee.get_slider_touched(hand),
        "slider_up": etee.get_slider_up_button(hand),
        "slider_down": etee.get_slider_down_button(hand)
    }

def process_gesture_data(etee, hand: str) -> Dict[str, Any]:
    """Process all gesture-related data"""
    return {
        "grip_pull": etee.get_grip_pull(hand),
        "grip_force": etee.get_grip_force(hand),
        "grip_touched": etee.get_grip_touched(hand),
        "grip_clicked": etee.get_grip_clicked(hand),
        "pinch_trackpad_pull": etee.get_pinch_trackpad_pull(hand),
        "pinch_trackpad_clicked": etee.get_pinch_trackpad_clicked(hand),
        "pinch_thumbfinger_pull": etee.get_pinch_thumbfinger_pull(hand),
        "pinch_thumbfinger_clicked": etee.get_pinch_thumbfinger_clicked(hand),
        "point_independent_clicked": etee.get_point_independent_clicked(hand),
        "point_excl_tp_clicked": etee.get_point_excl_tp_clicked(hand)
    }

def process_imu_data(etee, hand: str) -> Dict[str, Any]:
    """Process all IMU-related data"""
    return {
        "quaternion": etee.get_quaternion(hand),
        "euler": etee.get_euler(hand),
        "accel": etee.get_accel(hand),
        "gyro": etee.get_gyro(hand),
        "mag": etee.get_mag(hand)
    }

def process_system_data(etee, hand: str) -> Dict[str, Any]:
    """Process all system-related data"""
    return {
        "battery_level": etee.get_battery_level(hand),
        "charging": etee.get_charging_in_progress_status(hand),
        "charging_complete": etee.get_charging_complete_status(hand),
        "system_button": etee.get_system_button_pressed(hand),
        "tracker_connected": etee.get_tracker_connection(hand),
        "proximity": etee.get_proximity(hand),
        "proximity_touched": etee.get_proximity_touched(hand),
        "proximity_clicked": etee.get_proximity_clicked(hand)
    }

def format_data_line(data: Dict[str, Dict[str, Any]], variables: List[str]) -> str:
    parts = []
    timestamp = datetime.now().strftime("%H:%M:%S.%f")
    parts.append(timestamp)
    
    for var in variables:
        for hand in ['left', 'right']:
            if var in data[hand]:
                value = data[hand][var]
                # Handle different types of values
                if value is None:
                    formatted_value = "---"
                elif isinstance(value, bool):
                    formatted_value = "1" if value else "0"
                elif isinstance(value, (int, float)):
                    formatted_value = f"{value:>3}"
                elif "Quaternion" in str(type(value)):  # Check if it's a Quaternion object
                    quat_list = value.tolist()
                    formatted_value = f"[{quat_list[0]:>6.3f},{quat_list[1]:>6.3f},{quat_list[2]:>6.3f},{quat_list[3]:>6.3f}]"
                elif isinstance(value, list):  # For other IMU data
                    formatted_value = "[" + ",".join(f"{x:>5.2f}" if x is not None else "---" for x in value) + "]"
                else:
                    formatted_value = str(value)
                
                parts.append(f"{hand[0].upper()}_{var}:{formatted_value}")
    
    return " | ".join(parts)

# Example usage:
if __name__ == "__main__":
    import sys
    from etee import EteeController
    
    etee = EteeController()
    etee.connect()
    time.sleep(1)
    etee.start_data()
    etee.run()
    
    # Example of selecting specific variables to monitor
    # variables_to_monitor = [
    #     "index_pull", "index_force",
    #     "thumb_pull", "thumb_force",
    #     "middle_pull", "middle_force",
    #     "ring_pull", "ring_force",
    #     "pinky_pull", "pinky_force",
    #     "trackpad_x", "trackpad_y"
    # ]
    variables_to_monitor = ["quaternion"]
    
    try:
        while True:
            if etee.get_number_available_etee_ports() > 0:
                data = process_all_data(etee)
                print(format_data_line(data, variables_to_monitor))
                time.sleep(0.05)
            else:
                print("Dongle disconnected. Please reconnect and restart.")
                etee.stop_data()
                etee.stop()
                sys.exit(1)
                
    except KeyboardInterrupt:
        print("\nStopping data collection...")
        etee.stop_data()
        etee.stop()
        sys.exit(0)

# Example usage:
if __name__ == "__main__":
    import sys
    from etee import EteeController
    
    etee = EteeController()
    etee.connect()
    time.sleep(1)
    etee.start_data()
    etee.run()

    variables_to_monitor = [
        "index_pull", "index_force",
        "thumb_pull", "thumb_force",
        "middle_pull", "middle_force",
        "ring_pull", "ring_force",
        "pinky_pull", "pinky_force",
        "trackpad_x", "trackpad_y",
        "quaternion"
    ]
    #variables_to_monitor = ["quaternion"]
    
    try:
        while True:
            if etee.get_number_available_etee_ports() > 0:
                data = process_all_data(etee)
                print(format_data_line(data, variables_to_monitor))
                time.sleep(0.05)
            else:
                print("Dongle disconnected. Please reconnect and restart.")
                etee.stop_data()
                etee.stop()
                sys.exit(1)
                
    except KeyboardInterrupt:
        print("\nStopping data collection...")
        etee.stop_data()
        etee.stop()
        sys.exit(0)