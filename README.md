# tristan-backend
Backend for the tristan app

## How does it work?
Pour nos requêtes, nous avons utilisé la librairie de Vaphes : pyhon Pocketbase


Le client est hébergé localement, et est lancé par le fichier main.go. La base de donnée est lancée **localement** par la commande go run main.go serve.
Ce projet est toujours en constructions, donc des améliorations seront prévues à l'avenir, comme faire en sorte que la db soit accessible par une tierce machine.

Une fois le serveur lancé, faire tourner sur la machine serveur le fichier 'datamanager.py'

- Lignes 11 à 13 : affectations des clés et mots de passe associcés à l'aplication TTN
- lignes 21 à 23 : choix du certificat. En fonction de celui-ci, le port sera à adapter pour le broker
- la fonction on_connect ( ligne 76) permet de suscribe au client
- En ligne 86, on définit le stage du projet. Si on est en phase 1 (stage == 1) : connexion au client puis appel de la méthode on_ttn_message_s1 quand un message est reçu. Si on est en phase 2 : connexion au client puis appel de la méthode on_ttn_message_s2 quand un message est reçu.

Les mesures se font en deux phases : 

## Phase 1 : Ajout des données dans la base de donnée
Dans cette phase, nous contruisons la base de donnée. Donc lors de la réception de messages, il faut ajouter les données reçues dans la base de données. La gestion des messages est faite ar une instance de la classe TTnDataHandler, définie dans le module ttnLink dont voici l'explication : 

L'instance est définie avec ses attributs clients, qui est notre base de données locale ici, et le super_user, qui pemet la connexion en admin.
$python
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
$  
A l'appel de la fonction callback on_ttn_message_s1, le payload reçu est décodé. Ensuite, on identifie le type de données et la méthode correspondante est ensuite appelée : _add_sparkfun_data_s1 si c'est une donnée du sparkfun, _add_gps_data si c'est une donnée du gps. S'il s'agit d'un autre type de données, on pass pour ne rien faire car ce n'est pas une information qui nous intéresse. 

$python
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
$
Cette méthode permet d'ajouter les données du sparkfun dans la database. On entre à la main le nom du matériau, puis la méthode collection.create() de PocketBase nous permet d'ajouter une entrée dans la collection sparkfun, avec les données. 
_add_gps_data() fonctionne sous le même principe.
$
python
    def _add_gps_data(self, data_keys : list, data_values : list):
        self.client.collection("gps").create(
            {data_keys[0] : data_values[0],
             data_keys[1] : data_values[1],
             data_keys[2] : data_values[2],
                }
            )

$



### Phase 2 : Evaluation du matériau

Dans la deuxième phase, la base de donnée est créée et nous allons traiter les données de deux manières : 
- si c'est une donnée GPS, son utilisation reste la même que dans la phase 1
- si c'est une donnée sparkfun, il s'agit d'un matériau à identifier. On va donc réaliser une analyse knn.

La méthode _on_ttn_message_s2 est quasiment identique à son homologue de la partie 1, mais lorsqu'une donnée Sparkfun est reçue, la méthode _spark_knn ets appelée : 
$ python
    def _spark_knn(self, dico_data : dict) : 
        """
        doit retourner le matériau identifié par le knn
        """
        data_list = list(dico_data.values())
        #récupération des records en brut
        materials = self.client.collection("sparkfun").get_full_list(100,
            {"expand": 'material'})
        
        pb_data = []
        for mat in materials: 
            pb_data.append(self.decode(mat).l)
      
        print(materials)
        #identification
        print("Identification du matériau en cours")
        ident = KNN(data_list)
        ident.addKnnData(pb_data,)
        id_material = ident.knn()
        #for now it is a print. plus tard, l'ajouter dans l'historique de l'user, et le récupérer comme ca pour le frontend
        print(f"ifentificaation terminée. le matériau est : {id_material}")
        return (id_material, self.is_recyclable(id_material))

$
Note : cette méthode est toujours en amélioration et en debug. 
On récupère dans data_list la liste des valeurs de la mesure (flottants). 
La méthode collections.get_full_list() retourne l'ensemble des entrées de la collection Sparkfun. le paramètre {expland : 'material'} fait la jointure avec la collection materiau, par la valeur material.
L'appel de la méthode decude permet simplement de retourner le matériau en str. 
Enfin, le KNN est réalisé pour identifier le matériau, puis la méthode is_recyclable est appelée pour retourner la recyclabilité du matériau.
$ python
    def is_recyclable(self, mat) : 
        """"
        returns if a material is recyclable or not
        """
        if mat.material != "":
            return mat.material.recyclabilite
        else : 
            return "Erreur : matériau non présent dans la base de donnée"

$
Elle retourne directement la valeur de la colonne 'recyclablilite'.