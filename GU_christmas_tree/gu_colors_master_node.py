#!/usr/bin/python

#Communication library
import pika

#Input of messages
import sys

#Randomizer!
import random

#               Red          Blue           White
gu_colors = [ '204-0-51' , '0-45-114' , '255-255-255']

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
	#Start with solid color
	send_message('-2-255-255-255-')

	while True :
		#randomly pick index and change color
		msg = '-3-'
		
		#figure out index
		msg = msg + ('%d' %())###HERE!!

	
main()
