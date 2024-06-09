from time import sleep
from buzzer.buzzer import cleanup, play_tone, setup_buzzer


def main():
    buzzer_pin = setup_buzzer()
    try:
        mario_tune = [
            (659, 0.1), (659, 0.1), (0, 0.1), (659, 0.1),  # E E E pause E
            (523, 0.1), (659, 0.1), (784, 0.1), (0, 0.1),  # C E G pause
            (392, 0.2), (0, 0.2),                         # G pause
            (523, 0.1), (392, 0.1), (330, 0.1), (440, 0.1),  # C G E A
            (494, 0.1), (466, 0.1), (440, 0.1), (392, 0.1),  # B A# A G
            (659, 0.1), (784, 0.1), (880, 0.1), (698, 0.1),  # E G A F
            (784, 0.1), (659, 0.1), (523, 0.1), (587, 0.1),  # G E C D
            (494, 0.2),                                    # B
        ]
        for tone in mario_tune:
            frequency, duration = tone
            if frequency == 0:
                sleep(duration)
            else:
                play_tone(buzzer_pin, frequency, duration)
            sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()

if __name__ == "__main__":
    main()
