import pika
import uuid
import json
import threading
from mq.constant import *
import datetime
import os
from resources.global_var import get_current_state,edit_current_state
# from flask import current_app as app

queue = {}

class MQ():
     
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ['RABBITMQ_HOSTNAME'])) # Buat Koneksi Ke RMQ
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='web_status') #Declaring Queue dan buat queue durable
        self.channel.queue_declare(queue='lda_queue',durable=True) #Declaring Queue dan buat queue durable
        result = self.channel.queue_declare(queue='',durable=True,exclusive=True) #Declaring Queue dan buat queue durable
    
    def call(self, data):
        self.response = None
        message = json.dumps(data)
        self.corr_id = str(uuid.uuid4())
        queue[self.corr_id] = None
        self.channel.basic_publish(
            exchange='',
            routing_key='lda_queue',
            properties=pika.BasicProperties(
                delivery_mode = 2 # make messages persistent
            ),
            body=message)

        #Kirim Status Training
        self.channel.exchange_declare(exchange='logs', exchange_type='fanout') 

        message = {"status" : "training"}
        message = json.dumps(message)
        self.channel.basic_publish(exchange='',routing_key='web_status',body=message)
        self.connection.close()
        return True


def sendTrain(data):
    edit_current_state()
    mq = MQ()
    data = {
        "type" : "TRAIN",
        "payload" : data
    }
    try :
        threading.Thread(target=mq.call, args=(data,)).start()
        return True

    except Exception as e :
        print(e)    

def sendReTrain():
    edit_current_state()
    mq = MQ()
    data = {
        "type" : "RETRAIN"
    }
    try :
        threading.Thread(target=mq.call, args=(data,)).start()
        return True

    except Exception :
        print(Exception)    