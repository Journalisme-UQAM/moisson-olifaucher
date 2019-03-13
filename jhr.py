# coding: utf-8

### Bon script! Bien démarré. 

import csv
import requests
from bs4 import BeautifulSoup

fichier = "prof_udem2_JHR.csv" ### Nouveau nom de fichier pour faire mes tests

### Tu indiques ne recueillir que la première page. Il y en a 23. Alors fais-toi une boucle allant de 1 à 23:
for pg in range(1,24):
	url = "https://recherche.umontreal.ca/nos-chercheurs/repertoire-des-professeurs/sm/l/pg/{}/".format(pg)

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
			faculte_departement = coordonnees.find("p").text ### Parfois, ça ne fonctionne pas pcq le prof ne semble affilié à aucun département (Olivier Bauer par exemple)... J'escamoterais ces profs aux fiches incomplètes par un try en début de boucle.
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
			
			### «find_all("a")» fait une liste avec tous les «a» contenus dans «coordonnees»
			### Il y en a généralement deux.
			### Il te suffit donc de dire que le premier élément est le numéro de téléphone
			### Et que le 2e est le courriel
			### Mais il faut encapsuler chacun dans un «try», car les pages de certains profs ne contiennent pas ces informations

			try:
				tel = tel_courriel1[0].text.strip()
			except:
				tel = ""
			infos.append(tel)

			try:
				courriel = tel_courriel1[1].text.strip()
			except:
				courriel = ""
			infos.append(courriel)

			#Lien menant au profil du prof
			infos.append(enseignants)

			### Il est toujours bon d'afficher dans le terminal les infos qu'on a recueillies jusqu'à maintenant, histoire de voir ce qui se passe et de détecter d'éventuelles erreurs en cours de route
			print(infos)

			creation_fichier.writerow(infos)

# Rebonjour JH, mon script fonctionne pour la première des 23 pages du répertoire des professeurs
# de l'UdeM. Je compte faire une boucle que j'ai eu un peu de misère à faire pour que mon script
# rammasse tous les profs de l'UdeM. Je compte aussi exclure les non-professeurs.
