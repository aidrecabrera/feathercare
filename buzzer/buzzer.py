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

def play_tone(buzzer_pin, frequency, duration):
    period = 1.0 / frequency
    cycles = int(duration * frequency)
    for _ in range(cycles):
        buzzer_on(buzzer_pin)
        sleep(period / 2)
        buzzer_off(buzzer_pin)
        sleep(period / 2)

def cleanup():
    GPIO.cleanup()
