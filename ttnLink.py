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
        
        try : 
            dico_payload = message['uplink_message']['decoded_payload']           
            if list(dico_payload.keys())[0] == 'A' : 
                self._add_sparkfun_data_s1(list(dico_payload.keys()), list(dico_payload.values()))
            else :
                self._add_gps_data(list(dico_payload.keys()), list(dico_payload.values())) 
        except : 
            pass   

    def _add_sparkfun_data_s1(self, data_keys : list, data_values : list,):

            # On demande les informations lors du remplissage de la bdd
            material_input = str(input("saisir le matériau du déchet : "))
            #objet_input = str(input("saisir l'objet associé au déchet : "))
            #borne_input = "h6h259zvkm8a53x" # On suppose que la borne utilisée sera la seule existante
            #user_id_input = os.getenv('SUPER_ID') # On suppose que le seul superuser rentre les data

            #materials_list = self.client.collection("materiau").get_full_list()
            #contained = False # Tiens compte si le matériau est dans la bdd
            #for mat in materials_list :
            #    if material_input == mat['nom_materiau'] : # On suppose que les nom_materiau sont uniques pour chaque materiau
            #        material_id = mat['id']
            #        contained = True
            #if not contained : # Si le matériau entré n'existe pas dans la bdd, l'ajouter
            #    self.client.collection("materiau").create(
            #        {
            #        'nom_materiau' : material_input,
            #        'recyclabilite' : str(input("saisir la recyclabilite du materiau (True/False) : ")),
            #        }
            #    )
            #material = material_input
#
            #objets_list = self.client.collection("objet").get_full_list()
            #if objet_input not in objets_list : # Si l'objet entré n'existe pas dans la bdd, l'ajouter
            #    self.client.collection("objet").create(
            #        {
            #        'nom_objet' : objet_input,
            #        'user' : user_id_input,
            #        'materiau' : material_id,
            #        }
            #    )
            #objet = objet_input
#
        
            #'borne' : borne_input,
            #'objet' : objet,
            print("insertion en cours...")
            
            data_dict = {'material' : material_input,
            data_keys[0] : data_values[0], # A
            data_keys[1] : data_values[1], # B
            data_keys[2] : data_values[2], # C
            data_keys[3] : data_values[3], # D
            data_keys[4] : data_values[4], # E
            data_keys[5] : data_values[5], # F
            data_keys[6] : data_values[6], # G
            data_keys[7] : data_values[7], # H
            data_keys[8] : data_values[8], # I
            data_keys[9] : data_values[9], # J
            data_keys[10] : data_values[10], # k
            data_keys[11] : data_values[11], # L
            data_keys[12] : data_values[12], # R
            data_keys[13] : data_values[13], # S
            data_keys[14] : data_values[14], # T
            data_keys[15] : data_values[15], # U
            data_keys[16] : data_values[16], # V
            data_keys[17] : data_values[17], # W               
            }
            print(data_dict)
            self.client.collection("sparkfun").create()
        
    def _add_gps_data(self, data_keys : list, data_values : list):
        self.client.collection("borne").update(
            {'lat_actuel' : data_values[1], # lat
             'long_actuel' : data_values[2], # longitude
            }
        )
        
    def on_ttn_message_s2(self, client, userdata, msg) :
        
        message = ast.literal_eval(msg.payload.decode())
        
        #le try except sert à la gestion des erreurs. Si                                                                                                                                                                                                                                                   
        try : 
            dico_payload = message['uplink_message']['decoded_payload']
            print(dico_payload)

            if list(dico_payload.keys())[0] == 'A' : 
                print('test bon : le message est correctement formaté')
                self._spark_knn(list(dico_payload.keys()), list(dico_payload.values()))
                
            else :
                self._add_gps_data(list(dico_payload.keys()), list(dico_payload.values()))   
        except :
            print('bouhouhouuu')
            pass 
        
    def decode(self, val):
        
        if val.expand == {}: 
            return val  
        val.material = val.expand['material']
        return val 
         
    def _spark_knn(self, dico_data : dict) : 
        """
        doit retourner le matériau identifié par le knn
        """
        data_list = list(dico_data.values())
        print(f'liste des données : {data_list}')
        #récupération des records en brut
        materials = self.client.collection("sparkfun").get_full_list(100,
            {"expand": 'material'})
        
        pb_data = []
        for mat in materials: 
            pb_data.append(self.decode(mat).l)
        print(f'pb_data : {pb_data}')
            

                
        print(materials)
        #identification
        print("Identification du matériau en cours")
        ident = KNN(data_list)

        ident.addKnnData(pb_data, None)
        id_material = ident.knn()
        #for now it is a print. plus tard, l'ajouter dans l'historique de l'user, et le récupérer comme ca pour le frontend
        print(f"ifentificaation terminée. le matériau est : {id_material}")
        return (id_material, self.is_recyclable(id_material))

    def is_recyclable(self, mat) : 
        """"
        returns if a material is recyclable or not
        """
        if mat.material != "":
            return mat.material.recyclabilite
        else : 
            return "Erreur : matériau non présent dans la base de donnée"
        
obj = TTNDataHandler()
obj._spark_knn({'A' : 0, 'B' : 0, 'C' : 0, 'D' : 0, 'E' : 0, 'F' : 0, 'G' : 0, 'H' : 0, 'I' : 0, 'J' : 0, 'K' : 0, 'L' : 0, 'R' : 0, 'S' : 0, 'T' : 0, 'U' : 0, 'V' : 0, 'W ': 0})  
#obj._add_sparkfun_data_s1( ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'R', 'S', 'T','U', 'V', 'W'], [0 for i in range (18)])  
    


