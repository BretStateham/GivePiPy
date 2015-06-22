#!/usr/bin/python

# Adafruit 30mm LED Dots Test
# WS2801 Chips
# Based on code from https://learn.adafruit.com/light-painting-with-raspberry-pi/overview


# Used raspi-config to enable SPI and I2C (not sure I2C is needed, but...)

#Import libraries

import RPi.GPIO as GPIO, time

# Configurable values
dev = "/dev/spidev0.0"


width = 3
height = 7


#Open the SPI device
spidev = file(dev,"wb")

# Calculate gamma correction table.
# using pburgess' suggested code from: http://forums.adafruit.com/viewtopic.php?f=47&t=31962
gamma = bytearray(256)
for i in range(256):
    gamma[i] = int(pow(float(i) / 255.0, 2.5) * 255.0 + 0.5)

#Create a list of bytearrays.
column = [0 for x in range(width)]
for x in range(width):
        column[x] = bytearray(height * 3)

# Convert 8-bit RGB image into column-wise RGB list
for x in range(width):
    for y in range(height):
        value = [0,0,0]
        value[x] = 255
        y3 = y * 3
        column[x][y3]   = gamma[value[0]]
        column[x][y3+1] = gamma[value[1]]
        column[x][y3+2] = gamma[value[2]]

# Then it's a trivial matter of writing each column to the SPI port.
print "Displaying..."
while True:
    for x in range(width):
        spidev.write(column[x])
        spidev.flush()
        #time.sleep(0.001)
        time.sleep(1)
    #time.sleep(0.5)
