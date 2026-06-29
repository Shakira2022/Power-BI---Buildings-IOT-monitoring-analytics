import json
import uuid
import random
import time
from datetime import datetime
from azure.eventhub import EventHubProducerClient, EventData

CONNECTION_STR = "Endpoint=sb://smartcampus-001.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=euSBKhakXKRlRtKy6Cuq7aFMiAc59PzRQ+AEhEJmVCk="
EVENT_HUB_NAME = "environment-stream"

producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STR,
    eventhub_name=EVENT_HUB_NAME
)


departments = {
    "Engineering": ["Room-1", "Room-2", "Room-3", "Room-4", "Room-5"],
    "Science": ["Room-6", "Room-7", "Room-8", "Room-9", "Room-10"],
    "IT": ["Room-11", "Room-12", "Room-13", "Room-14", "Room-15"]
}


def generate_event():
    building = random.choice(list(departments.keys()))
    room = random.choice(departments[building])

    return {
        "event_id": str(uuid.uuid4()),
        "building": building,
        "room_id": room,
        "temperature": round(random.uniform(18, 40), 2),
        "humidity": round(random.uniform(30, 90), 2),
        "air_quality": random.choice(["good", "moderate", "bad"]),
        "event_time": datetime.utcnow().isoformat()
    }

while True:
    event = generate_event()

    batch = producer.create_batch()
    batch.add(EventData(json.dumps(event)))
    producer.send_batch(batch)

    print("Env event sent:", event)
    time.sleep(2)
