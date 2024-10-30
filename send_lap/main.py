"""
Runs a CLI where you can send commands to fuel and purge over serial to the XBee  
"""

import sys
import os

import time
import serial

from communicator import Communicator

XBEE_PORT = "/dev/ttyUSB0"


def process_data(data):
    """
    Given as a callback to the xbee object
    """
    print("Received data: " + str(data))


def menu(communicator: Communicator):
    """
    Based on the current state of the communicator, display the menu
    """
    print("1. Start fueling")
    print("2. Start purging")
    print("3. Stop fueling/purging")
    print("4. Refresh Menu")
    print("5. Exit")

    choice = input("Enter your choice: \n\n")

    if choice == "1":
        communicator.start_command_pulsing("fuel_")
    elif choice == "2":
        communicator.start_command_pulsing("purge")
    elif choice == "3":
        communicator.kill_sending_thread()
    elif choice == "4":
        pass
    elif choice == "5":
        return True
    
    return False



def main():
    """
    Main function
    """

    communicator = Communicator(XBEE_PORT)
    done = False 
    while not done:
        try:
            
            done = menu(communicator)
            time.sleep(1)

        except KeyboardInterrupt:
            done = True 

    print("Cleaning up communicator...")
    communicator.clean_up()
    print("Exiting...")
    sys.exit(0)


if __name__ == "__main__":
    main()
