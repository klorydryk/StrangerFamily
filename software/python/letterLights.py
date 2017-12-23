# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
import random
import os
from collections import OrderedDict

from neopixel import *

import argparse
import signal
import sys
def signal_handler(signal, frame):
        colorWipe(strip, Color(0,0,0))
        sys.exit(0)

def opt_parse():
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', action='store_true', help='clear the display on exit')
        args = parser.parse_args()
        if args.c:
                signal.signal(signal.SIGINT, signal_handler)

# LED strip configuration:
LED_COUNT      = 38      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

# Letters configuration :number of lights for each letter
# USAGE (for example with B):
#   position = ord('B') - ord('A')
#   2 = lightsList[position]
#   1 = Sum of previous positions
#         for j in range(1, 2):
#            strip.setPixelColor(j, color)
letters = OrderedDict()
#letters['A']=16
#letters['B']=12
#letters['C']=10
letters['A']=1
letters['B']=1
letters['C']=1
letters['D']=1
letters['E']=1
letters['F']=1
letters['G']=1
letters['H']=1
letters['I']=1
letters['J']=1
letters['K']=1
letters['L']=1
letters['M']=1
letters['N']=1
letters['O']=1
letters['P']=1
letters['Q']=1
letters['R']=1
letters['S']=1
letters['T']=1
letters['U']=1
letters['V']=1
letters['W']=1
letters['X']=1
letters['Y']=1
letters['Z']=1


def getLetterPositions(letter):
    letterPositions = [0, 0]

    if letter not in letters.keys():
       return letterPositions

    tableLetterPosition = letters.keys().index(letter)
    ledLetterPosition = 0

    print tableLetterPosition;

    for key in letters:
        if key != letter:
            ledLetterPosition += letters[key]
        else:
            break

    letterPositions[0] = ledLetterPosition
    letterPositions[1] = letters[letter]
    print letter
    print letterPositions
    return letterPositions

def lightning(strip, letterPositions):
    color = Color(255, 255, 255)
    random.seed(os.urandom(5))
    timeLeft = 500
    i = 0

    if letterPositions[1] == 0:
        time.sleep(timeLeft/1000.0)
        return

    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

# i-eme cycle
    while timeLeft>0:
        wait_ms = random.randint(0, timeLeft)
        if i%2==0:
            color = Color(red, green, blue)
        else:
            color = 0

        for j in range(letterPositions[0], letterPositions[0]+letterPositions[1]):
            strip.setPixelColor(j, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
        timeLeft = timeLeft-wait_ms
        i += 1
	shutoffLights(strip)


def shutoffLights(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, 0)
    strip.show()

def getSentence():
lineNb = 0
with open('sentences.txt', 'r') as f:
    num_lines = sum(1 for line in f)
    lineNb = random.randint(0, num_lines-1)
with open('sentences.txt', 'r') as f:
    for i, line in enumerate(f):
        if i == lineNb:
            return line




# Main program logic follows:
if __name__ == '__main__':
        # Process arguments
        opt_parse()

	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	shutoffLights(strip)


    string = getSentence() #"Friends dont lie"
	sequenceOfAlphabets = list(string.upper())
	for letter in sequenceOfAlphabets:
	    lightning(strip, getLetterPositions(letter))
	    time.sleep(0.3)