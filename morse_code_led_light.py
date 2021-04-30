import RPi.GPIO as GPIO
import string
import time

from enum import Enum
from functools import partial


LED_PIN_NUM = 11
DASH_NUM_OF_SECONDS = 2
DOT_NUM_OF_SECONDS = 1
PAUSE_NUM_OF_SECONDS = 1
SPACE_NUM_OF_SECONDS = 2


class LightSequenceNodes(Enum):
	dash = "dash"
	dot = "dot"
	pause = "pause"
	space = "space"


def set_up_gpio():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(LED_PIN_NUM, GPIO.OUT)
	GPIO.output(LED_PIN_NUM, GPIO.LOW)


def tear_down_gpio():
	GPIO.cleanup()


def display_morse_code(text):
	cleaned_text = clean_text(text)
	light_sequence = get_light_sequence(text)

	for f in light_sequence:
		f()


def clean_text(text):
	return text.translate(str.maketrans("", "", string.punctuation)).lower()


def get_light_sequence(text):
	light_sequence = []

	for character in text:
		# if space then add space func
		# if not then add pause func first
		# then check if dash or dot
		# if dash then add dash func
		# if dot then add dot func
		pass

	return light_sequence


def light_on(num_of_seconds):
	GPIO.output(LED_PIN_NUM, GPIO.HIGH)
	time.sleep(num_of_seconds)


def light_off(num_of_seconds):
	GPIO.output(LED_PIN_NUM, GPIO.LOW)
	time.sleep(num_of_seconds)


dash = partial(light_on, num_of_seconds=DASH_NUM_OF_SECONDS)
dot = partial(light_on, num_of_seconds=DOT_NUM_OF_SECONDS)
pause = partial(light_off, num_of_seconds=PAUSE_NUM_OF_SECONDS)
space = partial(light_off, num_of_seconds=SPACE_NUM_OF_SECONDS)


if __name__ == '__main__':
    set_up_gpio()

    try:
        display_morse_code("")  # Replace with text.
    except KeyboardInterrupt:
        tear_down_gpio()
