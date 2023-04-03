import sys
import pika
from mongoengine import connect, DoesNotExist
from models import Contact

connect(host='mongodb+srv://hw8:567432@cluster0.g08jtiw.mongodb.net/contacts?retryWrites=true&w=majority')

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='email_queue')

    def callback(ch, method, properties, body):
        try:
            contact_id = body.decode()
            contact = Contact.objects.get(id=contact_id)
            print(f'Sending email message to {contact.email}')
            contact.message_sent = True
            contact.save()
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except DoesNotExist:
            print(f'Contact with id {body.decode()} does not exist')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='email_queue', on_message_callback=callback)
    print('Waiting for email messages...')
    channel.start_consuming()
    
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)