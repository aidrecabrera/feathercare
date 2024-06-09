import time
from gsm.gsm import SIM800L

def main():
    gsm = SIM800L("/dev/serial0")
    gsm.setup()

    def on_incoming_call():
        print("Incoming call detected.")

    def on_no_carrier():
        print("No carrier detected.")

    def on_new_message():
        msg_id = gsm.get_msgid()
        print(f"New message with ID: {msg_id}")
        message = gsm.read_sms(msg_id)
        if message:
            print(f"Message from {message[0]} received at {message[1]} {message[2]}: {message[3]}")
            gsm.delete_sms(msg_id)

    gsm.callback_incoming(on_incoming_call)
    gsm.callback_no_carrier(on_no_carrier)
    gsm.callback_msg(on_new_message)

    while True:
        gsm.check_incoming()
        time.sleep(1)

if __name__ == "__main__":
    main()
