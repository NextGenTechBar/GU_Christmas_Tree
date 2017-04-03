#!/usr/bin/python

#imports for rabbitmq pi-to-pi connection
import pika

#imports for camera functionality
from picamera import PiCamera
import picamera
import time
import os
#I'm not sure is this one is needed (Yep! it is)
from PIL import Image

#imports for twitter streaming
import tweepy
#Do we need these ones?
import json
import requests

#for string editing
import re
import string

#Twitter Handle Blacklist (accounts that we don't want to be able to interact with the bot
#MAKE SURE THESE ARE LOWER CASE
twAccBlacklist = ['gu_ngtb' , 'gonzagaits', 'guhemmingson', 'gonzagau', 'guchristmastree','gonzagacio' ]

#Picture Things including the Directory of photos and if we want to save photos every time
camera = None
PIC_DIR = '/home/pi/photos/'
SAVE_PICS = False
ovl_name = 'overlay.png'
bk_name = 'background.png'

#Global Variable keys (I got these from the twitter app page)
#Using the Cool Camera Kid Codes
#consumer_key = "h4p5dOm1ah4SxFWt0Finxmd7I"
#consumer_secret = "N1cm9yNEzG31B2WrBKT4L7lIBocotR62UmupcJKltyDeUHJDkH"
#access_token = "3351579553-cYHh4gesLmv25tNIYUZiBqsNfK84Enx0urzshMs"
#access_token_secret = "5A2sYDgjb8F89sCu0PsPIFaYx4dE1tjW1S4H75b0yabNy"
consumer_key = "qArKjNWYjqR9LOkcFiS1mH0Pj" 
consumer_secret = "MD0FbgxXNazrrTeg9X0RnCHPzjqNCWObqc1PxQHMmE78ud9rBT"
access_token = "799044415809417218-srpq6iipfwkwAWmqDRNA1hr2vDlAjiJ"
access_token_secret = "up0Sljywk5CMPnRseADWTu2k6ni2jxvTTaJSGaov83vhN" 



