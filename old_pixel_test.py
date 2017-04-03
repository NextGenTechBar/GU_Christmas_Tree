#!/usr/bin/python
import time
#import pdb

from neopixel import *

#LED Strip config
LED_COUNT = 100
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 5
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_STRIP = ws.WS2811_STRIP_BGR

def colorWipe(strip, color, wait_ms=50):

	print "Color Wipe!"
	print "Number of Pixels: ",strip.numPixels()

	for i in range(strip.numPixels()):
#		pdb.set_trace()
		strip.setPixelColor(i,color)
		strip.show()
		time.sleep(wait_ms/1000.0)





if __name__ == '__main__':


	print "Starting the NGTB XMAS Pi Script"
	print "Using LED_STRIP: ",LED_STRIP

	#Initilize NeoPixel Strip
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS) #LED_STRIP
	strip.begin()

	print "Strip Initilized"

	while True:
		print "Top of Loop"
		colorWipe(strip, Color(255,0,0))
		print "Second part of Loop"
		colorWipe(strip, Color(0,255,0))
		colorWipe(strip, Color(0,0,255))
		colorWipe(strip, Color(255,255,255))

	print "Exiting"


	
