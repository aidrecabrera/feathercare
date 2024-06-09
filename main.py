from time import sleep
from sms.sms import BinNotificationSystem

def main():
    bin_notification = BinNotificationSystem()
    bin_notification.send_notification('start')
    sleep(5)
    bin_notification.send_notification('notify')
    bin_notification.close()