import paho.mqtt.client as mqtt
import sys, time, os, urlparse
from UAP1Actions import UAP1Actions
from UAP1States import UAP1States

UPDATE_TIME = 5*60 # 5 min

# Inspired from https://www.cloudmqtt.com/docs/python.html

server_uri = os.environ.get('MQTT_SERVER', 'mqtt://localhost:1883')
username = os.environ.get('MQTT_USERNAME', None)
password = os.environ.get('MQTT_PASSWORD', None)
clientid = os.environ.get('MQTT_CLIENT_ID', None)

topic_status_light = 'state/{}/light'.format(clientid)
topic_status_door = 'state/{}/door'.format(clientid)

topic_command_light = 'command/{}/light'.format(clientid)
topic_command_door = 'command/{}/door'.format(clientid)

server_parsed = urlparse.urlparse(server_uri)

mqttc = mqtt.Client(client_id=clientid)
if username and password :
    mqttc.username_pw_set(username, password=password)
mqttc.connect(server_parsed.hostname, port=server_parsed.port, keepalive=60)

ustates = UAP1States(36, 38, 40)
uactions = UAP1Actions(29, 31, 33, 35)

def on_connect(client, userdata, flags, rc):
    pass
    #print("rc: " + str(rc))

def on_message(client, obj, msg):
    #print("received message: {} -- {} -- retained {}".format(msg.topic,
    #                                          msg.payload, msg.retain))
    fmt_date = time.strftime("%Y-%m-%d %H:%M")
    if not msg.retain:
        rcv = msg.payload.lower()
        force_update = True
        if msg.topic == topic_command_light:
            if ustates.get_str_light().lower() != rcv:
                uactions.light()
        if msg.topic == topic_command_door:
            if ustates.get_str_door().lower() != rcv:
                print("[{}] Received {} command".format(fmt_date, rcv))
                if rcv == "close":
                    uactions.close()
                if rcv == "open":
                    uactions.open()
                if rcv == "slight":
                    uactions.slightly_open()

def on_publish(client, obj, mid):
    pass
    #print("pulbish: {}, {} ".format(obj, mid))

def on_subscribe(client, obj, mid, granted_qos):
    pass
    #print("Subscribed: {}, {}, {}".format(mid, granted_qos, obj))

def on_log(client, obj, level, string):
    print(string)

mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Uncomment to enable debug messages
#mqttc.on_log = on_log

# Start subscribe
mqttc.subscribe(topic_command_light, qos=0)
mqttc.subscribe(topic_command_door, qos=0)

# Monitor states + mqtt loop
rc = 0
last_door_state = None
last_light_state = None
last_light_update = time.time() - UPDATE_TIME
last_door_update = time.time() - UPDATE_TIME
force_update = False

time.sleep(1)
while rc == 0:
    door_state = ustates.get_door()
    light_state = ustates.get_light()
    curr_time = time.time()
    fmt_date = time.strftime("%Y-%m-%d %H:%M")
    if last_door_state != door_state or curr_time - last_door_update > UPDATE_TIME or force_update:
        last_door_update = time.time()
        last_door_state = door_state
        print("[{}] publishing new door state {}".format(fmt_date, ustates.get_str_door()))
        mqttc.publish(topic_status_door, ustates.get_str_door())
    if last_light_state != light_state or curr_time - last_light_update > UPDATE_TIME or force_update:
        last_light_update = time.time()
        last_light_state = light_state
        print("[{}] publishing new light state {}".format(fmt_date, ustates.get_str_light()))
        mqttc.publish(topic_status_light, ustates.get_str_light())
    force_update = False
    rc = mqttc.loop()
    time.sleep(0.3)
print("[{}] exited ! rc: {}".format(fmt_date, rc))

