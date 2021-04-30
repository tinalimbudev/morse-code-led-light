import RPi.GPIO as GPIO
import time


LED_PIN_NUMBER = 11


def set_up_gpio():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(LED_PIN_NUMBER, GPIO.OUT)
	GPIO.output(LED_PIN_NUMBER, GPIO.LOW)


def display_morse_code():
	# GPIO.output(ledPin, GPIO.HIGH)  # make ledPin output HIGH level to turn on led
	# print ('led turned on >>>')     # print information on terminal
	# time.sleep(1)                   # Wait for 1 second
	# GPIO.output(ledPin, GPIO.LOW)   # make ledPin output LOW level to turn off led
	# print ('led turned off <<<')
	# time.sleep(1)                   # Wait for 1 second
	pass


def tear_down_gpio():
	GPIO.cleanup()


if __name__ == '__main__':
    set_up_gpio()

    try:
        display_morse_code()
    except KeyboardInterrupt:
        tear_down_gpio()
