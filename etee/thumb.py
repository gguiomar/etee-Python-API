import time
import sys
import keyboard
from datetime import datetime
from etee import EteeController

def print_thumb_data(left_force, right_force):
    """
    Prints the force data for the thumbs of both hands in a single line, with a timestamp.
    
    :param left_force: The force data for the left thumb.
    :param right_force: The force data for the right thumb.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
    
    # Print the timestamp followed by the thumb force data for both hands
    print(f"{timestamp} | Lf:{left_force} | Rf:{right_force}")


def get_thumb_data(etee, hand):
    """
    Retrieves the thumb force data for the specified hand.

    :param etee: The EteeController instance.
    :param hand: The hand to retrieve data for ("left" or "right").
    :return: The thumb force value.
    """
    try:
        thumb_force = etee.get_thumb_force(hand) or 0
        return thumb_force
    except Exception as e:
        return {"error": str(e)}

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

    # If dongle is connected, continuously print thumb data force for both hands
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

        # Continue printing thumb force data
        else:
            current_time = datetime.now().strftime("%H:%M:%S.%f")
            print(f"\n{current_time} - Retrieving thumb data...")

            # Retrieve thumb data for both hands
            left_thumb_force = get_thumb_data(etee, "left")
            right_thumb_force = get_thumb_data(etee, "right")
            
            # Print the thumb data force for both hands
            print_thumb_data(left_thumb_force, right_thumb_force)

            time.sleep(0.05)  # Add a short delay between updates