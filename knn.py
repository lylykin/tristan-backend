from math import sqrt

#what my knn class needs : 
#in the 1st phatse, i'll need a KNN builder, and the the KNN indentification, based on Deborah's code
# phase de test
class KNN() : 
    data_test : list

    def __init__(self, data_test) : 
        self.knnData  = {}
        self.value = data_test

    def knn(self, k = 7) :        
        self.liste_vois  = self.plus_proche_voisins()
        return self.identification()
         

    def addKnnData(self, elt_list : list, name_list : str):
        """
        adds a list of points into the KNN test data.
        elt : array of the data we want to add
        """ 
        for elt, name in elt_list, name_list : 
            self.knnData[elt] = name 


    def plus_proche_voisins(self, k : int = 7):
        """
        returns the k-nearest neighbours of the data we want to identify
        k (int) : number of neighbours we want
        """ 
        
        dist = []
        data_dict = self.knnData
                       
        for data in data_dict.keys():
            dist.append((euclidienne(self.value, data),data))
            
        dist.sort() 
        return [data_dict[dist[j][1]] for j in range (k)]

    def identification(self):
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

#A = KNN((1,3))
#for val in fruits.items():
#    A.addKnnData(val[0], val[1])
#
#print(A.knn(k=2))
#

