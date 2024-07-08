from paho.mqtt import client as mqtt
import time
import threading

def init(mqtt_url: str, user: str, password: str, topic: str) -> mqtt.Client:
    """
    This function initializes the connection to the broker mqtt.

    Args:
        - mqtt_url (str): The url for the broker server.
        - user (str): The username for the broker server.
        - password (str): The password for the broker server.
        - topic (str): The topic for subscribe and start listening.

    Returns:
        - broker_connection (paho.mqtt.client.Client): The client object.

    Raises:
        - mysql.connector.Error: If there is an error in connecting to the database.
    """

    try:
        mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id = "ORUS_API")

        mqtt_client.username_pw_set(user, password) # Set the credentials for the broker server.
        mqtt_client.tls_set() # Set the tls for the broker server.
        mqtt_client.connect(mqtt_url, 8883) # Connect to the broker server.

        threading.Thread(target = mqtt_client.loop_forever).start() # Start the loop for the client.
        time.sleep(0.5) # Sleep for 0.5 seconds for the connection to be established.

        if mqtt_client.is_connected() is False:
            raise ConnectionRefusedError("Connection refused by the broker server.")

        else:
            return mqtt_client

    except Exception as error:
        return error
