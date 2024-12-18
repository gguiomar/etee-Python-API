import time
import sys
import keyboard
from datetime import datetime
from etee import EteeController

def print_finger_data(finger_data_list):
    """
    Prints minimal finger data for both hands side by side in a single line, with a timestamp.
    
    :param finger_data_list: List of dictionaries containing finger data for one hand.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
    
    # Loop through the finger data list and format it for each finger
    data_str = [f"{timestamp}"]
    for finger_data in finger_data_list:
        finger = finger_data['finger'][0].upper()  # Just the first letter for simplicity
        left_pull = f"L:{finger_data['left_pull']}"
        left_force = f"Lf:{finger_data['left_force']}"
        left_touched = "Lt" if finger_data['left_touched'] else ""
        left_clicked = "Lc" if finger_data['left_clicked'] else ""
        
        right_pull = f"R:{finger_data['right_pull']}"
        right_force = f"Rf:{finger_data['right_force']}"
        right_touched = "Rt" if finger_data['right_touched'] else ""
        right_clicked = "Rc" if finger_data['right_clicked'] else ""
        
        # Combine all the information for this finger
        finger_str = f"{finger} {left_pull} {left_force} {left_touched} {left_clicked} {right_pull} {right_force} {right_touched} {right_clicked}"
        data_str.append(finger_str)
    
    # Join all the data into a single line for output
    print(" | ".join(data_str))

def get_finger_data(etee, hand):
    """
    Retrieves all available data for all fingers for the specified hand.

    :param etee: The EteeController instance.
    :param hand: The hand to retrieve data for ("left" or "right").
    :return: A dictionary containing finger data.
    """
    try:
        finger_data = {
            "thumb": {
                "pull": etee.get_thumb_pull(hand) or 0,
                "force": etee.get_thumb_force(hand) or 0,
                "touched": etee.get_thumb_touched(hand) or False,
                "clicked": etee.get_thumb_clicked(hand) or False,
            },
            "index": {
                "pull": etee.get_index_pull(hand) or 0,
                "force": etee.get_index_force(hand) or 0,
                "touched": etee.get_index_touched(hand) or False,
                "clicked": etee.get_index_clicked(hand) or False,
            },
            "middle": {
                "pull": etee.get_middle_pull(hand) or 0,
                "force": etee.get_middle_force(hand) or 0,
                "touched": etee.get_middle_touched(hand) or False,
                "clicked": etee.get_middle_clicked(hand) or False,
            },
            "ring": {
                "pull": etee.get_ring_pull(hand) or 0,
                "force": etee.get_ring_force(hand) or 0,
                "touched": etee.get_ring_touched(hand) or False,
                "clicked": etee.get_ring_clicked(hand) or False,
            },
            "pinky": {
                "pull": etee.get_pinky_pull(hand) or 0,
                "force": etee.get_pinky_force(hand) or 0,
                "touched": etee.get_pinky_touched(hand) or False,
                "clicked": etee.get_pinky_clicked(hand) or False,
            }
        }
        return finger_data
    except Exception as e:
        return {"error": str(e)}

def print_finger_data(left_data, right_data):
    """
    Prints finger data for both hands side by side in a tabular format.

    :param left_data: The dictionary containing finger data for the left hand.
    :param right_data: The dictionary containing finger data for the right hand.
    """
    # Print header
    print(f"{'Finger':<10} | {'Left Hand':<35} | {'Right Hand':<35}")
    print("-" * 83)
    
    # Iterate over all fingers
    for finger in left_data.keys():
        left = left_data[finger]
        right = right_data[finger]
        print(f"{finger.capitalize():<10} | "
              f"Pull: {left['pull']:>3}, Force: {left['force']:>3}, "
              #f"Touched: {left['touched']:<5}, Clicked: {left['clicked']:<5} | "
              f"Pull: {right['pull']:>3}, Force: {right['force']:>3}, "
              #f"Touched: {right['touched']:<5}, Clicked: {right['clicked']:<5}"
              )

if __name__ == "__main__":
    # Initialize the etee driver and find dongle
    etee = EteeController()
    num_dongles_available = etee.get_number_available_etee_ports()
    etee.connect()     # Attempt connection to etee dongle
    time.sleep(1)
    etee.start_data()  # Attempt to send a command to etee controllers to start data stream
    etee.run()         # Start data loop

    # If dongle is connected, continuously print data for both hands
    while True:
        # Check if 'Esc' key is pressed
        if keyboard.is_pressed('Esc'):
            print("\n'Esc' key was pressed. Exiting application...")
            etee.stop_data()  # Stop controller data stream
            print("Controller data stream stopped.")
            etee.stop()  # Stop data loop
            print("Data loop stopped.")
            time.sleep(0.05)
            sys.exit(0)  # Exit driver

        # Continue printing controller data
        else:
            current_time = datetime.now().strftime("%H:%M:%S.%f")
            print(f"\n{current_time} - Retrieving data...")

            left_data = get_finger_data(etee, "left")
            right_data = get_finger_data(etee, "right")
            print("Left Data:", type(left_data), left_data)
            print("Right Data:", type(right_data), right_data)

            time.sleep(0.05)  # Add a short delay between updates