import RPi.GPIO as GPIO
import time

from functools import partial


LED_PIN_NUM = 11
DASH_NUM_OF_SECONDS = 2
DOT_NUM_OF_SECONDS = 1
OFF_NUM_OF_SECONDS = 1


def set_up_gpio():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(LED_PIN_NUM, GPIO.OUT)
	GPIO.output(LED_PIN_NUM, GPIO.LOW)


def tear_down_gpio():
	GPIO.cleanup()


def display_morse_code():
	pass


def light_on(num_of_seconds):
	GPIO.output(LED_PIN_NUM, GPIO.HIGH)
	time.sleep(num_of_seconds)


def light_off():
	GPIO.output(LED_PIN_NUM, GPIO.LOW)
	time.sleep(OFF_NUM_OF_SECONDS)


dash_on = partial(light_on, num_of_seconds=DASH_NUM_OF_SECONDS)
dot_on = partial(light_on, num_of_seconds=DOT_NUM_OF_SECONDS)


if __name__ == '__main__':
    set_up_gpio()

    try:
        display_morse_code()
    except KeyboardInterrupt:
        tear_down_gpio()
