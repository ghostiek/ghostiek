import json

from sensor import Ultrasonic
from time import sleep
import network
from umqtt.simple import MQTTClient

with open("mqttconfig.json", "r") as mqtt_config:
    mqtt_creds = json.load(mqtt_config)

with open("wifi_config.json", "r") as wifi_config:
    wifi_creds = json.load(wifi_config)


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

mqtt_server = str.encode(mqtt_creds["server"])
client_id = str.encode(mqtt_creds["client_id"])
topic_pub = str.encode(mqtt_creds['topic_pub'])
username = str.encode(mqtt_creds["username"])
password = str.encode(mqtt_creds["password"])


def mqtt_connect():
    client = MQTTClient(client_id,
                        mqtt_server,
                        user=username,
                        password=password,
                        keepalive=3600,
                        ssl=True,
                        ssl_params={'server_hostname': mqtt_creds["server"]})
    client.connect()
    print('Connected to %s MQTT Broker' % (mqtt_server))
    return client


def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    sleep(5)
    machine.reset()


try:
    client = mqtt_connect()
except OSError as e:
    reconnect()

sns = Ultrasonic(17, 16)

while True:
    distance = sns.distance_in_cm()
    if distance:
        print('Distance:', distance, 'cm')
        client.publish(topic_pub, str.encode(str(distance)))
    sleep(5)

