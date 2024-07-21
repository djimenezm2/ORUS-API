from paho.mqtt import client as mqtt
import time
import threading
from model import data_manager
import os

def init(broker_on_message: callable) -> mqtt.Client:
    """
    This function initializes the connection to the broker mqtt.

    Args:
        - broker_on_message (function): The function to be called when a message is received from the broker mqtt.

    Returns:
        - broker_connection (paho.mqtt.client.Client): The client object.

    Raises:
        - mysql.connector.Error: If there is an error in connecting to the database.
    """

    # Get the credentials from the environment variables.
    host = str(os.environ["API_MQTT_HOST"]); port = int(os.environ["API_MQTT_PORT"])
    user = str(os.environ["API_MQTT_USER"]); password = str(os.environ["API_MQTT_PASSWORD"])
    topic = str(os.environ["API_MQTT_TOPIC"])

    try:
        # Initialize the connection to the broker mqtt.
        mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id = "ORUS_API")

        mqtt_client.username_pw_set(user, password) # Set the credentials for the broker server.
        mqtt_client.tls_set() # Set the tls for the broker server.
        mqtt_client.connect(host, port) # Connect to the broker server.
        mqtt_client.subscribe(topic) # Subscribe to the topic.
        mqtt_client.on_message = broker_on_message # Set the on_message function.

        threading.Thread(target = mqtt_client.loop_forever).start() # Start the thread for the mqtt client in loop forever.
        time.sleep(0.5) # Sleep for 0.5 seconds for the connection to be established.

        if mqtt_client.is_connected() is False:
            raise ConnectionRefusedError("Connection refused by the broker server.")

        else:
            return mqtt_client

    except Exception as error: # If there is an error in connecting to the broker server.
        return error