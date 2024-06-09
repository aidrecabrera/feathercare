import time
import sys
import serial

def convert_to_string(buf):
    try:
        return buf.decode('utf-8').strip()
    except UnicodeError:
        tmp = bytearray(buf)
        for i in range(len(tmp)):
            if tmp[i] > 127:
                tmp[i] = ord('#')
        return bytes(tmp).decode('utf-8').strip()

class SIM800L:
    def __init__(self, ser):
        try:
            self.ser = serial.Serial(ser, baudrate=9600, timeout=1)
        except Exception as e:
            sys.exit(f"Error: {e}")
        self.incoming_action = None
        self.no_carrier_action = None
        self.clip_action = None
        self._clip = None
        self.msg_action = None
        self._msgid = 0
        self.savbuf = None

    def setup(self):
        self.command('ATE0\n')         # command echo off
        self.command('AT+CLIP=1\n')    # caller line identification
        self.command('AT+CMGF=1\n')    # plain text SMS
        self.command('AT+CLTS=1\n')    # enable get local timestamp mode
        self.command('AT+CSCLK=0\n')   # disable automatic sleep

    def callback_incoming(self, action):
        self.incoming_action = action

    def callback_no_carrier(self, action):
        self.no_carrier_action = action

    def get_clip(self):
        return self._clip

    def callback_msg(self, action):
        self.msg_action = action

    def get_msgid(self):
        return self._msgid

    def command(self, cmdstr, lines=1, waitfor=500, msgtext=None):
        self.ser.reset_input_buffer()  # Ensure input buffer is clear
        self.ser.write(cmdstr.encode())
        if msgtext:
            self.ser.write(msgtext.encode())
        if waitfor > 1000:
            time.sleep((waitfor - 1000) / 1000)

        result = ''
        try:
            for _ in range(lines):
                buf = self.ser.readline()
                if buf:
                    line = convert_to_string(buf)
                    if line:
                        result += line + '\n'
                else:
                    break
        except Exception as e:
            print(f"Error reading from serial: {e}")
        return result.strip()

    def send_sms(self, destno, msgtext):
        result = self.command(f'AT+CMGS="{destno}"\n', lines=2, waitfor=5000, msgtext=msgtext + '\x1A')
        if result and '>' in result:
            return 'OK'
        return 'ERROR'

    def read_sms(self, id):
        result = self.command(f'AT+CMGR={id}\n', lines=99)
        if result:
            parts = result.split('\n', 1)
            if len(parts) > 1 and '+CMGR' in parts[0]:
                header = parts[0].split(',')
                number = header[1].replace('"', '').strip()
                date = header[3].replace('"', '').strip()
                time = header[4].replace('"', '').strip()
                message = parts[1]
                return [number, date, time, message]
        return None

    def delete_sms(self, id):
        self.command(f'AT+CMGD={id}\n', lines=1)

    def check_incoming(self): 
        if self.ser.in_waiting:
            buf = self.ser.readline()
            buf = convert_to_string(buf)
            params = buf.split(',')

            if params[0].startswith("+CMTI"):
                self._msgid = int(params[1])
                if self.msg_action:
                    self.msg_action()

            elif params[0] == "NO CARRIER":
                if self.no_carrier_action:
                    self.no_carrier_action()

            elif params[0] == "RING" or params[0].startswith("+CLIP"):
                if self.incoming_action:
                    self.incoming_action()

    def read_and_delete_all(self):
        try:
            return self.read_sms(1)
        finally:
            self.command('AT+CMGDA="DEL ALL"\n', lines=1)
