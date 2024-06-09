from buzzer import buzzer

def main():
    buzzer_pin = buzzer.setup_buzzer()
    try:
        while True:
            buzzer.beep_buzzer(buzzer_pin, delay=1)
    except KeyboardInterrupt:
        pass
    finally:
        buzzer.cleanup()

if __name__ == "__main__":
    main()