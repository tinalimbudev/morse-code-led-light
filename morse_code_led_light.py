import RPi.GPIO as GPIO
import string
import time

from enum import Enum
from functools import partial


LED_PIN_NUM = 11


DOT = "1"
DASH = "2"
SPACE_SL = "3"  # The space between parts of the same letter.
SPACE_BL = "4"  # The space between different letters.
SPACE_BW = "5"  # The space between different words.


DOT_SECS = 1
DASH_SECS = DOT_SECS * 3
SPACE_SL_SECS = DOT_SECS
SPACE_BL_SECS = DOT_SECS * 3
SPACE_BW_SECS = DOT_SECS * 7


MORSE_CODE_MAP = {
	"a": [DOT, DASH],
	"b": [DASH, DOT, DOT, DOT],
	"c": [DASH, DOT, DASH, DOT],
	"d": [DASH, DOT, DOT],
	"e": [DOT],
	"f": [DOT, DOT, DASH, DOT],
	"g": [DASH, DASH, DOT],
	"h": [DOT, DOT, DOT, DOT],
	"i": [DOT, DOT],
	"j": [DOT, DASH, DASH, DASH],
	"k": [DASH, DOT, DASH],
	"l": [DOT, DASH, DOT, DOT],
	"m": [DASH, DASH],
	"n": [DASH, DOT],
	"o": [DASH, DASH, DASH],
	"p": [DOT, DASH, DASH, DOT],
	"q": [DASH, DASH, DOT, DASH],
	"r": [DOT, DASH, DOT],
	"s": [DOT, DOT, DOT],
	"t": [DASH],
	"u": [DOT, DOT, DASH],
	"v": [DOT, DOT, DOT, DASH],
	"w": [DOT, DASH, DASH],
	"x": [DASH, DOT, DOT, DASH],
	"y": [DASH, DOT, DASH, DASH],
	"z": [DASH, DASH, DOT, DOT],
	"1": [DOT, DASH, DASH, DASH, DASH],
	"2": [DOT, DOT, DASH, DASH, DASH],
	"3": [DOT, DOT, DOT, DASH, DASH],
	"4": [DOT, DOT, DOT, DOT, DASH],
	"5": [DOT, DOT, DOT, DOT, DOT],
	"6": [DASH, DOT, DOT, DOT, DOT],
	"7": [DASH, DASH, DOT, DOT, DOT],
	"8": [DASH, DASH, DASH, DOT, DOT],
	"9": [DASH, DASH, DASH, DASH, DOT],
	"10": [DASH, DASH, DASH, DASH, DASH],
}
CODE_MAP = {k: SPACE_SL.join(v) for k, v in MORSE_CODE_MAP.items()}


class InvalidInput(Exception):
	pass


def set_up_gpio():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(LED_PIN_NUM, GPIO.OUT)
	GPIO.output(LED_PIN_NUM, GPIO.LOW)


def tear_down_gpio():
	GPIO.cleanup()


def display_morse_code(text):
	cleaned_text = clean_text(text)
	code_sequence = get_code_sequence(cleaned_text)
	light_sequence = get_light_sequence(code_sequence)

	for func in light_sequence:
		func()

	GPIO.output(LED_PIN_NUM, GPIO.LOW)


def clean_text(text):
	if not isinstance(text, str):
		print("Invalid input type given - please provide a string")
		raise InvalidInput

	return text.translate(str.maketrans("", "", string.punctuation)).lower()


def get_code_sequence(text):
	code_sequence = []

	for character in text:
		if character == " ":
			code_sequence.append(SPACE_BW)
		else:
			try:
				codes = CODE_MAP[character]
			except KeyError:
				print(f"Invalid character given: {character}")
				raise InvalidInput
			else:
				code_sequence.extend(codes)
				code_sequence.append(SPACE_BL)

	return code_sequence


def light_on(num_of_seconds):
	GPIO.output(LED_PIN_NUM, GPIO.HIGH)
	time.sleep(num_of_seconds)


def light_off(num_of_seconds):
	GPIO.output(LED_PIN_NUM, GPIO.LOW)
	time.sleep(num_of_seconds)


dot = partial(light_on, num_of_seconds=DOT_SECS)
dash = partial(light_on, num_of_seconds=DASH_SECS)
space_sl = partial(light_off, num_of_seconds=SPACE_SL_SECS)
space_bl = partial(light_off, num_of_seconds=SPACE_BL_SECS)
space_bw = partial(light_off, num_of_seconds=SPACE_BW_SECS)


def get_light_sequence(code_sequence):
	light_sequence = []

	for code in code_sequence:
		if code == DOT:
			func = dot
		elif code == DASH:
			func = dash
		elif code == SPACE_SL:
			func = space_sl
		elif code == SPACE_BL:
			func == space_bl
		elif code == SPACE_BW:
			func = space_bw
		else:
			raise NotImplementedError

		light_sequence.append(func)

	return light_sequence


if __name__ == '__main__':
    set_up_gpio()

    try:
        display_morse_code("")  # Replace with text.
    except (KeyboardInterrupt, InvalidInput):
        tear_down_gpio()
