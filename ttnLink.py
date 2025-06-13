from pocketbase import PocketBase  # Client also works the same
from dotenv import load_dotenv 
import os
from knn import KNN
import json 
import pca
import statistique as stati



# Classe TTNDataHandler qui doit avoir une méthode on_ttn_message
class TTNDataHandler:
    client : PocketBase
    
    def __init__(self, client = PocketBase('https://vps-2244fb93.vps.ovh.net')):
        load_dotenv(dotenv_path="secret_dont_look_at_me.env")
        
        self.client = client
        self.super_user = self.client.admins.auth_with_password(os.getenv('SUPER_ID'), os.getenv('SUPER_PASS'))

    # Méthode appelée lorsque le client TTN reçoit un message
    def on_ttn_message_s1(self, client, userdata, msg):
        
        #converts the recieved data as a    
        
        message = json.loads(msg.payload.decode())
        print(message)
        
        try : 
            dico_payload = message['uplink_message']['decoded_payload']           
            if list(dico_payload.keys())[0] == 'A' : 
                self._add_sparkfun_data_s1(list(dico_payload.keys()), list(dico_payload.values()))
            else :
                self._add_gps_data(list(dico_payload.keys()), list(dico_payload.values())) 
        except: 
            pass   

    def _add_sparkfun_data_s1(self, data_keys : list, data_values : list,):
        """
        Pour la phase d'insertion (1), appelée à la réception de donnée
        data_keys étant le nom des attributs du payload et data_values les valeurs associées
        On demande le matériau associé à la mesure, traite sa création si besoin et on ajoute les valeurs aux attributs de sparkfun
        """
        # On demande les informations lors du remplissage de la bdd
        material_input = str(input("Donnée Sparkfun reçue\nSaisir le matériau du déchet : "))
        self.add_material_if_needed(material_input)
        
        print("Phase 1 : Insertion en cours...")
        data_dict = { 
                     data_keys[i]: data_values[i] 
                     for i in range(len(data_values))
                    }
        
        data_dict['material'] = material_input
 
        print(data_dict)
        
        #gestion plus facile des trash : on différencie les trash des empty
        if material_input != 'trash' :
            self.client.collection("sparkfun").create(data_dict)
 
 #Dorian, pour moi ta méthode a pas besoin de return car material_input est pas modifié...   
    def add_material_if_needed(self, material_input):
        """
        Récupère les matériaux présents dans la bdd et teste si le nom de matériau en paramètre existe
        Récupère l'identifiant si le matériau existe déjà et sinon crée la ligne en demandant la recyclabilité
        renvoie l'id du matériau inséré/entré
        """
        materials_list = self.client.collection("materiau").get_full_list()
        contained = False # Tiens compte si le matériau est dans la bdd
        for mat in materials_list :
            id = mat.id
            if material_input == id : # On suppose que les id ou nom de materiaux sont uniques pour chaque materiau
                material_id = id
                contained = True
        if not contained : # Si le matériau entré n'existe pas dans la bdd, l'ajouter
            self.client.collection("materiau").create(
                {
                    'id' : material_input,
                    'recyclabilite' : str(input("Nouveau matériau,\nSaisir la recyclabilite du materiau (True/False) : ")),
                }
            )
            
            material_input #self.client.collection("materiau").get_full_list(batch=1)['id'] # Récupère l'id du dernier matériau inséré (voir ci-dessus)

    
    def _add_gps_data(self, data_keys : list, data_values : list):
        self.client.collection("borne").update(
            {
                'lat_actuel'  : data_values[1], # lat
                'long_actuel' : data_values[2], # longitude
            }
        )
        
    def on_ttn_message_s2(self, client, userdata, msg : dict) :
        
        message = json.loads(msg.payload.decode())
        
        #le try except sert à la gestion des erreurs.
        #try : 
        
        dico_payload = message['uplink_message']['decoded_payload']
        print(dico_payload)
        
        if list(dico_payload.keys())[0] == 'A' : 
            print('test bon : le message est correctement formaté')
            mat, recyclable = self._spark_knn(dico_payload)
            self._add_sparkfun_data_s2(list(dico_payload.keys()), list(dico_payload.values()), mat)
            #self.update_knn_found_material(mat)
            return(mat, recyclable)
            
            
        else :
            self._add_gps_data(list(dico_payload.keys()), list(dico_payload.values()))  
        #except :
            print('bouhouhouuu')
            pass 
        
        
    def _add_sparkfun_data_s2(self, data_keys : list, data_values : list, mat : str):
        """
        Pour la phase d'identification (2), appelée à la réception de donnée
        data_keys étant le nom des attributs du payload et data_values les valeurs associées
        Récupère le matériau et le nom de l'objet inséré, le nom de la borne, et le nom de l'user
        Ajoute les informations à la database suivant data_keys et data_values
        """
        # On demande les informations lors du remplissage de la bdd
        self.add_material_if_needed(mat)
        
        #je le passe en attribut pour faciliter l'appel de l'une de tes fonctions
        #au futur : doit être récup de la table objet?? marche pas si reste coté serveur
        self.objet = str(input("saisir l'objet associé au déchet : "))
        borne_input = "tristan1" # On suppose que la borne utilisée sera la seule existante
        #objet_id = self.add_object(objet_input, user_id_input)
        
        print("Phase 2 : Insertion en cours...")
        
        data_dict = {data_keys[i] : data_values[i]
                    for i in range(len(data_values))}
        
        data_dict['borne'] = borne_input
        data_dict['material'] = mat
        
        #récupération de l'id de l'objet
        obj_record = self.client.collection('objet').get_first_list_item(filter = f"nom_objet='{self.objet}'")
        data_dict['objet'] = obj_record.id

        print(data_dict)
        self.client.collection("sparkfun").create(data_dict)
    
    #j'ai supprimé son utilisation car je suis pas sure de ce qu'elle fait + bugguée
    def update_knn_found_material(self, material_id):
        """
        Modifie les collections objet et sparkfun pour leur associer le matériau détecté par le knn
        (à chaque mesure associé à l'objet inséré par l'utilisateur)
        """
        
        #récupération de l'id

        self.client.collection("objet").update(self.objet,
                {
                  'material' : material_id,
                }
            )
        
        mesures_list = self.client.collection("sparkfun").get_full_list(
            {filter: f'objet = {self.objet}'}
        )
        for mesure in mesures_list:
            self.client.collection("sparkfun").update(mesure.id,
                    {
                    'material' : material_id,
                    }
                )

    def _spark_knn(self, dico_data : dict) : 
        """
        doit retourner le matériau identifié par le knn
        """
        data_list = list(dico_data.values())
        #suppression du len qui est resté par je ne sais quelle sorcellerie
        data_list.pop(-1)
        #data_list.pop(11)
    
        print(f'liste des données : {data_list}')
        
        #récupération des records en brut des données de la table sparkfun
        print('récupération des données dans la db\n')
        self.spark_data = self.client.collection("sparkfun").get_full_list(100,
         {'expand': 'material', filter : 'objet=""'})

        #formattage des données materials
        print('formattage des données en cours')
        pb_data = {}
        materials_data = []
        index = 0

        for mat in self.spark_data:
            #récupérer, lettre par lettre, les données des lettres sparkfun
            #bon, est bruteforce mais seul moyen de faire
            materials_data.append((
                mat.a,
                mat.b,
                mat.c,
                mat.d,
                mat.e,
                mat.f,
                mat.g,
                mat.h,
                mat.i,
                mat.j,
                mat.k,
                mat.l,
                mat.r,
                mat.s,
                mat.t,
                mat.u,
                mat.v,
                mat.w
            ))
                
            # asssociation des données sparkfun à son matériau, 
            #formattage pour knn
            pb_data[materials_data[index]] = mat.material
            index += 1
        print(f'pb_data : {pb_data}')
        print('formattage fini')

                
        #identification
        print("Identification du matériau en cours")
        ident = KNN(data_list, pb_data)
        
        id_material = ident.knn()
        #for now it is a print. plus tard, l'ajouter dans l'historique de l'user, et le récupérer comme ca pour le frontend
        print(f"ifentification terminée. le matériau est : {id_material}")
        #print (id_material, self.is_recyclable(id_material))
        return (id_material, self.is_recyclable(id_material))

    def is_recyclable(self, nom_mat : int) : 
        """"
        returns if a material is recyclable or not
        """
        print("vérification de la recyclabilité")
        #récupération des infos sur les matériaux et leur recyclabilité :
        if nom_mat != 'trash' : 
            
            mat = self.client.collection("materiau").get_first_list_item(filter= f"id='{nom_mat}'")
            return mat.recyclabilite
        
        else : 
            return "Erreur : mesure incorrecte, refaites votre donnée"
    
    def pca(self):
        """
        Fonction qui affiche un graphique en 3D en faisant des combinaisaons linéaires des 18D des matériaux

        """
        sparkfun_data = {'data':[],
                         'target_names':[],
                         'target':[]}
        for mat in self.client.collection('sparkfun').get_full_list(100, {filter : f'object=""'}):
            mat_a_mettre = ['verre', 'carton', 'alu', 'pap', 'papth', 'trash']
            if mat.material:# in mat_a_mettre:
                sparkfun_data['data'].append([mat.a,mat.b, mat.c, mat.d, mat.e, mat.f, mat.g, mat.h, mat.i, mat.j, mat.k, mat.r, mat.s, mat.t, mat.u, mat.v, mat.w])
                if mat.material not in sparkfun_data['target_names']:
                    sparkfun_data['target_names'].append(mat.material)
                i = 0
                while i < len(sparkfun_data['target_names']):
                    if sparkfun_data['target_names'][i] == mat.material:
                        sparkfun_data['target'].append(i)
                    i += 1

        pca.pca3D(sparkfun_data)

    def statistique(self):
        liste_donnees = []
        materiau = []

        for mat in self.client.collection('sparkfun').get_full_list(100, {filter : f"objet=''"}):
            if mat.objet != '': #marche pas
                liste_donnees.append([mat.a,mat.b, mat.c, mat.d, mat.e, mat.f, mat.g, mat.h, mat.i, mat.j, mat.k, mat.r, mat.s, mat.t, mat.u, mat.v, mat.w])
                materiau.append(mat.material)

        l = len(liste_donnees)#met l = 6

        #stati.find_best_k(liste_donnees, materiau) # knn meilleur k = 7 avec 48,5 de réussite
        stati.find_best_k(liste_donnees, materiau, True) #knn meilleur k = 3 avec 70,8 de réussite avec le filter direct ds statistique 
                                                         #là ne marche pas



        
#obj = TTNDataHandler()
#print(obj._spark_knn({'A' : 0, 'B' : 0, 'C' : 0, 'D' : 0, 'E' : 0, 'F' : 0, 'G' : 0, 'H' : 0, 'I' : 0, 'J' : 0, 'K' : 0, 'L' : 0, 'R' : 0, 'S' : 0, 'T' : 0, 'U' : 0, 'V' : 0, 'W ': 0})  )
##obj._add_sparkfun_data_s1( ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'R', 'S', 'T','U', 'V', 'W'], [0 for i in range (18)])  
    
