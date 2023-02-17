import paho.mqtt.client as mqtt
import socket


"""This function (or "callback") will be executed when this client receives 
a connection acknowledgement packet response from the server. """

def on_connect(client, userdata, flags, rc):
    """Once our client has successfully connected, it makes sense to subscribe to
    all the topics of interest. Also, subscribing in on_connect() means that, 
    if we lose the connection and the library reconnects for us, this callback
    will be called again thus renewing the subscriptions"""

    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("claireyu/pong")
    
    #Add the custom callbacks by indicating the topic and the name of the callback handle
    client.message_callback_add("claireyu/pong", on_message_from_pong)
    

def on_message_from_pong(client, userdata, message):
   """Print integer from pong message and publish the next integer onto ping.
   """
   
   i = int(message.payload.decode())
   print("Custom callback  - Pong: ", i)
   
   # Increase integer by 1 and publish
   i += 1
   time.sleep(1)
   client.publish("claireyu/ping", f"{i}")
    

if __name__ == '__main__':    
    # create a client object
    client = mqtt.Client()
    
    # attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect
    
    """Connect using the following hostname, port, and keepalive interval (in 
    seconds). 
    
    The keepalive interval indicates when to send keepalive packets to the 
    server in the event no messages have been published from or sent to this 
    client. If the connection request is successful, the callback attached to
    `client.on_connect` will be called."""
    client.connect("172.20.10.4", port=1883, keepalive=60)

    
    # Start by publishing a 1
    i = 1
    client.publish("claireyu/ping", f"{i}")
    
    # Loop indefinitely 
    client.loop_forever()
        
        
