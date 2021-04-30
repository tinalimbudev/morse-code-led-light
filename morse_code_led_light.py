import RPi.GPIO as GPIO
import string
import time

from enum import Enum
from functools import partial


LED_PIN_NUM = 11

DASH = 1
DOT = 2
PAUSE = 3
SPACE = 4

DASH_NUM_OF_SECONDS = 2
DOT_NUM_OF_SECONDS = 1
PAUSE_NUM_OF_SECONDS = 1
SPACE_NUM_OF_SECONDS = 2


MORSE_CODE_MAP = {
	"a": [DOT, DASH],
	# TODO: Add rest of letters and numbers.
}


class InvalidCharacter(Exception):
	pass


def set_up_gpio():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(LED_PIN_NUM, GPIO.OUT)
	GPIO.output(LED_PIN_NUM, GPIO.LOW)


def tear_down_gpio():
	GPIO.cleanup()


def display_morse_code(text):
	cleaned_text = clean_text(text)
	code_sequence = get_code_sequence(text)
	light_sequence = get_light_sequence(code_sequence)

	for func in light_sequence:
		func()


def clean_text(text):
	return text.translate(str.maketrans("", "", string.punctuation)).lower()


def get_code_sequence(text):
	code_sequence = []

	for character in text:
		if character == " ":
			code_sequence.append(SPACE)
		else:
			try:
				codes = MORSE_CODE_MAP[character]
			except KeyError:
				print(f"Invalid character given: {character}")
				raise InvalidCharacter
			else:
				code_sequence.extend(codes)
				code_sequence.append(PAUSE)

	return code_sequence


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


def get_light_sequence(code_sequence):
	light_sequence = []

	for code in code_sequence:
		if code == DASH:
			func = dash
		elif code == DOT:
			func = dot
		elif code == PAUSE:
			func = pause
		elif code == SPACE:
			func == space
		else:
			raise NotImplementedError

		light_sequence.append(func)

	return light_sequence


if __name__ == '__main__':
    set_up_gpio()

    try:
        display_morse_code("")  # Replace with text.
    except (KeyboardInterrupt, InvalidCharacter):
        tear_down_gpio()
