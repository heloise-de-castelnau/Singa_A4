import streamlit as st
from PIL import Image
#Importer les datasets
import pandas as pd
import requests as rq
from io import BytesIO

import pandas as pd
import numpy as np
# test symptome maladie pour le soigné
path = 'https://raw.githubusercontent.com/heloise-de-castelnau/Singa_A4/main/'
url=path+ 'symptomes_maladies.xlsx'
data = rq.get(url).content
data_user= pd.read_excel(BytesIO(data))
data_user=data_user.iloc[:,:99]

#test risque maladie pour le soigné
url=path+ 'risques_maladies.xlsx'
data = rq.get(url).content
data_risques= pd.read_excel(BytesIO(data))
list_symptoms =data_risques.columns.values.tolist()
list_symptoms.remove(list_symptoms[0])

#affichage des préventions selon maladie

url=path+ 'prévention.xlsx'
data = rq.get(url).content
prevention= pd.read_excel(BytesIO(data))
#probabilité de maladie selon symptomes pour le médecin
url=path+ 'singa_xl.xlsx'
data = rq.get(url).content
data_medecin= pd.read_excel(BytesIO(data))
list_symptoms_maladie =data_medecin.columns.values.tolist()
list_symptoms_maladie.remove(list_symptoms_maladie[0])



### Liste des elements obtenues du Excel
def page_acceuil():
  st.header("Bienvenue sur la page d'acceuil de l'API de SINGA")
  st.markdown("Cette interface a pour objectif de vous aider à comprendre les risques qui vous entourent et peuvent impacter votre santé. Attention cependant, ces conseils ne remplacent pas une visite médicale chez le médecin")
  url=path+ 'singa_project_img0.jpg'
  res = rq.get(url)
  image = Image.open(BytesIO(res.content))
  st.image(image, caption='SINGA')

#Pour le médecin
def create_vector_medecin(options):
  vector=[]
  for i in range(len(options)):
    for j in range(len(list_symptoms_maladie)):
      if str(options[i])==str(list_symptoms_maladie[j]):
        vector.insert(j,1.0)
      else:
        vector.insert(j,0.0)
  return vector

def what_disease(array,percentage):
  list_sickness={}
  for i in range(30):
    count_up =0
    count_down=0
    count =0
    for j in range(len(data_medecin.iloc[i])-2):
     if array[j]==data_medecin.iloc[i][j+1]:
       count_up+=1
     else :
       count_down+=1  
    count=count_up-count_down
    if ((count/122)*100)>=percentage:
      list_sickness[data_medecin.iloc[i][0]]=((count/122)*100)
  list_sickness= sorted(list_sickness.items(), key=lambda x: x[1], reverse=True)
  return list_sickness

#Pour le soigné
def create_vector_soin(options):
  vector=[]
  for i in range(len(options)):
    for j in range(len(list_symptoms)):
      if str(options[i])==str(list_symptoms[j]):
        vector.insert(j,1.0)
      else:
        vector.insert(j,0.0)
  return vector


def risk_disease(array,percentage):
  list_sickness={}
  for i in range(30):
    count_up =0
    count_down=0
    count =0
    for j in range(23):
     if array[j]==data_risques.iloc[i][1:25][j]:
       count_up+=1
     else :
       count_down+=1  
    count=count_up-count_down
    if ((count/23)*100)>=percentage:
      list_sickness[data_risques.iloc[i][0]]=((count/23)*100)
  list_sickness= sorted(list_sickness.items(), key=lambda x: x[1], reverse=True)
  return list_sickness



#Test symptome maladie pour le soigné
def symptomes_maladies():
  st.header("Quelle maladie devez-vous prévenir ?")
  options = st.multiselect(
     'Quels sont vos risque?',
     list_symptoms)
  if st.button('Rechercher'):
     vect =create_vector_soin(options)
     liste_resultats=risk_disease(vect,80)
     for i in range(3):
       st.markdown(liste_resultats[i][0])
  if st.button('Nettoyer Resultats'):
    st.write('Nettoyé !')
  else:
     st.write('Remplir infos')
  


