#imports for rabbitmq pi-to-pi connection
import pika

#imports for camera functionality
from picamera import PiCamera
import time
import os
#I'm not sure is this one is needed
from PIL import Image

#imports for twitter streaming
import tweepy
#Do we need these ones?
import json
import requests


#Global Variable keys (I got these from the twitter app page)
#Using the Cool Camera Kid Codes
consumer_key = "h4p5dOm1ah4SxFWt0Finxmd7I"
consumer_secret = "N1cm9yNEzG31B2WrBKT4L7lIBocotR62UmupcJKltyDeUHJDkH"
access_token = "3351579553-cYHh4gesLmv25tNIYUZiBqsNfK84Enx0urzshMs"
access_token_secret = "5A2sYDgjb8F89sCu0PsPIFaYx4dE1tjW1S4H75b0yabNy"




#Function to send out commands to networked pi's
#Sends same message to all pis. Maybe include parameter that specifies which pi
#passed in message should be the command wanted. Figure out how to parse this
def send_message(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()
    
    channel.exchange_declare(exchange='christmas', type='fanout')

    #message is passed in
    channel.basic_publish(exchange='test',
                          routing_key='',
                          body=message)
    
    #Take this out later. For testing purposes
    print (" [x] Sent message: ", message)
    connection.close()
    #see www.rabbitmq.com/tutorials/tutorial-three-python.html for more info



#Function to take pictures
#Returns the image/processed image
def take_picture():
    camera = PiCamera()

    camera.resolution = (1920, 1080)
    camera.capture('/home/pi/Desktop/GU_christmas_tree/saved_pictures/%s.ong' %time)

    #Need to make overlay first. Uncomment if you have one, and put .png file location in
    '''
    background = Image.open('/home/pi/Desktop/FallFamilyWeekend/Raw/%s.png' %time)
    overlay = Image.open('/home/pi/Desktop/GU_Christmas_tree/overlay.png')
    
    background = background.convert("RGBA")
    overlay = overlay.convert("RGBA")

    background.paste(overlay,(0,0), overlay)
            
    background.save("/home/pi/Desktop/GU_christmas_tree/processed_pictures/%s.png" %time, "PNG")
    '''
    #if overlay, do this one
    #image = os.path.abspath('/home/pi/Desktop/GU_christmas_tree/processed_pictures/%s.png' %time)
    #else, do this one
    image = os.path.abspath('/home/pi/Desktop/GU_christmas_tree/saved_pictures/%s.png' %time)
    #do we return the image or the image path and grab it in the higer function?
    return image

#Sets up twitter stream.
def twitter_stream():
    #Twitter stream connection initialization
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print 'Error! Failed to get request token.'

    request_token = auth.request_token


    class StdOutListener(tweepy.StreamListener):
        def on_data(self,data):
            #grabs all of the tweet's information in json format.
            tweet = json.loads(data)
            
            temp = tweet['text'] #gets actual text of tweet
            lst = temp.split('#')  #gets rid of the hashtag ending
            

            #gets the user that sent the tweet
            user = tweet.get('user')
            name = user['screen_name']
            print (user['screen_name'])

            #gets the time original tweet was sent.
            #Printed in the  retweet to prevent duplicate tweet errors
            time = tweet['created_at']
            time = time[:-10]       
            
            #Takes a picture and returns the processed image
            #Don't forget to actually attach the camera.
            image = take_picture()
        

            #Retweets the picture. Put in image for first param.
            #Put whatever we want for the status. @+name retweets to sender
            # +time to prevent retweet errors
            api.update_with_media(image, status="@" + name + "\nHappy Holidays!\n" + time + "\n")

            print("Tweet sent to %s" %name)
                  
        def on_error(self, status):
            print (status)

    #Starts the twitter stream
    #if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    print "Scanning for Hemmingson Playlist Requests"
    stream = tweepy.Stream(auth, l)
    #Set whatever hashtag we want
    stream.filter(track=['guchristmastree, GUchristmastree'])

def main():
    twtter_stream()

main()
    

