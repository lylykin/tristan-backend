from TTN.ttnLink import TTNDataHandler
from TTN.ttnClient import TTNClient
from pathlib import Path
import base64
from dotenv import load_dotenv 
import os

env_path = Path(__file__).resolve().parent.parent / "secret_dont_look_at_me.env"
load_dotenv(dotenv_path=env_path, override=True)

# clé et id de l'application, dans un file env pour la sécurité

ttn_application_id = os.getenv('TTN_APPLICATION_ID')
ttn_api_key_secret = os.getenv('TTN_API_KEY_SECRET')

ttn_data_handler = TTNDataHandler()

# ** Choix de la connexion MQTT ou MQTTs **
ttn_ca_cert = None  # pour connexion MQTT simple
#ttn_ca_cert = './mqtt2-ca-cert.pem'  # pour connexion MQTTs avec certificat

print("start")
# ** Initialisation de la classe TTN Client **
ttn_client = TTNClient(
    "eu1.cloud.thethings.network",
    ttn_application_id,
    ttn_api_key_secret,
    ttn_data_handler,
    ca_cert=ttn_ca_cert
)


# ttn_client.mqtt_connect()

# ** Récupération des messages stockés (Message storage) **
print()
print("** Récupération des messages stockés (depuis 5 minutes)")
ttn_client.storage_retrieve_messages(hours=10, minutes=5)  # Penser à activer le "Message storage" sur TTN


# ** Connexion MQTT(s) + Abonnement aux devices **
print()
print("** Connexion MQTT @ TTN")
ttn_client.mqtt_connect()  # Connect to TTN

# ttn.mqtt_register_device("node16")
# ttn.mqtt_register_device("node8")
ttn_client.mqtt_register_devices(['node9', 'node7'])


# ** Script en attente // Réception des Messages MQTT par le Handler **
try:
    print("[Attente au clavier]")
    input("Appuyer 2 fois sur Entrée pour arrêter le script\n\n")
except KeyboardInterrupt as ex:
    print("[Attente interrompue]")


# ** Déconnexion MQTT(s) **
print("Déconnexion de MQTT @ TTN")
ttn_client.mqtt_disconnect()

print("** Fin du script **")
