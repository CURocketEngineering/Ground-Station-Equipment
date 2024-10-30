import threading 
import serial 
import time 

class SendingThread(threading.Thread):
    """
    Thread for repeatedly sending the same command to the xbee
    e.g. 
    "fuel", "purge"
    """

    def __init__(self, ser, command: str):
        """
        ser: serial.Serial object
        command: the command to send either "fuel" or "purge"
        """

        super().__init__()
        self.ser = ser 
        self.command = command + "\0\n\r"  # Add the null character and newline for parsing

        assert command in ["fuel", "purge"], f"Invalid command {command}"

        self._stop_event = threading.Event()

    def run(self):
        dots = 0
        while not self._stop_event.is_set():
            dots = (dots + 1) % 10
            dots_string = "." * dots
            print(" " * 100, end="\r")
            print(f"Sending command {self.command.strip()}{dots_string}", end="\r")
            self.ser.write(self.command.encode())
            time.sleep(1)  # Adjust the sleep time as needed

    def stop(self):
        self._stop_event.set()

class Communicator:
    """
    Communicator class for sending commands to the xbee and receiving data
    """

    def __init__(self, xbee_port: str, baud_rate: int = 9600):
        """
        xbee_port: the port of the xbee
        baud_rate: the baud rate of the xbee
        """

        self.ser = serial.Serial(xbee_port, baud_rate)

        self.sending_thread = None

        self.current_pulsing_command = None

    def kill_sending_thread(self):
        """
        Kill the sending thread
        """

        if self.sending_thread is not None:
            self.sending_thread.stop()
            self.sending_thread.join()
            self.sending_thread = None
            self.current_pulsing_command = None

    def start_command_pulsing(self, command: str):
        """
        Start sending the command repeatedly
        command: the command to send either "fuel" or "purge"
        """

        self.kill_sending_thread()
        self.sending_thread = SendingThread(self.ser, command)
        self.sending_thread.start()
        self.current_pulsing_command = command

    def clean_up(self):
        """
        Clean up the communicator
        """

        self.kill_sending_thread()
        self.close()

    def close(self):
        """
        Close the serial connection
        """

        self.ser.close()