import paho.mqtt.subscribe as subscribe
from influxdb import InfluxDBClient
from datetime import datetime

#time setup
now = datetime.now()
dt_string = now.strftime("%Y-%m-%dT%H:%M:%S")
date_string = now.strftime("%Y-%m-%d")
databasename = f'smoker-{date_string}'
print(f"databasename:{databasename}")

topics = ['outTopic','smoker/temp','smoker/WiFi/#']

#database setup
client = InfluxDBClient(host='tanukimario', port=8086)
for databases in client.get_list_database():
    if databases['name'] == databasename:
        print("there's a match!")
    else:
        client.create_database(databasename)
client.switch_database(databasename)

while True:
    msg = subscribe.simple(topics, hostname="tanukimario.mushroomkingdom", retained=False, msg_count=2) #in order not to miss any messages you will want msg_count to equal the max number of messages you expect to be sent at once.
    for message in msg:
        if message.topic == "smoker/temp":
            tempC = int(message.payload)
            tempF = 9.0/5.0 * int(message.payload)+32
            print(f'{message.topic}:{tempC}° C')
            print(f'{message.topic}:{tempF}° F')
            now = datetime.utcnow()
            dt_string = now.strftime("%Y-%m-%dT%H:%M:%SZ")
            data = [{"measurement":"smoker data", "time":f"{dt_string}", "fields":{"temperature":f"{tempF}", "Fan Speed":"not a real value yet"}}]
            client.write_points(data)
        else:
            print(f'{message.topic}:{message.payload}')