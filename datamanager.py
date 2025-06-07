from ttnLink import TTNDataHandler
from ttnClient import TTNClient
from ttnClient import TTNClient
#from subscribeData import PBdataListener
import base64
from dotenv import load_dotenv 
import os
import paho.mqtt.client as mqtt

# clé et id de l'application, dans un file env pour la sécurité
load_dotenv(dotenv_path="secret_dont_look_at_me.env")
ttn_application_id = os.getenv('TTN_APPLICATION_ID')
ttn_api_key_secret = os.getenv('TTN_API_KEY_SECRET')

ttn_data_handler = TTNDataHandler()

# Récupération de l'écoute de modification PocketBase
#pb_data_listener = PBdataListener()
#pb_data_listener.subscribe_sparkfun()

# ** Choix de la connexion MQTT ou MQTTs **
ttn_ca_cert = None  # pour connexion MQTT simple
#ttn_ca_cert = './mqtt2-ca-cert.pem'  # pour connexion MQTTs avec certificat

#print("start")
## ** Initialisation de la classe TTN Client **
ttn_client = TTNClient(
    "eu1.cloud.thethings.network:1883",
    ttn_application_id,
    ttn_api_key_secret,
    ttn_data_handler,
    ca_cert=ttn_ca_cert
)

#ttn_client.mqtt_connect()

client = mqtt.Client()
client.username_pw_set(ttn_application_id + "@ttn", ttn_api_key_secret)
# client.tls_set(ca_certs=ca_cert) # (cas du MQTTS)

# Paramètres de connexion
broker = "eu1.cloud.thethings.network"  # Adresse du broker MQTT (ou MQTTs)
port = 1883
topic = "#" # tous les topics

def on_connect_callback(client, userdata, flags, rc):
    print("Connecté au serveur MQTT")
    client.subscribe(topic)

#cas variable si on est en phase de construction de la bdd(1) ou de comparaison des data à la bdd(2)

stage = int(input("stage du projet : "))

if stage == 1:
    client.on_connect = on_connect_callback
    client.on_message = ttn_data_handler.on_ttn_message_s1
    #client.on_message = on_message  
else : 
    client.on_connect = on_connect_callback
    client.on_message = ttn_data_handler.on_ttn_message_s2 
    #client.on_message = on_message


client.connect(broker, port, 60)
client.loop_forever()
