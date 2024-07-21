#include <Wire.h> // Include Wire library for I2C communication
#include "Adafruit_SHTC3.h" // Include Adafruit SHTC3 library for SHTC3 sensor
#include <PubSubClient.h> // Include PubSubClient library for MQTT communication
#include <ESP8266WiFi.h> // Include ESP8266WiFi library for WiFi communication
#include <WiFiClientSecure.h> // Include WiFiClientSecure library for secure WiFi communication
#include <ArduinoJson.h> // Include ArduinoJson library for JSON object creation

// Client ID and Chip Sleep Time
#define CLIENT_ID "CLIENTE_PRUEBA_1" // Client ID (Unique for each chip client, please change it)
#define SLEEP_TIME 5 * 60000 // Sleep Time: 5 min

// Capacitive soil moisture sensor configuration
#define AOUT A0
const int airSensorValue = 620;
const int waterSensorValue = 310;
int soilMoisture = 0;
int soilMoisturePercentage = 0;

// SHTC3 Temperature and Humidity Sensor configuration
Adafruit_SHTC3 shtc3 = Adafruit_SHTC3();
sensors_event_t SHTC3AmbientMoisture, SHTC3AmbientTemp;

// WiFi configuration (Please change it to your WiFi network)
#define WIFI_NAME "ML_747"
#define WIFI_PASS "00000000"

// MQTT Broker configuration
#define MQTT_SERVER "fabspacecol.uniandes.edu.co"
#define MQTT_PORT 8883
#define MQTT_USERNAME "FabSpaceColMQTTClient"
#define MQTT_PASSWORD "mqttclientpassword"

// WiFi and MQTT Client configuration
WiFiClientSecure wifiSecureClient;
PubSubClient mqttClient(wifiSecureClient);

void setup () {
  /**
   * @brief Setup function that initializes the serial communication, sensors and MQTT Broker connection.
   * @note Uses functions connectWiFi, SHTC3SensorSetup
   * @note For further details on each function, please refer to their respective documentation.
   *
   * @return void
   */

  Serial.begin(9600); // Start serial communication with baud rate of 9600
  delay(5000); // Wait 5 seconds before proceeding

  Serial.println("Starting...");

  connectWiFi(); // WiFi connection setup
  SHTC3SensorSetup(); // SHTC3 Sensor setup

  // Load SSL certificate (Set as Insecure to avoid certificate validation)
  wifiSecureClient.setInsecure();

  // Connect to MQTT Broker
  mqttClient.setServer(MQTT_SERVER, MQTT_PORT);
}

void connectWiFi () {
  /**
   * @brief Connects to WiFi network.
   * @note It will keep trying to connect until it is successful.
   *
   * @return void
   */

  Serial.print("\nAttempting WiFi connection...");
  WiFi.begin(WIFI_NAME, WIFI_PASS); // Connect to WiFi network

  while (WiFi.status() != WL_CONNECTED) { // If connection is not successful, it will keep trying to connect indefinitely
    delay(500);
    Serial.print("\nNO WIFI CONNECTION...");
  }

  Serial.println("\n\nConnected to WiFi successfully!");
  Serial.println("Network SSID: " + WiFi.SSID());
  Serial.println("Local IP address assigned: " + WiFi.localIP().toString());
}

void SHTC3SensorSetup () {
  /**
   * @brief Setup function for SHTC3 sensor.
   * It initializes the I2C communication and checks if the sensor is connected.
   * @note It will keep trying to connect until it is successful.
   *
   * @return void
   */

  Wire.begin(4, 5); // Start I2C communication in ports D2 (GPIO4, SDA) and D1 (GPIO5, SCL)

  Serial.println("\nSetting up SHTC3 Sensor...");

  while (!shtc3.begin()) { // If sensor is not found, it will keep trying to connect until sensor is found
    Serial.println("ERROR: Couldn't find SHTC3 sensor");
    delay(500);
  }

  Serial.println("Found SHTC3 sensor!");
}

void readSoilMoistureSensor () {
  /**
   * @brief Reads soil moisture sensor value and converts it to percentage.
   * Values are stored in global variables soilMoisture and soilMoisturePercentage.
   *
   * @return void
   */

  delay(2000);
  soilMoisture = analogRead(AOUT); // Read analog value from sensor
  soilMoisturePercentage = map(soilMoisture, waterSensorValue, airSensorValue, 100, 0); // Convert analog value to percentage

  // Ensure soilMoisturePercentage is within 0-100 range
  if (soilMoisturePercentage < 0) {
    soilMoisturePercentage = 0;

  } else if (soilMoisturePercentage > 100) {
    soilMoisturePercentage = 100;
  }
}

