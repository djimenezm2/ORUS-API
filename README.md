# Proyecto ORUS-API

## Desarrollado por:
- David Jiménez Mora, d.jimenezm2@uniandes.edu.co, @djimenezm2
- Yafar Alletse Solano Perez, ya.solano@uniandes.edu.co, @IamYaphy

## Descripción del Proyecto

Este proyecto implementa una solución integral para la gestión y almacenamiento de datos provenientes de sensores IoT que hacen parte de el proyecto de renovación de la huerta Fenicia de la Universidad de los Andes, los cuales monitorean de manera constante distintos aspectos del ambiente en el que se encuentran ubicados, como la temperatura y la humedad del aire, así como la humedad del suelo. La solución propuesta permite a los usuarios acceder a los datos de manera segura y eficiente a través de una API REST, la cual se conecta a un bróker MQTT para recibir los mensajes enviados por los sensores y los almacena en una base de datos MySQL para su posterior consulta.

# Componentes del Proyecto

### Mosquitto Bróker MQTT

El bróker MQTT (Message Queuing Telemetry Transport) recibe los mensajes (payloads) enviados por los clientes (chips Arduino IoT) y los retransmite a los demás clientes conectados para su procesamiento. Este bróker está desplegado en `fabspacecol.uniandes.edu.co:8883`, utilizando el protocolo seguro MQTT (MQTT Secure) con un certificado SSL y requiere autenticación por usuario y contraseña.

### Base de Datos

Se diseñó una base de datos en MySQL para almacenar de manera organizada los datos obtenidos por los sensores. La API se conecta localmente a esta base de datos para responder a las consultas. La disposición de las tablas es la siguiente:

- **Tabla `data_types`**: Almacena los tipos de datos esperados relacionados con las medidas capturadas.
- **Tabla `iot_chips`**: Contiene un registro individual para cada cliente (chip IoT).
- **Tablas `ambient_temperature`, `ambient_moisture` y `soil_moisture`**: Establecen la relación entre el tipo de dato y el cliente que lo registra, así como el valor del dato y la fecha.

### API

La API está desarrollada en Python utilizando la librería Flask y sigue una arquitectura REST. Las responsabilidades de la API incluyen:

- Conectarse al Bróker MQTT para obtener y procesar los payloads enviados por los clientes IoT.
- Leer y escribir en la base de datos los datos obtenidos de los clientes.
- Responder a las consultas de los clientes de la API (aplicativos web) con los datos solicitados de manera segura y eficiente.