# Test symptomes maladie pour le médecin
def symptomes_maladies_medecin():
  st.header("Aide à la detection de maladies")
  options = st.multiselect(
     'Quels sont les symptomes ?',
     list_symptoms_maladie)
  
  if st.button('Rechercher'):
     vect=create_vector_medecin(options)
     liste_resultats=what_disease(vect,85)
     for i in range(5):
       st.markdown(liste_resultats[i][0])
      
  if st.button('Tout afficher'):
    vect=create_vector_medecin(options)
    liste_resultats=what_disease(vect,85)
    for i in range(len(liste_resultats)):
      st.markdown(liste_resultats[i][0])

  if st.button('Nettoyer Resultats'):
    vect=[0.0]*128
    options=[]
    st.write('Nettoyé !')
  else:
     st.write('Remplir infos')
  

def projet_singa():
   st.title("Presentation du projet Singa")
   st.header("Le problème ")
   st.markdown("- 41% de la population du continent vit actuellement au-dessus du seuil de la pauvreté")
   st.markdown("- En 2020, 53 % des Africains déclaraient avoir manqué de soins nécessaires au moins une fois au cours de l’année passée")
   st.header("La RDC ")
   st.markdown("- environ 84 millions d’habitants en RDC ")
   st.markdown("- marché estimé à 800 millions de dollars américains ")
   st.markdown("- le système de santé Congolais est fracturé ")
   st.markdown("- 74% de la population vit sous le seuil de pauvreté ")
   st.markdown("- moins d’1% de la population a une assurance santé ")
   st.markdown("- le budget pour la santé est à peine de 7% ")
   st.header("Le marché ")
   st.markdown("- depuis 2015: libéralisation du marché opérée par le gouvernement")
   st.markdown("- 400k membres de la diaspora en Europe : une participation active dans l’économie du pays")
   st.markdown("- un marché de l’assurance estimé à 800 millions de dollars")
   st.markdown("- 3 millions d’assurés, soit moins d’1% de la population")
   st.header("La solution")
   url=path+ 'singa_project_img1.jpg'
   res = rq.get(url)
   image = Image.open(BytesIO(res.content))
   st.image(image, caption='Solution singa')
   st.markdown("- Un site en ligne pour enregistrer ses bénéficiaires et assurer la santé de sa famille")
   st.markdown("- Une application pour accéder à l'abonnement en tant que bénéficiaire et enregistrer ses consultations")
   st.header("Une protection adaptée")
   st.markdown("couvrir 100% des dépenses de santé, dans la limite de plafonds étudiés et adaptés aux besoins de la population ")
   url=path+ 'singa_project_img3.jpg'
   res = rq.get(url)
   image = Image.open(BytesIO(res.content))
   st.image(image, caption='Solution singa')

   st.header("Valeurs")
   st.header("Partage, sincérité & utilité")
   st.markdown("« nous croyons que la l’Afrique mérite d’avoir accès à des soins de qualité")
   st.markdown("nous rendons cela possible en renforçant le lien entre les membres de la diaspora et leurs familles, en commençant par le Congo")
   st.markdown("singa permet à la diaspora d’offrir à leurs proches une mutuelle santé simple, solidaire et utile »")

