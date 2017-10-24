from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import json, time
import random


pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-f4d521fc-b32a-11e7-8d4b-66b981d3b880'
pnconfig.publish_key = 'pub-c-c74cc51d-96d1-4126-b62e-73da4542d67b'

pubnub = PubNub(pnconfig)

def my_publish_callback(envelope, status):
    if not status.is_error():
        pass
    else:
        pass

class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass
        elif status.category == PNStatusCategory.PNConnectedCategory:
            pubnub.publish().channel("test-channel").message(messagejson).async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
    def message(self, pubnub, message):
        pass

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('test-channel').execute()

while 1:
    pubnub.publish().channel("test-channel").message({ "text": random.randint(10, 50) }).async(my_publish_callback)
    time.sleep(1)
