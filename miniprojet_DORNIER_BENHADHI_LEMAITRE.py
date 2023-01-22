# DORNIER - LEMAITRE - BEN KADHI
########## Importation des modules ##########

import time
from algo_stat import *
from lxml import etree
import requests

##### Définition des variables globales #####

parkings=['FR_MTP_ANTI','FR_MTP_COME','FR_MTP_CORU','FR_MTP_EURO','FR_MTP_SABL','FR_MTP_FOCH','FR_MTP_GARE','FR_MTP_TRIA','FR_MTP_ARCT','FR_MTP_PITO','FR_MTP_CIRC','FR_MTP_SABI','FR_MTP_GARC','FR_MTP_MOSS','FR_STJ_SJLC','FR_MTP_MEDC','FR_MTP_OCCI','FR_MTP_GA109','FR_MTP_GA250','FR_CAS_CDGA','FR_MTP_POLY']

################# Fonctions #################

### Collecte des données : 

def collecte_de_donnees():
    """collecte les données des parkings et les enregistre dans le fichier nb_placesNOM_PARKING.txt"""
    temps = time.time()
    base = "https://data.montpellier3m.fr/sites/default/files/ressources/"
    while 3600 > time.time()-temps:  #boucle while qui tourne pendant le temps indiqué en secondes  
        for i in range(len(parkings)):
            print(i)
            lien = base + parkings[i] + ".xml"
            response = requests.get(lien)
            if response.text != "":
                f1 = open("data_"+parkings[i]+".txt", "w", encoding="utf8") 
                f1.write(response.text) #écrit le contenu du fichier xml d'un parking dans un fichier texte pour chaque parkings
                f1.close()
                tree = etree.parse("data_"+parkings[i]+".txt")  #parse le fichier texte du parking
                f2 = open("nb_places"+parkings[i]+".txt", "a", encoding="utf8") #ajoute chaque éléments de la liste dans un fichier texte
                for libre in tree.xpath("Free"):
                    f2.writelines(libre.text+"\n")
                f2.close() 
        time.sleep(600) #arrête le programme pendant un temps donné en secondes 
        print(time.time()-temps)
print(collecte_de_donnees())

### Transformation des données pour pouvoir mieux les exploiter :

def transforme_liste():
    """met dans une liste des listes contenant le nombre de places libres de chaque parking à chaque nouvel échantillonage"""
    occupation = []
    for i in range(len(parkings)):
        f1 = open("nb_places"+parkings[i]+".txt", "r", encoding="utf8") #parcours les lignes des fichiers de chaque parkings
        liste = f1.readlines() #ajoute chaque éléments du fichier texte dans une liste
        f1.close()
        occupation.append(liste) #ajoute la liste dans la liste "occupation"
    return occupation

### Moyenne de places libres pour chaque parkings

def moyenne_parkings():
    """calcule la moyenne de chaque liste contenu dans la liste occupation"""
    moy_park = [] #liste contenant la moyenne de place libres pour chaque parkings
    l = transforme_liste() #variable contenant le résultat de la fonction transforme_liste
    for i in range(len(l)):
        somme = 0
        for j in range(len(l[i])):
            terme = l[i][j]
            nombre = terme[:-1] #enlève le "\n" à la fin de chaque caractère et le convertit en integer
            somme += int(nombre)
            moy = round(somme/len(l[i]),2) #calcule la moyenne de chaque listes contenu dans moy_park
        moy_park.append(moy)
    f1 = open("moyenne_places.txt", "a", encoding="utf8")
    f1.write(str(moy_park))
    f1.close()

print(moyenne_parkings())

### Ecart-type du nombre de places libres pour chaque parking

def ecartType_parkings():
    """calcule l'écart-type du nombre de places libres de chaque parking"""
    l = transforme_liste()
    l_e_t = [] 
    for i in range(len(l)):
        liste_tempo = [] #liste contenant le nombre de places libres pour un seul parking
        for j in range(len(l[i])):
            terme = l[i][j]
            nombre = int(terme[:-1]) #enlève le "\n" à la fin de chaque termes et le convertit en integer
            liste_tempo.append(nombre)
        e_t = round(ecart_type(liste_tempo),1)
        l_e_t.append(e_t)
    f1 = open("ecartType.txt", "a", encoding="utf8")
    f1.write(str(l_e_t))
    f1.close()

print(ecartType_parkings())

    