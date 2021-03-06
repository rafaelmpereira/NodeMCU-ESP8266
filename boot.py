from umqtt.simple import MQTTClient
from machine import Pin
import time
from wifi import conectar         #file .py
from testedht import readDHT11    #file .py

"""
#                   Almir                                 Rafael                                    Stefano
clientid = ["aa07e300-803f-11ea-883c-638d8ce4c23d", "bf401e30-a656-11ea-93bf-d33a96695544", "a2c20010-a657-11ea-883c-638d8ce4c23d"]
# channels PUB
channel = ["1","2","3"]
# channels SUB
channel = ["5","6","7"]
"""
# Cayenne Definition
server = "mqtt.mydevices.com"
clientid = "bf401e30-a656-11ea-93bf-d33a96695544"
username = "d6033960-7df0-11ea-a67f-15e30d90bbf4"
password = "99e45f8e4ef9ef46f3bc0c42e4d0317e5bb523cb"

led = Pin(2, Pin.OUT)       # on ESP12E (not ESP32), LED is in GPIO 2
rele = Pin(15, Pin.OUT)
led.value(1)                # on ESP12E (not ESP32), LED is off with level HIGH
rele.value(0)
type = "temp"
unit = "c"
channel = 2
channelSub = 6
value = readDHT11()
topicPub = ("v1/%s/things/%s/data/%s" % (username, clientid, channel))
topicSub = ("v1/%s/things/%s/cmd/%s" % (username, clientid, channelSub))

#conectar()          #wifi
c.disconnect()       #if previously connected to cayenne
c = MQTTClient(clientid,server,0,username,password)
c.connect()

# sending data to channel
def pub():
  message = ("%s,%s=%s" %(type,unit,value))
  c.publish(topicPub,message)
  print("Enviado:", value)
  led.value(not led.value())
  sleep(0.2)
  led.value(not led.value())
  
# receiving data from channel
def sub():
  def sub_cb(topic, msg):
    p = msg.decode().split(',')
    print('Recebido: ',p[1])
    #sending status
    c.publish("v1/%s/things/%s/digital/%s" % (username, clientid, channelSub),"%s" %(p[1]))
    #sending actuator is ok
    c.publish("v1/%s/things/%s/response" % (username, clientid),"ok,%s" %(p[0]))
    # code to act on relay
    if str(p[1]) = "1":
      if int(value) >= 30:    
        rele.value(1)       #turn relay ON
      else:
        rele.value(0)       # turn relay OFF
  c.set_callback(sub_cb)
  c.subscribe(topicSub)

while True:
  sub()
  sleep(0.1)
  pub()
  sleep(2)
