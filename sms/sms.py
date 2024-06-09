import serial
import time

class BinNotificationSystem:
    def __init__(self, port="/dev/ttyUSB0", baud_rate=9600):
        self.serial_connection = serial.Serial(port, baud_rate, timeout=1)
        time.sleep(2)
        
    def send_notification(self, action):
        commands = {
            'start': 's',
            'notify': 'n',
        }
        if action in commands:
            print(f"Sending notification for {action} bin.")
            self.serial_connection.write(commands[action].encode())
        else:
            print("Invalid or Error")
            
    def close(self):
        self.serial_connection.close()
        print("COMM Closed!")