import time
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from pythonosc import udp_client
from pythonosc import osc_message_builder

# OSC

def normalize_value(value, min_val, max_val):
    """Normalize a value to 0-1 range"""
    if value is None:
        return 0
    return max(0, min(1, (value - min_val) / (max_val - min_val)))

def send_osc_data(client, data: Dict[str, Dict[str, Any]], variables: List[str]):
    """Send normalized sensor data via OSC"""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")
    
    # Define value ranges for normalization
    ranges = {
        "pull": (0, 126),        # Pull pressure range
        "force": (0, 126),       # Force pressure range
        "trackpad_x": (0, 255),  # Trackpad X range
        "trackpad_y": (0, 255),  # Trackpad Y range
        "slider_value": (0, 126),# Slider range
        "battery_level": (0, 100),# Battery level range
        "proximity": (0, 126),   # Proximity sensor range
    }
    
    for var in variables:
        for hand in ['left', 'right']:
            if var in data[hand]:
                value = data[hand][var]
                osc_address = f"/{hand}/{var}"
                
                # Normalize different types of values
                if value is None:
                    formatted_value = 0
                elif isinstance(value, bool):
                    formatted_value = 1 if value else 0
                elif isinstance(value, (int, float)):
                    # Determine range for this variable
                    range_key = next((k for k in ranges.keys() if k in var), None)
                    if range_key:
                        min_val, max_val = ranges[range_key]
                        formatted_value = normalize_value(value, min_val, max_val)
                    else:
                        formatted_value = normalize_value(value, 0, 126)  # default range
                elif "Quaternion" in str(type(value)):
                    try:
                        quat_list = value.tolist()
                        # Quaternion values are already in normalized form (-1 to 1)
                        # Convert to 0-1 range
                        for i, q in enumerate(['w', 'x', 'y', 'z']):
                            normalized = (quat_list[i] + 1) / 2  # Convert from -1,1 to 0,1
                            client.send_message(f"{osc_address}/{q}", float(normalized))
                        continue
                    except:
                        formatted_value = 0
                elif isinstance(value, list):
                    # For IMU data (accel, gyro, mag)
                    try:
                        for i, component in enumerate(value):
                            if component is not None:
                                # Normalize based on typical IMU ranges
                                if "accel" in var:
                                    # Typical accelerometer range ±2g
                                    normalized = normalize_value(component, -2, 2)
                                elif "gyro" in var:
                                    # Typical gyroscope range ±250 deg/s
                                    normalized = normalize_value(component, -250, 250)
                                elif "mag" in var:
                                    # Typical magnetometer range ±4900 µT
                                    normalized = normalize_value(component, -4900, 4900)
                                else:
                                    normalized = normalize_value(component, -1, 1)
                                client.send_message(f"{osc_address}/{i}", float(normalized))
                        continue
                    except:
                        formatted_value = 0
                else:
                    formatted_value = 0
                
                client.send_message(osc_address, formatted_value)

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

def format_data_line(data: Dict[str, Dict[str, Any]], variables: List[str]) -> str:
    parts = []
    timestamp = datetime.now().strftime("%H:%M:%S.%f")
    parts.append(timestamp)
    
    for var in variables:
        #for hand in ['left', 'right']:
        for hand in ['right']:
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


if __name__ == "__main__":
    import sys
    from etee import EteeController
    
    # Initialize OSC client
    #osc_ip = "127.0.0.1"  # localhost
    osc_ip = "192.168.1.125"  # localhostquit
    osc_port = 8000       # Choose your desired port
    osc_client = udp_client.SimpleUDPClient(osc_ip, osc_port)
    
    # Initialize etee controller
    etee = EteeController()
    etee.connect()
    time.sleep(1)
    etee.start_data()
    etee.run()

    # Variables to monitor and send via OSC
    # variables_to_monitor = [
    #     "index_pull", "index_force",
    #     "thumb_pull", "thumb_force",
    #     "middle_pull", "middle_force",
    #     "ring_pull", "ring_force",
    #     "pinky_pull", "pinky_force",
    #     "trackpad_x", "trackpad_y",
    #     "quaternion"
    # ]

    variables_to_monitor = ["trackpad_x"]
    
    print(f"Sending OSC data to {osc_ip}:{osc_port}")
    print("OSC addresses format: /<hand>/<sensor>")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            if etee.get_number_available_etee_ports() > 0:
                data = process_all_data(etee)
                send_osc_data(osc_client, data, variables_to_monitor)
                print(format_data_line(data, variables_to_monitor))
                time.sleep(0.1)
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