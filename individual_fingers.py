import time
import sys
import keyboard
from datetime import datetime
from etee import EteeController

# Process functions for each finger
def process_right_thumb():
    right_thumb_pull = etee.get_thumb_pull('right')
    right_thumb_force = etee.get_thumb_force('right')
    return right_thumb_pull, right_thumb_force

def process_left_thumb():
    left_thumb_pull = etee.get_thumb_pull('left')
    left_thumb_force = etee.get_thumb_force('left')
    return left_thumb_pull, left_thumb_force

def process_right_index():
    right_index_pull = etee.get_index_pull('right')
    right_index_force = etee.get_index_force('right')
    return right_index_pull, right_index_force

def process_left_index():
    left_index_pull = etee.get_index_pull('left')
    left_index_force = etee.get_index_force('left')
    return left_index_pull, left_index_force

def process_right_middle():
    right_middle_pull = etee.get_middle_pull('right')
    right_middle_force = etee.get_middle_force('right')
    return right_middle_pull, right_middle_force

def process_left_middle():
    left_middle_pull = etee.get_middle_pull('left')
    left_middle_force = etee.get_middle_force('left')
    return left_middle_pull, left_middle_force

def process_right_ring():
    right_ring_pull = etee.get_ring_pull('right')
    right_ring_force = etee.get_ring_force('right')
    return right_ring_pull, right_ring_force

def process_left_ring():
    left_ring_pull = etee.get_ring_pull('left')
    left_ring_force = etee.get_ring_force('left')
    return left_ring_pull, left_ring_force

def process_right_pinky():
    right_pinky_pull = etee.get_pinky_pull('right')
    right_pinky_force = etee.get_pinky_force('right')
    return right_pinky_pull, right_pinky_force

def process_left_pinky():
    left_pinky_pull = etee.get_pinky_pull('left')
    left_pinky_force = etee.get_pinky_force('left')
    return left_pinky_pull, left_pinky_force

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
        current_time = datetime.now().strftime("%H:%M:%S.%f")
        
        if etee.get_number_available_etee_ports() > 0:
            # Get data for all fingers
            right_thumb_pull, right_thumb_force = process_right_thumb()
            left_thumb_pull, left_thumb_force = process_left_thumb()
            right_index_pull, right_index_force = process_right_index()
            left_index_pull, left_index_force = process_left_index()
            right_middle_pull, right_middle_force = process_right_middle()
            left_middle_pull, left_middle_force = process_left_middle()
            right_ring_pull, right_ring_force = process_right_ring()
            left_ring_pull, left_ring_force = process_left_ring()
            right_pinky_pull, right_pinky_force = process_right_pinky()
            left_pinky_pull, left_pinky_force = process_left_pinky()

            if right_index_pull is None:  # Use any sensor to check connection
                print("---")
                print(current_time, "Right etee controller not detected. Please reconnect controller.")
                etee.start_data()
                time.sleep(0.05)
            else:
                # Format all finger data in a single line
                print(f"{current_time} | " +
                      f"Thumb  L: pull={left_thumb_pull:>3} force={left_thumb_force:>3} R: pull={right_thumb_pull:>3} force={right_thumb_force:>3} | " +
                      f"Index  L: pull={left_index_pull:>3} force={left_index_force:>3} R: pull={right_index_pull:>3} force={right_index_force:>3} | " +
                      f"Middle L: pull={left_middle_pull:>3} force={left_middle_force:>3} R: pull={right_middle_pull:>3} force={right_middle_force:>3} | " +
                      f"Ring   L: pull={left_ring_pull:>3} force={left_ring_force:>3} R: pull={right_ring_pull:>3} force={right_ring_force:>3} | " +
                      f"Pinky  L: pull={left_pinky_pull:>3} force={left_pinky_force:>3} R: pull={right_pinky_pull:>3} force={right_pinky_force:>3}")
                time.sleep(0.05)
        else:
            print("---")
            print(current_time, "Dongle disconnected. Please, re-insert the dongle and re-run the application.")
            etee.stop_data()  # Stop controller data stream
            print("Controller data stream stopped.")
            etee.stop()  # Stop data loop
            print("Data loop stopped.")
            time.sleep(0.05)
            sys.exit("Exiting application...")