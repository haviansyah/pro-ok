import mq.mq
from mq.constant import *
import json
import pika
import time
from ml.controller import trainFromDB, preprocessing

def retrain():
    print("Retraining")
    trainFromDB()


def training(data):
    print("Preprocessing & Training")
    preprocessing(data)


def callback(ch, method, props, body):
    start_time = time.time()
    print("[X] Received %r " % body)
    message_data = json.loads(body)
    type = message_data["type"]

    if type == "RETRAIN" : retrain()
    elif type == "TRAIN" : training(message_data["payload"])
    
    finish_time = time.time()
    print("--- %s seconds ---" % (finish_time-start_time))
    ch.exchange_declare(exchange='logs', exchange_type='fanout')

    message = {"status" : "active"}
    message = json.dumps(message)
    ch.basic_publish(exchange='',routing_key='web_status',body=message)
    ch.basic_ack(delivery_tag=method.delivery_tag)

print("Worker Started CTRL + C to quit")
mq.mq.run(callback)