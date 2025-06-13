from math import sqrt

#what my knn class needs : 
#in the 1st phatse, i'll need a KNN builder, and the the KNN indentification, based on Deborah's code
# phase de test
class KNN() : 
    data_test : list
    dico_ref : dict

    def __init__(self, data_test : list, dico_ref : dict) : 
        self.knnData, self.value = normalize(dico_ref, data_test)
        #print(self.knnData)
        #print(self.value)

    def knn(self) :        
        self.liste_vois = self.plus_proche_voisins()
        return self.identification()

    def plus_proche_voisins(self, k : int = 7):
        """
        returns the k-nearest neighbours of the data we want to identify
        k (int) : number of neighbours we want
        """ 
        print("recherche des plus proches voisisns")
        dist = []
        self.knnData
        #print(f'les data sont :{self.knnData} ')
        
        #calcul de la distance 
        for data in self.knnData.keys():
            dist.append((euclidienne(self.value, data),data))
            
        dist.sort() 
        #print (dist)
        return [self.knnData[dist[j][1]] for j in range (k)]

    def identification(self):
        print("identification du matériau")
        nbr = {}
        for elt in self.liste_vois:
            if elt in nbr:
                nbr[elt] += 1
            else:
                nbr[elt] = 1
        max = 0
        type = ""
        for valeur in nbr.items():
            if max < valeur[1]: 
                max = valeur[1]
                type = valeur[0]
        return type
    

def euclidienne(list_a : list, list_b : list):
    "returns the euclidian distance of 2 series of the same lenght"
    
    sum_dist = (list_a[0]-list_b[0])**2
    
    for i in range (1, len(list_a)) : 
        sum_dist += (list_a[i]- list_b[i])**2
    
    return sqrt(sum_dist)


def normalize(data_dico : dict, data_list : list) :
    
    "normalise les data passées en paramètre, pour que toutes les dimensions soient entre 0 et 1"
    
    norma_dict = {}
    norma_list = []
    max_vals=[0 for _ in range (len(list(data_dico.keys())[0]))]
    
    #on parcoure les lettres une à une, pour rechercher le plus grand.
    for i in range(len(list(data_dico.keys())[0])) : 
                
        for spark_data in data_dico.keys():
             #recherche de la plus grande valeur pour la lettre correspondante
            if spark_data[i] >max_vals[i] :
                max_vals[i] = spark_data[i]
        
        if data_list[i]>max_vals[i]: 
            max_vals[i] = data_list[i]
            
    #normalisation des datas dans la db
    for spark_data in data_dico.keys():
        
        vals = []
        
        #les deux ont forcément la même taille et les données dans le même sens.
        for val in range(len(spark_data)) : 
            vals.append(spark_data[val]/max_vals[val])
            
        vals = tuple(vals)
        norma_dict[vals] = data_dico[spark_data]
            
    for i in range(len(max_vals)) : 
        norma_list.append(data_list[i]/max_vals[i])
            
        #dico avec les valeurs normalisées.

        
    return (norma_dict, norma_list)


    
    
  
fruits = {
    (1, 3): 'poire',
    (3, 5): 'poire',
    (6, 2): 'pomme',
    (1, 7): 'poire',
    (3, 2): 'poire',
    (4, 5): 'pomme',
    (5, 6): 'poire',
    (6, 5): 'pomme',
    (7, 6): 'pomme',
    (8, 4): 'pomme'}

#A = KNN((1,3), fruits)
#for val in fruits.items():
#    A.addKnnData(val[0], val[1])
#
#print(A.knn())


