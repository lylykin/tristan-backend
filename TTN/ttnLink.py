import json
from pocketbase import PocketBase  # Client also works the same

# Classe TTNDataHandler qui doit avoir une méthode on_ttn_message
class TTNDataHandler:
    client : PocketBase
    
    def __init__(self, client = PocketBase('http://127.0.0.1:8090') ):
        self.client = client
        #self.parameter2 = parameter2

    # Méthode appelée lorsque le client TTN reçoit un message
    def on_ttn_message(self, message):
        #print(f"[TTNDataHandler] Données reçues par le Handler: " + str(message))
        
        #voir si on a vraiment besion de l'id et de la date du  device, mais je pense pas
        device_id = message['device_id']
        message_date = message['date']
        message_json = message['json']

        #aff_message_date = message_date.strftime("%d/%m/%Y %H:%M:%S (%Z%z)")
        #print()
        #print(f"[TTNDataHandler] {aff_message_date}: Message de {device_id} => " + str(message_json))
        print(message_json)

        self.my_method(device_id, json.__loader__(message_json))
        
    #adding recieved data in pocketbase, for the 1st phase.
    def add_data_in_pb(self, device_id, message_file : json.__loader__):
        
        #variables to adapt depending of the json build        
        data_id = "a adapter à la gueule du json"
        data_array = 'idem'
        
        #attention, les méthodes privées sont à adapter aussi
        if data_id == 'correspond aux data du sparkfun' : 
            self._add_sparkfun_data(data_array)
        else :
            self._add_gps_data(data_array)
        
        
        #print(f"[TTNDataHandler] Votre Méthode du TTNDataHandler... ['{self.parameter1}', '{self.parameter2}']")*
    def _add_sparkfun_data(self, data : list):
        
        self.client.collection("sparkfun").create(
            { "column 1 ": "value"}
            )
        
    def _add_gps_data(self, data : list):
        
        self.client.collection("gps").create(
            { "column 1 ": "value"}
            )

#idée random : si ya plein de trucs associés au fichier json : passer des truces en arguments   

# list and filter "example" collection records
#result = client.collection("example").get_list(
 #   1, 20, {"filter": 'status = true && created > "2022-08-01 10:00:00"'})

# create record and upload file to image field

#class DataManager : 
#   data_array : list
#   
#   def __init__(self, data_array,client) :
#       self.data_2_add = data_array
#       self.client = client 
#   
#   #we'll see how the data will be organized in the array
#
#        
#   def get_data(self, client, collection) :
#       data = client.collections(collection).get_list({"sparkdata"})  
#   
#   def create_table(self, client, collection : str) :
#       client.collections(collection).create()
