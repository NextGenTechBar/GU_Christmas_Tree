#!/usr/bin/python

#import for camera
from picamera import PiCamera
import picamera
import time
import os
from PIL import Image

camera = None
PIC_DIR = '/home/pi/photos/'
SAVE_PICS = False
ovl_name = 'overlay.png'
bk_name = 'background.png'

def take_picture():
	if SAVE_PICS :
		img_name = ("%s_raw.png" %time)
	else :
		img_name = "XMAS_raw.png"

	print("Taking a photo. Named: %s" %img_name)	

	time.sleep(1)

	camera.capture("%s/%s" %(PIC_DIR,img_name))

	#Need to make overlay first. Uncomment if you have one, and put .png file l$
	background = Image.open("%s/%s" %(PIC_DIR,bk_name)) 
	tree = Image.open("%s/%s" %(PIC_DIR,img_name))
	overlay = Image.open("%s/%s" %(PIC_DIR,ovl_name))

	background = background.convert("RGBA")
	tree = tree.convert("RGBA")
	overlay = overlay.convert("RGBA")

	background.paste(tree,(170,0),tree)
	background.paste(overlay,(0,0), overlay)

	background.save("%s/out_%s" %(PIC_DIR,img_name), "PNG")

	#if overlay, do this one
	image = os.path.abspath("%s/out_%s" %(PIC_DIR,img_name))
    	return image

def main():
	#initilize camera
	global camera
	
	try:     
		camera = PiCamera()
		camera.vflip = True
		camera.hflip = True
	        #camera.resolution = (1024,512) #This may be wack, but it is a good test
#		camera.resolution = (2592,1944) #full size
		camera.resolution = (683,512)

	except picamera.PiCameraError :
        	print("Error initilizing Camera, probably already running! Exiting")
		return

	take_picture()



main()
	
