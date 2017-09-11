
''' Importer le nécessaire pour le webscrapping'''
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
"""Importer le nécesaire pour l'enregistrement des données"""
import pymongo
from pymongo import MongoClient
""" Text-to-Speech """
from gtts import gTTS
from playsound import playsound
import os

''' Requête vers la page d'acceuil pour aller chercher l'article le plus récent. '''
site="http://ici.radio-canada.ca/economie/gerald-fillion"
uClient = uReq(site)
code = uClient.read()
uClient.close()
page_soup = soup(code, "html.parser")
site = page_soup.h3.find('a').get('href')

''' Récuppérer les information de l'article le plus récent. '''
uClient = uReq(site)
code = uClient.read()
uClient.close()
''' Variable code qui resort. '''

''' Enregistre le code de la page dans la variable page_soup '''
page_soup = soup(code, "html.parser", from_encoding="utf-8")
'''  Enregistre le titre dans la variable titre '''
titre = page_soup.h1
''' Prend le texte de l'article et nettoye le. '''
code_texte = page_soup.find("div", { "data-component-name" : "DocumentNewsStoryBody" })
texte_non_clean = code_texte.get_text()
presque = texte_non_clean.strip()
mieux = presque.replace("\xa0", "")
encore_mieux = mieux.replace("\n", " ")
on_y_est = encore_mieux
''' Le texte est maintenant propre '''
''' Il en resort la variable on_y_est '''

''' Aller chercher la date dans le code de la page '''
date = page_soup.find("time")

""" Section MongoDB """
client = MongoClient()
db = client.Nouvelle_Economique
Nouvelles = db.Nouvelles
nouvelle = {"Date": str(date), "Titre": str(titre), "Contenue": str(on_y_est)}
nouvelle_id = Nouvelles.insert_one(nouvelle).inserted_id
""" Ok alors l'information est bien enregistrer dans la base de donnée """

""" Section Text-to-Speech """
tts = gTTS(text=on_y_est, lang="fr")
tts.save("news.mp3")
playsound("news.mp3")
os.remove("news.mp3")
""" Fin de la section Text-to-Speech """
