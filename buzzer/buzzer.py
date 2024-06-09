import RPi.GPIO as GPIO
from time import sleep

def setup_buzzer(buzzer_pin=23):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer_pin, GPIO.OUT)
    return buzzer_pin

def buzzer_on(buzzer_pin):
    GPIO.output(buzzer_pin, GPIO.HIGH)

def buzzer_off(buzzer_pin):
    GPIO.output(buzzer_pin, GPIO.LOW)

def beep_buzzer(buzzer_pin, delay=0.5):
    buzzer_on(buzzer_pin)
    sleep(delay)
    buzzer_off(buzzer_pin)
    sleep(delay)

def cleanup():
    GPIO.cleanup()
