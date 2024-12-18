"""
Example code:
-------------
This script shows how to use getter functions to retrieve controller data.
In this case, getter functions are called every loop. Getter functions pull data from the driver internal buffer, which
gets updated every time data is received from the controllers. If event-based methods are used, the frequency of data
received from the controllers can be irregular (e.g. 5ms, or 10ms). Unlike the event-based method, getter functions
allow the user to have better control in the timing of data retrieval.
"""

import time
import sys
import keyboard
from datetime import datetime
from etee import EteeController


def process_right_index():
    right_index_pull = etee.get_index_pull('right')
    right_index_force = etee.get_index_force('right')
    return right_index_pull, right_index_force

def process_left_index():
    left_index_pull = etee.get_index_pull('left')
    left_index_force = etee.get_index_force('left')
    return left_index_pull, left_index_force


if __name__ == "__main__":
    # Initialise the etee driver and find dongle
    etee = EteeController()
    num_dongles_available = etee.get_number_available_etee_ports()
    etee.connect()     # Attempt connection to etee dongle
    time.sleep(1)
    etee.start_data()  # Attempt to send a command to etee controllers to start data stream
    etee.run()         # Start data loo

    # If dongle is connected, print index values
    while True:
        num_dongles_available = etee.get_number_available_etee_ports()
        current_time = datetime.now().strftime("%H:%M:%S.%f")

        if num_dongles_available > 0:
            right_index_pull, right_index_force = process_right_index()
            left_index_pull, left_index_force = process_left_index()
            if right_index_pull is None:
                print("---")
                print(current_time, "Right etee controller not detected. Please reconnect controller.")
                etee.start_data()   # Retry reconnection and data stream access in controllers
                time.sleep(0.05)
            else:
                print(current_time, f"L: pull = {left_index_pull:>3}  |  force = {left_index_force:>3} R: pull = {right_index_pull:>3}  |  force = {right_index_force:>3}")
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
