import paho.mqtt.client as mqtt
import db_utils as db
import json

with open("../pico/mqtt_config.json", "r") as mqtt_file:
    mqtt_config = json.load(mqtt_file)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(mqtt_config["topic_pub"])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    conn = db.connect_db()
    cur = conn.cursor()
    db.send_data(conn, cur, msg.payload)
    conn.close()
    

client = mqtt.Client()
client.username_pw_set(username=mqtt_config["username"], password=mqtt_config["password"])
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", mqtt_config["port"], 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
