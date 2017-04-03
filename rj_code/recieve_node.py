#import needed for rabbitmq pi-to-pi connection
import pika

def exchange_scan():
    #replace with ip of host node
    ip='147.222.72.89'

    credentials = pika.PlainCredentials('ngtb','evergreen')
    parameters = pika.ConnectionParameters(host=ip, port=5672, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange='christmas', type='fanout')

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='christmas',
                       queue=queue_name)

    print(" [*] Waiting for data from christmas exchange. Press CTRL+C to exit")

    def callback(ch, method, properties, body):
        #put in i2C code to conenct to arduinos from here.
        print(" [x] %r" %body)

        #calls the sxchange_scan again, so it runs recursivley
        exchange_scan()

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    channel.start_consuming()


exchange_scan()
