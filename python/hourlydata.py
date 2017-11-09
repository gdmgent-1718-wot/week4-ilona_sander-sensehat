from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
import os, json, time, sys
import pygame
from pygame.locals import *
from sense_hat import SenseHat

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-f4d521fc-b32a-11e7-8d4b-66b981d3b880'
pnconfig.publish_key = 'pub-c-c74cc51d-96d1-4126-b62e-73da4542d67b'
pnconfig.uuid = 'PI'
pubnub = PubNub(pnconfig)
datachannel = "constant-data"

pygame.init()
size = width, height = 320, 240
speed = [2, 2]
black = 0, 0, 0
screen = pygame.display.set_mode(size)

sleepcount = 0
hourlymark = 3600

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
            pubnub.publish().channel(datachannel).message(messagejson).async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
    def message(self, pubnub, message):
        pass

pubnub.subscribe().channels(["hourly-data", "constant-data"]).execute()
pubnub.add_listener(MySubscribeCallback())

try:
    while 1:
        def get_cpu_temp():
            res = os.popen("vcgencmd measure_temp").readline()
            temp = float(res.replace("temp=", "").replace("'C\n",""))
            return temp

        sense = SenseHat()
        sense.clear()
        humidity = sense.get_humidity()
        temp = sense.get_temperature()
        pressure = sense.get_pressure()
        north = sense.get_compass()
        north = round(north, 1)

        cpuTemp = get_cpu_temp()
        roomTemp = temp - ((cpuTemp-temp)/1.5)
        roomTemp = round(roomTemp, 1)

        # humidity in %
        # temperature in C
        # pressure in Millibars
        
        if sleepcount == hourlymark - 1:
            datachannel = "hourly-data"

        messagejson = {
            "channel": datachannel,
            "humidity": str(humidity),
            "temperature": str(roomTemp),
            "pressure": str(pressure),
            "north": str(north)
        }
        
        pubnub.publish().channel(datachannel).message(messagejson).sync()
        
        sleepcount += 1
        if sleepcount == hourlymark:
            sleepcount = 0
            datachannel = "constant-data"
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                try:
                    sys.exit()
                except SystemExit:
                    os._exit(0)
            
        screen.fill(black)
            
        time.sleep(1)

except KeyboardInterrupt:
    print('The program was interrupted. Unsubscribing from channel and shutting down...')
    pubnub.unsubscribe().channels(["hourly-data", "constant-data"]).execute()
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

