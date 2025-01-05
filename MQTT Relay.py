# python 3.11
 
import random
from paho.mqtt import client as mqtt_client
# from paho.mqtt import publish as publish  # Not needed if we always use client
from buildhat import Matrix, ForceSensor
 
##############################################################################
#                         GLOBAL VARIABLES / SETUP                           #
##############################################################################
 
# -----------------------#
# MQTT Configuration    #
# -----------------------#
broker = 'XXX.XXX.XXX.XXX'     # IP of your broker
port = 1883                 # Port for MQTT (default is 1883)
topic = "test/relay"        # Topic to subscribe/publish to
 
# We create a random ID just so multiple clients on the same broker
# don't stomp on each other:
client_id = f'subscribe-{random.randint(0, 100)}'
 
# Username / password for the broker (if needed)
username = 'YOURUSERNAME'
password = 'YOURPASSWORD'
 
# -----------------------#
# BuildHat Configuration #
# -----------------------#
# Create a matrix on port 'B' (adjust as needed for your setup)
matrix = Matrix('B')
matrix.clear(("yellow", 10))
 
# Create a ForceSensor on port 'C'
button = ForceSensor('C')
 
# This will indicate the relay state:
buttonFlag = 1
 
# -----------------------#
# The Big Global Client  #
# -----------------------#
#
# We declare 'client' here. We'll fill it in `connect_mqtt()`.
# This is so that any function that needs it can do `global client`.
client = None
 
 
##############################################################################
#                            MQTT SETUP FUNCTIONS                            #
##############################################################################
 
def connect_mqtt():
    """
    Connects to the MQTT broker exactly once and assigns the resulting
    mqtt_client.Client instance to the global 'client'.
    Returns the same client, but we also store it in the global variable.
    """
    global client  # Tells Python we're referring to the global variable above.
 
    def on_connect(client, userdata, flags, rc):
        """
        Callback that fires when a connection to the broker is established.
        """
        if rc == 0:
            print("Connected to MQTT Broker!")
            # As an example, we publish a greeting on a different topic:
            client.publish("test/time", "HI from PI!")
        else:
            print(f"Failed to connect. Return code={rc}")
 
    # Actually create the client object
    client = mqtt_client.Client(client_id)
 
    # Assign credentials
    client.username_pw_set(username, password)
 
    # Assign the on_connect callback
    client.on_connect = on_connect
 
    # Connect to the broker
    client.connect(broker, port)
 
    return client
 
 
def subscribe():
    """
    Sets up subscription to a topic and defines how incoming messages are handled.
    """
    global client  # We'll need the client to call subscribe on it
 
    def on_message(client, userdata, msg):
        """
        Callback that fires when a message arrives on a topic we subscribed to.
        """
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        
        # If the received payload is '1', turn the matrix green, else red.
        # (Adjust logic if your messages are strings other than '1'/'0')
        if msg.payload.decode() == '1':
            matrix.clear(("green", 10))
        else:
            matrix.clear(("red", 10))
 
    # Subscribe to the desired topic
    client.subscribe(topic)
 
    # Assign the on_message callback
    client.on_message = on_message
 
 
 ##############################################################################
#                       FUNCTIONS TO PUBLISH MESSAGES                        #
##############################################################################
 
def publish_message():
    """
    Publishes the current state of 'buttonFlag' to the MQTT broker.
    """
    global client  # We'll need the global client
    print("Publishing message:", buttonFlag)
    client.publish(topic, buttonFlag)
 
 
##############################################################################
#                        BUILDHAT BUTTON-RELATED CODE                        #
##############################################################################
 
def handle_pressed(force):
    """
    Called automatically when the ForceSensor on port 'C' is pressed.
    We'll flip the buttonFlag from 1 to 0 or 0 to 1 and then publish.
    """
    global buttonFlag  # Tells Python to use the global variable
    if force > 10:
        print("Button Pressed!")
        # Flip the state of buttonFlag
        if buttonFlag == 1:
            buttonFlag = 0
            matrix.clear(("red", 10))
        else:
            buttonFlag = 1
            matrix.clear(("green", 10))
 
        # Now publish our updated buttonFlag via MQTT
        publish_message()
 
 
##############################################################################
#                             MAIN LOOP (run)                                #
##############################################################################
 
def run():
    """
    Main entry-point for our script. Connect to MQTT, subscribe, 
    and start the loop forever.
    """
    global client  # We'll store the client in the global variable
    
    # 1. Connect once
    connect_mqtt()
    
    # 2. Subscribe once
    subscribe()
    
    # 3. Start an infinite loop to process messages and keep the connection open
    client.loop_forever()
 
 
# Assign our 'handle_pressed' function to be called when the ForceSensor is pressed
button.when_pressed = handle_pressed
 
 
##############################################################################
#                          START THE PROGRAM HERE                            #
##############################################################################
 
if __name__ == '__main__':
    run()
