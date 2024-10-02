"""
Runs a CLI where you can send commands to fuel and purge over serial to the XBee  
"""

import sys
import os
import threading 
import time
import serial

XBEE_PORT = "COM3"
ser = serial.Serial(XBEE_PORT, 9600)

status = ["`fuel`, `purge`, or `exit`", 0,
          "1: fuel, 2: purge, 3: exit"]


def process_data(data):
    """
    Given as a callback to the xbee object
    """
    print("Received data: " + str(data))


class SendingThread(threading.Thread):
    """
    Thread for repeatedly sending the same command to the xbee
    e.g. 
    "fuel", "purge"
    """

    global status

    def __init__(self, command):
        super().__init__()
        self.command = command
        self._stop_event = threading.Event()

        status[0] = f"Sending command: {self.command}"
        status[1] = 0

    def run(self):
        while not self._stop_event.is_set():
            status[1] = status[1] + 1
            print(status[0], status[1], "\n", status[2], end="\r")
            ser.write(self.command.encode())
            time.sleep(1)  # Adjust the sleep time as needed

    def stop(self):
        self._stop_event.set()


def main():
    """
    Main function
    """

    # Import the xbee module
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

    # Create an xbee object
    # my_xbee = XBee(ser, callback=process_data)

    # Create a thread for sending commands
    sending_thread = None

    command_dict = {"1": "fuel", "2": "purge"}

    print("Ready... Type 1 to fuel or 2 to purge")

    try:
        # Loop for sending commands
        while True:
            # Get the command
            command = input()

            # If the command is empty, stop the sending thread
            if command == "":
                if sending_thread is not None:
                    sending_thread.stop()
                    sending_thread.join()
                    sending_thread = None
                    print("STOPPED SENDING")
                continue

            if command == "exit":
                print("Exiting...")
                break

            # If the command is valid, start the sending thread
            if command in ["1", "2"]:
                # If there is an existing thread, stop it first
                if sending_thread is not None:
                    sending_thread.stop()
                    sending_thread.join()
                    sending_thread = None
                    print("STOPPED SENDING")

                sending_thread = SendingThread(command_dict[command])
                sending_thread.start()
            else:
                print("Invalid command")

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Stopping...")

    finally:
        # Ensure the thread is properly stopped and joined before exiting
        if sending_thread is not None:
            sending_thread.stop()
            sending_thread.join()

        # Close the serial port
        ser.close()
        print("Serial port closed. Program exited.")


if __name__ == "__main__":
    main()
