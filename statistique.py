from random import randint
from sklearn.model_selection import train_test_split
import math
from knn import KNN

# Données (18 valeurs) et materiau
liste_donnees = []
tour = 0
while tour < 3 :
    l= []
    for i in range (18):
        l.append(randint(0,100))
    liste_donnees.append(l)
    tour += 1
materiau = ['A', 'B', 'A']  

dic = {}
for i in range (3):
    dic[tuple(liste_donnees[i])] = materiau[i]

# === Split 80/20 ===
X_train, X_test, y_train, y_test = train_test_split(liste_donnees, materiau, test_size=0.2, random_state=2)
print(X_test, y_test)
print(X_train, y_train)

dic2 = {}
for i in range(len(X_train)):
    dic2[tuple(X_train[i])] = y_train[i]

y_pred = []
for test_liste in X_test :
    knn = KNN(data_test=test_liste, dico_ref=dic2)
    y_pred.append(knn.knn())

correct = 0
for i in range (len(y_pred)):
    if y_pred[i] == y_test[i]:
        correct +=1

accuracy = correct / len(y_test)

print(f"Précision (80/20) : {accuracy:.2%}")