import requests
import json
import time
from datetime import datetime
import pandas as pd
import csv

while True:             #Permet de faire une boucle qui ne s'arrête pas tant que le programme sera bon.

    # Récupération des données JSON à partir de l'URL indiqué
    response = requests.get("https://montpellier-fr-smoove.klervi.net/gbfs/en/station_information.json")
    data = response.json()

    # Chaque donnée de l'URL est enregistré dans des variables.
    for station in data["data"]["stations"]:
        nom = station["name"]
        num_station = station["station_id"]
        capacité = station["capacity"]
        longitude = station["lon"]
        latitude = station ["lat"]

        # Affichage des informations récupérés de chaque station
        print(f"Nom: {nom}")
        print(f"Numéro de station: {num_station}")
        print(f"Capacité: {capacité}")
        print(f"Latitude: {latitude}")
        print(f"Longitude : {longitude}")
        print()
        

	#Récupération des informations à partir des 2 URL donnés

    def velo():
        requete_site1 = requests.get("https://montpellier-fr-smoove.klervi.net/gbfs/en/station_information.json")
        data_site1 = requete_site1.json()
        requete_site2 = requests.get("https://montpellier-fr-smoove.klervi.net/gbfs/en/station_status.json")
        data_site2 = requete_site2.json()
        
        #Création de plusieurs liste qui contiendront les informations récupérés.
        
        temp=0
        nom = []
        num_station = []
        capacité = []
        longitude = []
        latitude = []
        num_velo_dispo = []
        num_borne_dispo = []
        derniere_update  = []
        
        temps = datetime.now()


	#Stockage des données dans les listes.

        for i in data_site1["data"]["stations"]:
            num_station.append (i["station_id"])
            nom.append (i["name"])
            capacité.append (i["capacity"])
            longitude.append (i["lon"])
            latitude.append (i["lat"])

        for x in data_site2["data"]["stations"]:
            temp+=1
            num_velo_dispo.append (x["num_bikes_available"])
            num_borne_dispo.append (x["num_docks_available"])
            derniere_update.append (x["last_reported"])
            
           #Création d'un fichier.csv et .txt a partir des données stockées

        file_path = temps.strftime("Bureau/sae15/csv/%Y-%m-%d_%H-%M-%S.csv")
        tableau = {'Numero de station': num_station, 'Nom': nom, 'Heure': derniere_update, 'Bornes disponibles': num_borne_dispo, 'Places Total' : capacité,  'Longitude': longitude, 'latitude': latitude}
        data = pd.DataFrame(tableau)
        data.to_csv(file_path, mode='a', index=False)

        file_path = temps.strftime("Bureau/sae15/txt/%Y-%m-%d_%H-%M-%S.txt")
        f = open(file_path, "w")
        data.to_csv(file_path, mode='a', index=False)
        f.close()           
    velo()

#Récupération d'une donnée particluière dans les fichiers enregistrés.


    open('2023-01-22_21-34-11.csv', 'r') as f:
    reader = csv.reader(f)
    for j in reader:
        print(j[4])



time.sleep(180)                 #Mets une pause de 180 secondes avant de relancer la boucle while