def projet_singa_esilv():
  st.title("Presentation du projet Singa - ESILV")
  st.header("Missions")
  st.markdown("Au cours de ce projet d'année nous avons réalisés plusieurs missions techniques : de gestion back-end en premier lieu, de recherches et traitement d'informations médicales et enfin de gestion front-end avec une API user-friendly")
  
  st.header("Gestion des données en back-end")
  st.markdown("Notre objectif premier fut de développer pour Singa une organisation de leurs différents partenaires, des échanges et des responsabilités/options de chacun et ce afin de faciliter la gestion de leurs données après création du site web")
  st.markdown("Nous avons alors dévellopé un schéma E/A de ces différents acteurs et des relations qui les lient")
  url=path+ 'image.png'
  res = rq.get(url)
  image = Image.open(BytesIO(res.content))
  st.image(image, caption='Schema E/A')
  st.markdown("Nous avons ensuite travaillé sur le développement de ce schéma en creant une base de donnée via JavaScript et pouvant ainsi être importé sur Docker")
  url=path+ 'singa_dev.jpg'
  res = rq.get(url)
  image = Image.open(BytesIO(res.content))
  st.image(image, caption='Dévellopement de la base de données en JavaScript')
  url=path+ 'horizontal-logo-monochromatic-white.png'
  res = rq.get(url)
  image = Image.open(BytesIO(res.content))
  st.image(image, caption='Exportation et gestion de la BDD sur Docker')
  
  st.header("Gestion de données de santé")
  st.markdown("Les données de santé etant très reglementés, nous avons effectués un travail de recherces médicales en créant un excel de pres de 1300 points d'informations reliés ( dizaine de maladies pour 126 critères d'indentifications)")
  st.markdown("Nous avions pour objectif de dévelloper une API d'aide à l'identification de maladies pour le médecin mais de pré-diagnostic pour le bénéficiaire aussi et nous avons alors travaillé sur les datasets suivants nous permettant de prévenir les maladies étudiés :")
  url=path+ 'prévention.xlsx'
  data = rq.get(url).content
  prevention= pd.read_excel(BytesIO(data))
  st.dataframe(prevention)
  url=path+ 'risques_maladies.xlsx'
  data = rq.get(url).content
  data_risques= pd.read_excel(BytesIO(data))
  st.dataframe(data_risques)
  url=path+ 'singa_xl.xlsx'
  data = rq.get(url).content
  data_medecin= pd.read_excel(BytesIO(data))  
  st.dataframe(data_medecin)
  st.markdown("")
  
  st.header("Développement d'une API d'aide à la prévention")
  st.markdown("Notre objectif final avec l'étude des données de santé décrite au dessus, était de dévelloper une API d'aide à l'identification de maladies pour le médecin mais de pré-diagnostic pour le bénéficiaire")
  st.markdown("Nous avons alors dévellopé un algorithmes qui ressort selon les critères rentrés par le sujet, les maladies les plus à risques :")
  st.markdown("Ici un appercu du code :")
  code='''
  #Pour le médecin
  #Transformation de l'information en vecteur 
  def create_vector_medecin(options):
    vector=[]
    for i in range(len(options)):
      for j in range(len(list_symptoms_maladie)):
        if str(options[i])==str(list_symptoms_maladie[j]):
          vector.insert(j,1.0)
        else:
          vector.insert(j,0.0)
    return vector
  #Algotihme de ressemblance du vecteur rentré par rapport au dataset 
  def what_disease(array,percentage):
    list_sickness={}
    for i in range(30):
      count_up =0
      count_down=0
      count =0
      for j in range(len(data_medecin.iloc[i])-2):
      if array[j]==data_medecin.iloc[i][j+1]:
        count_up+=1
      else :
        count_down+=1  
      count=count_up-count_down
      if ((count/122)*100)>=percentage:
        list_sickness[data_medecin.iloc[i][0]]=((count/122)*100)
    list_sickness= sorted(list_sickness.items(), key=lambda x: x[1], reverse=True)
    return list_sickness'''
  st.code(code)

#### MAIN
def main():
  page_projet=st.sidebar.selectbox(
            "A propos de singa",
            ["Selection","Presentation du projet Singa","Projet ESILV-SINGA"],)
  if page_projet=="Presentation du projet Singa":
    projet_singa()
  if page_projet=="Projet ESILV-SINGA":
    projet_singa_esilv()
  page = st.sidebar.selectbox(
              "Prévenir les maladies",
              ["Selection"]+prevention.iloc[:,0].to_list())
  for i in range(len(prevention.iloc[:,0].to_list())):
    if page ==prevention.iloc[:,0].to_list()[i]:
      st.header(prevention.iloc[:,0].to_list()[i])
      # Tuberculose, ebola
      #Tuberculose,Ebola (FHV) 
      if(prevention.iloc[:,0].to_list()[0]==page):
           url=path+ 'tuberculose.jpg'
           res = rq.get(url)
           image = Image.open(BytesIO(res.content))
           st.image(image, caption='Solution singa')
        
      if(prevention.iloc[:,0].to_list()[1]==page):
           url=path+ 'ebola.jpg'
           res = rq.get(url)
           image = Image.open(BytesIO(res.content))
           st.image(image, caption='Solution singa')
      if(prevention.iloc[:,0].to_list()[3]==page):
          url=path+ 'oncho.jpg'
          res = rq.get(url)
          image = Image.open(BytesIO(res.content))
          st.image(image, caption='Solution singa')

      else :
        st.markdown(prevention.iloc[:,1].to_list()[i])

  test_api= st.sidebar.selectbox(
              "De quelle maladie suis-je sujet à risque ?",
              ["Selection","Testez-vous ici","Test médecin"],)
  if test_api=="Testez-vous ici":
    symptomes_maladies()
  if page=="Selection" and test_api=="Selection" and page_projet=="Selection":
    page_acceuil()
  if test_api=="Test médecin":
    symptomes_maladies_medecin()




main()
