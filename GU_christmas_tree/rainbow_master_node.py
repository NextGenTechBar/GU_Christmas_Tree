#!/usr/bin/python

#Communication library
import pika

#Input of messages
import sys

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
	print("Sending Rainbow Colors!")
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
	
main()
