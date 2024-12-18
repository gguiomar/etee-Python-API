import time
import sys
import keyboard
from datetime import datetime
from etee import EteeController

def print_finger_data(finger_data_list):
    """
    Prints minimal finger data for both hands side by side in a single line, with a timestamp.
    
    :param finger_data_list: List of dictionaries containing finger data for both hands.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
    
    # Start the data string with timestamp
    data_str = [f"{timestamp}"]

    # Loop through the finger data list and format it for each finger
    for finger_data in finger_data_list:
        finger = finger_data['finger'][0].upper()  # Just the first letter for simplicity
        
        # Collect minimal left and right hand data for each finger
        left_pull = f"L:{finger_data['left_pull']}"
        left_force = f"Lf:{finger_data['left_force']}"
        left_touched = "Lt" if finger_data['left_touched'] else ""
        left_clicked = "Lc" if finger_data['left_clicked'] else ""
        
        right_pull = f"R:{finger_data['right_pull']}"
        right_force = f"Rf:{finger_data['right_force']}"
        right_touched = "Rt" if finger_data['right_touched'] else ""
        right_clicked = "Rc" if finger_data['right_clicked'] else ""
        
        # Combine all the information for this finger
        #finger_str = f"{finger} {left_pull} {left_force} {left_touched} {left_clicked} {right_pull} {right_force} {right_touched} {right_clicked}"
        finger_str = f"{left_force} {right_force}"
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

def print_finger_data_side_by_side(left_data, right_data):
    """
    Prints the finger data for both hands side by side in a single line with minimal formatting.

    :param left_data: The dictionary containing finger data for the left hand.
    :param right_data: The dictionary containing finger data for the right hand.
    """
    # Create a list to store the data for printing
    finger_data_list = []

    for finger in left_data.keys():
        finger_data = {
            "finger": finger,
            "left_pull": left_data[finger]["pull"],
            "left_force": left_data[finger]["force"],
            "left_touched": left_data[finger]["touched"],
            "left_clicked": left_data[finger]["clicked"],
            "right_pull": right_data[finger]["pull"],
            "right_force": right_data[finger]["force"],
            "right_touched": right_data[finger]["touched"],
            "right_clicked": right_data[finger]["clicked"],
        }
        finger_data_list.append(finger_data)

    # Print the minimal finger data
    print_finger_data(finger_data_list)

if __name__ == "__main__":
    # Initialize the etee driver and find dongle
    etee = EteeController()
    num_dongles_available = etee.get_number_available_etee_ports()
    if num_dongles_available > 0:
        etee.connect()     # Attempt connection to etee dongle
        time.sleep(1)
        etee.start_data()  # Attempt to send a command to etee controllers to start data stream
        etee.run()         # Start data loop
    else:
        print("---")
        print("No dongle found. Please, insert an etee dongle and re-run the application.")
        sys.exit("Exiting application...")

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
            
            # Print the left and right hand data side by side
            print_finger_data_side_by_side(left_data, right_data)

            time.sleep(0.05)  # Add a short delay between updates