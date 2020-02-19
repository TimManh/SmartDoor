import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

print("Looking for cards")
print("Press Ctrl+c to STOP")

try:
	id,text = reader.read()
	print(id)
	print(text)
finally:
	GPIO.cleanup()
