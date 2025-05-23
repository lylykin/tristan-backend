from pocketbase import PocketBase  # Client also works the same
import ast
from dotenv import load_dotenv 
import os
from knn import KNN

# Classe TTNDataHandler qui doit avoir une méthode on_ttn_message
class TTNDataHandler:
    client : PocketBase
    
    def __init__(self, client = PocketBase('http://127.0.0.1:8090')):
        load_dotenv(dotenv_path="secret_dont_look_at_me.env")
        
        self.client = client
        self.super_user = self.client.admins.auth_with_password(os.getenv('SUPER_ID'), os.getenv('SUPER_PASS'))

    # Méthode appelée lorsque le client TTN reçoit un message
    def on_ttn_message_s1(self, client, userdata, msg):
        
        #converts the recieved data as a dict
        message = ast.literal_eval(msg.payload.decode())
        print(message)
        
        
        #voir si on a vraiment besion de l'id et de la date du  device, mais je pense pas
        #device_id = message['device_id']
        # message_date = message['time']
        #message_json = message['json']

        #aff_message_date = message_date.strftime("%d/%m/%Y %H:%M:%S (%Z%z)")
        try : 
            dico_payload = message['uplink_message']['decoded_payload']           
            if list(dico_payload.keys())[0] == 'A' : 
                self._add_sparkfun_data_s1(list(dico_payload.keys()), list(dico_payload.values()))
            else :
                self._add_gps_data(list(dico_payload.keys()), list(dico_payload.values())) 
        except : 
            pass   

    def _add_sparkfun_data_s1(self, data_keys : list, data_values : list,):
        
            material = str(input("saisir le matériau du déchet : "))
        
            self.client.collection("sparkfun").create(
                {
                'material' : material,
                 data_keys[0] : data_values[0],
                 data_keys[1] : data_values[1],
                 data_keys[2] : data_values[2],
                 data_keys[3] : data_values[3],
                 data_keys[4] : data_values[4],
                 data_keys[5] : data_values[5],
                 data_keys[6] : data_values[6],
                 data_keys[7] : data_values[7],
                 data_keys[8] : data_values[8],
                 data_keys[9] : data_values[9],
                 data_keys[10] : data_values[10],
                 data_keys[11] : data_values[11],
                 data_keys[12] : data_values[12],
                 data_keys[13] : data_values[13],
                 data_keys[14] : data_values[14],
                 data_keys[15] : data_values[15],
                 data_keys[16] : data_values[16],
                 data_keys[17] : data_values[17],               
                 }
            )
        
    def _add_gps_data(self, data_keys : list, data_values : list):
        self.client.collection("gps").create(
            {data_keys[0] : data_values[0],
             data_keys[1] : data_values[1],
             data_keys[2] : data_values[2],
                }
            )
        
    def on_ttn_message_s2(self, message : dict) :
        """
        Non implémentée car pas la priorité pour l'instant
        est techniquement la meme fonction que la version s1, mais vu que est utilisée en tant que callback, je suis obligée de faire comme ca
        """
        dico_payload = message['data']['uplink_message']['decoded_payload']
        print(dico_payload)
        
        if list(dico_payload.keys())[0] == 'A' : 
            self._spark_knn(list(dico_payload.keys()), list(dico_payload.values()))
        else :
            self._add_gps_data(list(dico_payload.keys()), list(dico_payload.values()))   
    
    def _spark_knn(self, dico_data : dict) : 
        """
        doit retourner le matériau identifié par le knn
        """
        data_list = list(dico_data.values())
        #getting all the recyclable materials. might be a bit bruteforce but thats a first try
        materials = self.client.collection("material").get_full_list(
            {"filter": 'recyclable = true'})
        print(materials)
        data_test = self.client.collection("sparkfun").get_full_list()

        #je ne sais pas quel type de data est renvoyé par ca 
        #mais voila l'idée du truc, à adapter ensuite

        ident = KNN(data_list)
        #adding the data test to the knn.there might be a way to set it as default, so that it doesnt compute each time. but again its a first idea
        ident.addKnnData(data_test)
        id_material = ident.knn()
        #for now it is a print. plus tard, l'ajouter dans l'historique de l'user, et le récupérer comme ca pour le frontend
        print(id_material)


test=  TTNDataHandler()
data = {'uplink_message' : {'decoded_payload' : {'A' : 1, 'B' : 1, 'C' : 1}}}

test.on_ttn_message_s2()
        
    


