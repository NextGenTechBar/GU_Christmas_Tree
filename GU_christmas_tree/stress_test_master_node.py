#!/usr/bin/python

#Communication library
import pika

#Input of messages
import sys

#Random Number Lib and sleeping time
import random
from time import sleep

def send_message(message):
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.exchange_declare(exchange='christmas', type='fanout')

	#message is passed in
	channel.basic_publish(exchange='christmas',
			      routing_key='',
			      body = message)

	print(" [x] Sent message: %s" % message)
	connection.close()

def main():

	cnt = 0;	

	while True:
		cnt = cnt + 1
		print("Loop %d " %cnt)

		if cnt % 10 == 0 :
			msg = '-1-'
		else :
			#Initilize Set Color  Message to be random ints
			#between 0 and 255. Must include the "-" demarcation character
			red = random.randint(0,255)
			green = random.randint(0,255)
			blue = random.randint(0,255)

			msg = '-2-'+str(red)+'-'+str(green)+'-'+str(blue)+'-' 

		print("Constructed Message: ^%s^" %msg)	

		#Send Message to the attached Pi's
		send_message(msg)

		#Wait 6 seconds (it takes 5 seconds to fade from one color to the other)
		sleep(10)

main()
