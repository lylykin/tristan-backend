from pocketbase import PocketBase
from dotenv import load_dotenv 
import os
from random import randint

class PBdataListener:
    def __init__(self):
        # id et mdp de l'admin, dans un file env pour la sécurité
        load_dotenv(dotenv_path="secret_dont_look_at_me.env")
        admin_id_secret = os.getenv('SUPER_ID')
        admin_pass_secret = os.getenv('SUPER_PASS')

        self.client = PocketBase('http://127.0.0.1:8090')

        # (Optionally) authenticate
        #user_data = client.collection('users').auth_with_password('test@example.com', '123456')
        #user_data.is_valid
        # as admin
        self.admin_data = self.client.admins.auth_with_password(admin_id_secret, admin_pass_secret)
        self.admin_data.is_valid

    # Traitement des changements
    def on_change(event) : 
        print(event["action"]) 
        print(event["record"])

    # Subscribe to changes in any sparkfun record
    def subscribe_sparkfun(self):
        # Récupération des changements
        self.client.collection('sparkfun').subscribe(

        #'*', # Sujet (nom de la ligne (ex : 'RECORD_ID'), ou toutes les lignes : *) NON NECESSAIRE EN PYTHON (méthodes différentes ligne/collection)
        callback=self.on_change
        )
        self.client.collection("sparkfun").update(
            "f8j9py6i289vvce",
            {
                'material' : "test1",
                 'A' : randint(0,200),
                 'B' : randint(0,200),
                 'C' : randint(0,200),
                 'D' : randint(0,200),
                 'E' : randint(0,200),
                 'F' : randint(0,200),
                 'G' : randint(0,200),
                 'H' : randint(0,200),
                 'I' : randint(0,200),
                 'J' : randint(0,200),
                 'K' : randint(0,200),
                 'L' : randint(0,200),
                 'R' : randint(0,200),
                 'S' : randint(0,200),
                 'T' : randint(0,200),
                 'U' : randint(0,200),
                 'V' : randint(0,200),             
                 }
        )

        # Unsubscribe
        #client.collection('sparkfun').unsubscribe('RECORD_ID') # remove all 'RECORD_ID' subscriptions
        #client.collection('sparkfun').unsubscribe('*') # remove all '*' topic subscriptions
        #client.collection('sparkfun').unsubscribe() # remove all subscriptions in the collection