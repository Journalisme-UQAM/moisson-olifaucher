# coding: utf-8

import csv
import requests
from bs4 import BeautifulSoup

fichier = "prof_udem2.csv"

url = "https://recherche.umontreal.ca/nos-chercheurs/repertoire-des-professeurs/sm/l/"

entete = {
	"User-Agent": "Olivier Faucher - requête acheminée dans le cadre d'un cours de journalisme de données",
	"From":"faucher.olivier@courrier.uqam.ca"
}

contenu = requests.get(url,headers=entete)

page = BeautifulSoup(contenu.text,"html.parser")

professeurs = page.find_all("div", class_="row udemvitrine-search-result")


with open(fichier,"w") as f2:
	creation_fichier = csv.writer(f2,)
	for professeur in professeurs:
		href = professeur.find("a")["href"] #Trouver le lien de la page d'un prof
		enseignants = "https://recherche.umontreal.ca" + href #Compléter la page
		contenu2 = requests.get(enseignants,headers=entete) #Accéder à la page
		page_prof = BeautifulSoup(contenu2.text, "html.parser") #Lire la page

		coordonnees = page_prof.find("dd", class_="uniteAdministrative") #Ceci est la section des coordonnées du prof

		infos = []

		#La faculté et le département
		faculte_departement = coordonnees.find("p").text
		infos.append(faculte_departement)

		#Nom du prof
		section_nom = page_prof.find("div", class_="carte-visite")
		nom = section_nom.find("h1").text #Trouver le nom dans cette section
		infos.append(nom)


		#Professeur ou professeure
		genre1 = page_prof.find("dt", class_="fonction")
		genre2 = genre1.text
		genre3 = genre2.split()
		genre4 = genre3[0]
		infos.append(genre4)


		#Tel et courriel (Salut JH, j'essaie de supprimer la partie href de ce string
		# afin de ne conserver que le numéro et le courriel sans les liens. Je suis incapable. Help!)
		tel_courriel1 = coordonnees.find_all("a")
		

		#Lien menant au profil du prof
		infos.append(enseignants)

		creation_fichier.writerow(infos)


# Rebonjour JH, mon script fonctionne pour la première des 23 pages du répertoire des professeurs
# de l'UdeM. Je compte faire une boucle que j'ai eu un peu de misère à faire pour que mon script
# rammasse tous les profs de l'UdeM. Je compte aussi exclure les non-professeurs.
		



		




		



		



