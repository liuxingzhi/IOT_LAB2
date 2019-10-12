import time
import serial
import RPi.GPIO as GPIO

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

counter = 0
while True:
    ser.write(str.encode('Write counter: %d \n' % (counter)))
    time.sleep(1)
    counter += 1
