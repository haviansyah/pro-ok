import pika

class MQ():
     
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) # Buat Koneksi Ke RMQ
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='web_status') #Declaring Queue dan buat queue durable
        self.channel.queue_declare(queue='lda_queue',durable=True) #Declaring Queue dan buat queue durable
        
    def run(self,callback):
        self.channel.basic_qos(prefetch_count=1) # Buat memastikan rmq ngasih task 1 dulu sampe kelar ke worker
        self.channel.basic_consume(queue='lda_queue', on_message_callback=callback)
        self.channel.start_consuming()


def run(callback):
    mq = MQ()
    mq.run(callback)