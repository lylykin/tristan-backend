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

# ** Récupération des messages stockés (Message storage) **
#print()
#print("** Récupération des messages stockés (depuis 5 minutes)")
#ttn_client.storage_retrieve_messages(minutes=5)  # Penser à activer le "Message storage" sur TTN


# ** Connexion MQTT(s) + Abonnement aux devices **
#print()
#print("** Connexion MQTT @ TTN")
#ttn_client.mqtt_connect()  # Connect to TTN

# ttn.mqtt_register_device("node16")
# ttn.mqtt_register_device("node8")
# ttn_client.mqtt_register_devices(['node9', 'node7'])


# ** Script en attente // Réception des Messages MQTT par le Handler **
#try:
#    print("[Attente au clavier]")
#    input("Appuyer 2 fois sur Entrée pour arrêter le script\n\n")
#except KeyboardInterrupt as ex:
#    print("[Attente interrompue]")


# ** Déconnexion MQTT(s) **
#print("Déconnexion de MQTT @ TTN")
#ttn_client.mqtt_disconnect()#
#
#print("** Fin du script **")

# Paramètres de connexion
broker = "eu1.cloud.thethings.network"  # Adresse du broker MQTT (ou MQTTs)
port = 1883
topic = "#" # tous les topics

def on_connect(client, userdata, flags, rc):
    print("Connecté au serveur MQTT")
    client.subscribe(topic)

#def on_message(client, userdata, msg):
#   print(f"Message reçu : {msg.topic} -> {msg.payload.decode()}")
#   print(type(msg.payload.decode()))

#cas variable si on est en phase de construction de la bdd(1) ou de comparaison des data à la bdd(2)

stage = 2

if stage == 1:
    client.on_connect = on_connect
    client.on_message = ttn_data_handler.on_ttn_message_s1
    #client.on_message = on_message  
else : 
    client.on_connect = on_connect
    client.on_message = ttn_data_handler.on_ttn_message_s2 #n'existe pas encore mais c'est pas la priorité
    #client.on_message = on_message


client.connect(broker, port, 60)
client.loop_forever()
