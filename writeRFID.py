import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
	text = input('Enter New Data to write on Card:')
	print ("Now place your tage to write...")
	reader.write(text)
	print("Data Written successfully")
finally:
	GPIO.cleanup()