#Function to send out commands to networked pi's
#Sends same message to all pis. Maybe include parameter that specifies which pi
#passed in message should be the command wanted. Figure out how to parse this
def send_message(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()
    
    channel.exchange_declare(exchange='christmas', type='fanout')

    #message is passed in. twitter function will convert tweeted message to pi message
    channel.basic_publish(exchange='christmas',
                          routing_key='',
                          body=message)
    
    #Take this out later. For testing purposes
    print (" [x] Sent message: ", message)
    connection.close()
    #see www.rabbitmq.com/tutorials/tutorial-three-python.html for more info


def getFormat(red, green, blue):
        return '-2-%d-%d-%d-' % (red, green, blue)


#fill in later. Converts tweet to usable message by pi-nodes
def tweet_to_command(tweet):
    colors = {'red':getFormat(255, 0, 0), 'green':getFormat(0,255,0), 'blue':getFormat(0,0,255),
              'yellow':getFormat(255,255,0), 'orange':getFormat(255,128,0), 'purple': getFormat(128,0,128),
              'pink':getFormat(255,192,203), 'indigo':getFormat(75,0,130), 'turquoise':getFormat(0,245,255),
              'mint':getFormat(189,252,201), 'olive':getFormat(128,128,0), 'banana':getFormat(227,207,87),
              'gold':getFormat(255,215,0), 'tan':getFormat(210,190,140), 'chocolate':getFormat(210,105,30),
              'flesh':getFormat(255,125,64), 'salmon':getFormat(250,128,114), 'brown':getFormat(165,42,42),
              'black':getFormat(0,0,0), 'grey':getFormat(128,128,128), 'gray':getFormat(128,128,128),
              'white':getFormat(255,255,255), 'maroon':getFormat(255,52,179), 'violet':getFormat(238,130,238),
              'navy':getFormat(0,0,128), 'hot pink':getFormat(255,105,180), 'fuchsia':getFormat(255,0,255),
              'magenta':getFormat(255,0,255), 'silver':getFormat(192,192,192), 'lime':getFormat(60,255,15),
              'aqua':getFormat(0,255,255), 'aquamarine':getFormat(127,255,212), 'teal':getFormat(0,128,128),
              'evergreen':getFormat(0,129,69), 'crimson':getFormat(220,20,0), 'snow':getFormat(255,255,250),
              'rose':getFormat(255,238,225), 'pumpkin':getFormat(255,127,0), 'cranberry':getFormat(176,23,31),
              'robert':getFormat(34,139,34), 'emerald':getFormat(0,201,87), 'cyan':getFormat(0,255,255),
	      'mauve':getFormat(224,176,255), 'lavender':getFormat(181,126,220), 'chartreuse':getFormat(127,255,0),
	      'scarlet':getFormat(255,36,0), 'burgundy':getFormat(144,0,32), 'periwinkle':getFormat(204,204,255),
	      'sapphire':getFormat(15,82,186) }
    
    if not isinstance(tweet, unicode):   #Checks type of tweet
	return "error"                   #Hopefully catches our nonetype error

    #Checks for numbers first. Returns a command if there is a rgb vaule in the tweet
    tweet = tweet.lower()
    if (re.search(r'\d', tweet)):
	number_list = re.sub('[^0-9]', ' ', tweet).split()
	print (number_list)
	if (len(number_list) == 3):
		r = number_list[0]
		g = number_list[1]
		b = number_list[2]
		if int(r) < 256 and int(g) < 256 and int(b) < 256:
			cmd ='-2-'+ r+'-'+g+'-'+b+'-'
			print(cmd)
			return cmd

    #Checks for color words next
    word_list = re.sub(r'[^a-zA-A ]', ' ', tweet).split()  #Splits the text. Replaces all non-letters with spaces, then splits on spaces
    for word in word_list:                  #Checks every word in the tweet
        word_temp = word.split('\n')        #removes the \n character from any word
        print (word_temp[0])                #we don't need this print, but it helps
	if word_temp[0] == 'rainbow' :
	    print("Rainbow Time!!!")
	    return ('rainbow')
        for key in colors.keys():	    #runs through the keys in the color dictionary
            if word_temp[0] == key:         #Checks each key against each word
		print(" [P] There is a color in that tweet!")
		print (colors[word_temp[0]])
 		return (colors[word_temp[0]])

    return ("error")    #throws an error is no word in the tweet is in the color dictionary.
           

              


#Function to take pictures
#Returns the image/processed image
def take_picture():
    if SAVE_PICS : #if we are saving pictures, set name to current time
	img_name = ("%s_raw.png" %time)
    else : #if not, just name XMAS_raw
	img_name = "XMAS_raw.png"

    #wait command. use to sync up color change with the picture
    time.sleep(6)
	
    #capture image
    camera.capture("%s/%s" %(PIC_DIR,img_name))

    #Need to make overlay first. Uncomment if you have one, and put .png file location in
    background = Image.open("%s/%s" %(PIC_DIR,bk_name))
    tree = Image.open("%s/%s" %(PIC_DIR,img_name))
    overlay = Image.open("%s/%s" %(PIC_DIR,ovl_name))
    
    background = background.convert("RGBA")
    tree = tree.convert("RGBA")
    overlay = overlay.convert("RGBA")

    background.paste(tree,(170,0), tree)
    background.paste(overlay,(0,0), overlay)
            
    background.save("%s/out_%s" %(PIC_DIR,img_name), "PNG")
  
    #if overlay, do this one
    image = os.path.abspath("%s/out_%s" %(PIC_DIR,img_name))
    #else, do this one
    #image = os.path.abspath('/home/pi/Desktop/GU_christmas_tree/saved_pictures/%s.png' %time)

    return image

#Sets up twitter stream.
def twitter_stream():
    #Twitter stream connection initialization
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
    except:
	twitter_stream()	

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print ('Error! Failed to get request token. Trying again..')

    request_token = auth.request_token

    class StdOutListener(tweepy.StreamListener):
        def on_data(self,data):
            #grabs all of the tweet's information from json format.
            tweet = json.loads(data)
            
            temp = tweet['text'] #gets actual text of tweet
            #lst = temp.split('#')  #gets rid of the hashtag ending
            #text = lst[0]
	    text = temp
	    
	    #Grabs the tweet id so we can retweet
	    tweet_id= tweet['id']
 	    
            #gets the user that sent the tweet
            user = tweet.get('user')
            name = user['screen_name']
            print (user['screen_name'])
		
	    if name.lower() in twAccBlacklist :
		print("Accout in Blacklist! Ignorning interaction")
		return

            #gets the time original tweet was sent.
            #Printed in the  retweet to prevent duplicate tweet errors
            time = tweet['created_at']
            time = time[:-10]       

            #send out commands to other pi-nodes
            ard_msg = tweet_to_command(text)
	    print(ard_msg)
	    if ard_msg != "error":
	        if ard_msg == 'rainbow':
		    send_rainbow()
		else:
	    	    send_message(ard_msg)
		image = take_picture()
		retweet = "\nHappy Holidays from Gonzaga!\n"
		api.update_with_media(image, status='@' + name + retweet + time, in_reply_to_status_id = tweet_id)
	    else:
		#change the massage as desired
	    	retweet = "\nSorry, We didn't find any colors in your tweet.\nHave a Merry Christmas!\n"
		api.update_status(status="@" + name + retweet + time + "\n", in_reply_to_status_id = tweet_id)	    	 


            print("Tweet sent to %s" %name)
                  
        def on_error(self, status):
            print (status)

    #Starts the twitter stream
    #if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    print "  [!] Scanning for Holiday Tweets [!]"
    stream = tweepy.Stream(auth, l)
    #Set whatever hashtag we want
    #stream.filter(track=['ngtbtest'])
    stream.filter(track=['guchristmastree, GUchristmastree, GUChristmasTree, GUCHRISTMASTREE'])

def send_rainbow():
    #White (8)
    rain_msg = '-3-8-255-255-255-'
    send_message(rain_msg)

    #Magenta (7)
    rain_msg = '-3-7-128-0-128-'
    send_message(rain_msg)

    #Purple (9)
    rain_msg = '-3-9-255-0-0-'
    send_message(rain_msg)

    #Red (5)
    rain_msg = '-3-5-255-50-0-'
    send_message(rain_msg)

    #Orange (4)
    rain_msg = '-3-4-255-100-0-'
    send_message(rain_msg)

    #Yellow (2)
    rain_msg = '-3-2-200-255-0-'
    send_message(rain_msg)

    #Green (6)
    rain_msg = '-3-6-0-255-0-'
    send_message(rain_msg)

    #Aqua (1)
    rain_msg = '-3-1-0-255-255-'
    send_message(rain_msg)

    #Blue (3)
    rain_msg = '-3-3-0-0-255-'
    send_message(rain_msg)

def main():
    #initilize camera
    global camera
    try:
    	camera = PiCamera()
    	#camera.resolution = (1024,512) #This may be wack, but it is a good test
	camera.resolution = (683,512)
	camera.vflip = True
	camera.hflip = True

    except picamera.PiCameraError :
	print("Error initilizing Camera, probably already running! Exiting")
	return

	
    while True:
        try:
	    twitter_stream()
        except:
	    print("Error in twitter_stream()! Restarting!")
	    time.sleep(2)

#time.sleep(1)
main()
    

