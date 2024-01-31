import json

from sensor import Ultrasonic
import utime
import network
from umqtt.simple import MQTTClient

with open("wifi_config.json", "r") as wifi_config:
    wifi_creds = json.load(wifi_config)

with open("mqtt_config.json", "r") as mqtt_config:
    mqtt_creds = json.load(mqtt_config)


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(wifi_creds["username"], wifi_creds["password"])
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


do_connect()

mqtt_ip = str.encode(mqtt_creds["ip"])
mqtt_port = mqtt_creds["port"]
client_id = str.encode(mqtt_creds["client_id"])
topic_pub = str.encode(mqtt_creds['topic_pub'])
username = str.encode(mqtt_creds["username"])
password = str.encode(mqtt_creds["password"])


client = MQTTClient(client_id, mqtt_ip, port=mqtt_port, user=username, password=password)
sns = Ultrasonic(17, 16)


while True:
    try:
        client.connect()
        distance = sns.distance_in_cm()
        if distance:
            print('Distance:', distance, 'cm')
            client.publish(topic_pub, str.encode(str(distance)))
        client.disconnect()
        utime.sleep(5)
    except Exception as e:
        print(e)
        pass
    