void readSHTC3Sensor () {
  /**
   * @brief Reads SHTC3 sensor values and stores them in global variables SHTC3AmbientMoisture and SHTC3AmbientTemp.
   *
   * @return void
   */

  shtc3.getEvent(&SHTC3AmbientMoisture, &SHTC3AmbientTemp); // Read sensor values
}

void connectToMQTTBroker () {
  /**
   * @brief Connects to MQTT Broker.
   * It will keep trying to connect until it is successful.
   *
   * @return void
   */

  while (!mqttClient.connected()) { // If connection is not successful, it will keep trying to connect indefinitely
    Serial.print("\nAttempting MQTT Broker connection...");
    Serial.print("\nMQTT Broker Server: " + (String)MQTT_SERVER + " Port: " + (String)MQTT_PORT);

    if (!mqttClient.connect("ESP8266Client", MQTT_USERNAME, MQTT_PASSWORD)) { /*Connect to MQTT Broker*/
      Serial.print("\nFailed to connect to MQTT Broker, trying again in 2 seconds...\n");
      delay(2000);

    } else {
      Serial.println("\nConnected to MQTT Broker successfully!");
    }
  }
}

void publishToMQTTBroker ( String topic, String message ) {
  /**
   * @brief Publishes data to MQTT Broker
   * @param topic String with the topic to publish the message
   * @param message String with the message to publish
   * @note If mqttClient is disconnected, it will try to reconnect before publishing the data
   *
   * @return void
   */
  Serial.print("\n\nAttempting to publish data to MQTT Broker...");

  if (mqttClient.connected()) { // If mqttClient is connected, it will publish the data
    mqttClient.publish(topic.c_str(), message.c_str()); // Publish data to MQTT Broker

    Serial.println("\nData published successfully!");
    Serial.println("Topic: " + topic);
    Serial.println("Message: " + message);

  } else { // If mqttClient is disconnected, it will try to reconnect before publishing the data
    Serial.println("\nData not published, client is disconnected from MQTT broker, trying to reconnect...\n");
    connectToMQTTBroker();
    publishToMQTTBroker(topic, message); // Try to publish the data again
  }
}

void loop () {
  /**
   * @brief Loop function that reads sensor values and publishes them to MQTT Broker.
   * @note Uses functions readSoilMoistureSensor, readSHTC3Sensor, reconnectWifi, connectToMQTTBroker, publishToMQTTBroker
   * @note For further details on each function, please refer to their respective documentation.
   *
   * @return void
   */

  readSoilMoistureSensor(); // Read soil moisture sensor values
  readSHTC3Sensor(); // Read SHTC3 sensor values

  if (WiFi.status() != WL_CONNECTED) { // If WiFi connection is lost, it will try to reconnect
    Serial.print("\nWiFi connection lost, trying to reconnect...");
    connectWiFi();
  }

  if (!mqttClient.connected()) { // If mqttClient is disconnected, it will try to reconnect
    Serial.print("\nMQTT Broker connection lost, trying to reconnect...");
    connectToMQTTBroker();
  }

  float ambientMoisture = SHTC3AmbientMoisture.relative_humidity; // Get ambient moisture value
  float ambientTemp = SHTC3AmbientTemp.temperature; // Get ambient temperature value

  // Print in SN the sensor values
  Serial.print("\n" + (String)CLIENT_ID + " sensor's read results:");
  Serial.print("\nAmbient temperature: " + (String)ambientTemp + " Celsius");
  Serial.print("\nAmbient Moisture: " + (String)ambientMoisture + "%");
  Serial.print("\nSoil Moisture: " + (String)soilMoisturePercentage + "% HR");

  // Create JSON object with sensor values to publish
  StaticJsonDocument<200> doc;
  doc["CLIENT_ID"] = CLIENT_ID;
  doc["ambientTemperature"] = ambientTemp;
  doc["ambientMouisture"] = ambientMoisture;
  doc["soilMoisture"] = soilMoisturePercentage;

  // Convert JSON object into a string
  char buffer[256];
  serializeJson(doc, buffer);

  // Publish JSON string
  publishToMQTTBroker("CROPPER", buffer); // Publish data to MQTT Broker
  mqttClient.loop(); // Keep MQTT Broker connection alive

  Serial.println("\nWaiting for " + (String)(SLEEP_TIME / 60000) + " mins.");
  delay(SLEEP_TIME); // Sleep for SLEEP_TIME
}