import os, time
from sense_hat import SenseHat

def get_cpu_temp():
    res = os.popen("vcgencmd measure_temp").readline()
    temp = float(res.replace("temp=", "").replace("'C\n",""))
    return temp

sense = SenseHat()
sense.clear()
humidity = sense.get_humidity()
temp = sense.get_temperature()
cpuTemp = get_cpu_temp()
roomTemp = temp - ((cpuTemp-temp)/1.5)
roomTemp = round(roomTemp, 1)

while 1:
    north = sense.get_compass()
    north = round(north, 1)
    print("North: %s" % north)

