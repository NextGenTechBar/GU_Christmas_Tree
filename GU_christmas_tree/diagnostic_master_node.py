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
	#Initilize Message to be just the "-" demarcation character
	msg = '-'	

	#Grab All of the command line args
	#This does not check anything, just passes them straight through
	for i in range(1,len(sys.argv)):
		print("%d cmd: %r " %(i, sys.argv[i]))	
		#Append arguments to message with a "-" character inbetween everything
		msg = msg+sys.argv[i]+'-'
	
	print("Constructed Message: ^%s^" %msg)	

	#Send Message to the attached Pi's
	send_message(msg)

main()
