![forthebadge](https://forthebadge.com/images/badges/cc-0.svg)
![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)  



# ocr-p12 Développez une architecture back-end sécurisée en utilisant Django ORM

- Table of Content
  - [Disclaimer](#disclaimer)
  - [Quick Start](#quick-start)
  - [Security and Privacy]
  - [Epic Events API documentation]
  - [Tests passed](#tests-passed)
  - [Crédits and good reads](#credits-and-good-reads)
  - [PEP 8 check](#pep-8-check)


  
## Disclaimer

---

This code is part of the openclassrooms learning adventure split in 13 business alike projects.  
  
  
Some materials or links may have rights to be granted by https://openclassrooms.com. 
The additionnal code follows "CC BY-SA ".
  
** Not to be used for production **  

---

## Epic Events API documentation

### Introduction




## Quick start


Pour démarrer le serveur d'API en local 
sous le prompt bash python (ici cmd Anaconda3 sous Windows 10), vous pouvez:

1.  cloner l'ensemble du répertoire github dans un répertoire local dédié.
    `git clone https://github.com/dev-KC20/ocr-p12.git  
  
2.  se déplacer dans le sous répertoire de travail   
    `cd ocr-p12  
  
3. créer un environnement virtuel python, ENV  
    `python -m venv ENV  
  
4.  activer un environnement virtuel python, ENV  
    `ENV\scripts\activate.bat  

5.  installer les paquets requis,  
    `pip install -r requirements-dev.txt 

6.  se déplacer dans le répertoire de l'application:
    `cd eecrm     
  
7.  créer un fichier .env sous le répertoire courant afin de contenir les "secrets" (cf. plus bas) :  
     ``` 
        # SECURITY WARNING: keep the secret key used in production secret!  
        SECRET_KEY = blabla  
        DEBUG = True  
     ``` 
  
8.  exécuter la migration des modèles  
    `python manage.py migrate  
  
9.  exécuter le script serveur  
    `python manage.py runserver  
  
10. accéder coté client à l'application servie par Django en vous rendant @ :  
    http://127.0.0.1:8000/   
  
   


### Gestion des secrets

Django utilise un "secret" pour générer ses certificats et recommande de garder cette clé secrète. 
Nous utilisons le paquet python-decouple pour remplacer les clés de secret par leur valeur dans le fichier settings.py :
Le fait de stocker les secrets dans un fichier .env évite de le "committer" par accident sur un dépôt centralisé grâce au paramétrage de notre .gitignore.

S'agissant ici d'un exercice pédagogique, nous voulons permettre d'utiliser notre code source et éventuelles données tout en respectant les bonnes pratiques. C'est pourquoi nous autorisons exceptionnellement le commit du fichier .env.

```py
from decouple import config
...
SECRET_KEY = config("SECRET_KEY")

```

## Tests passed


### Django ApiTestCase pass 6/6

![](img/p12-tests-passed-2022-07-16-214829.png)  

![](img/p12-pytest-cov-2022-07-16-213906.png)  


## Credits and good reads.

Openclassrooms and even more the DA Python discord gals & guys!

Offical Flask et pytest documentation!

Nicely written and opiniated post on owasp and Django


## PEP 8 check

`flake8 --format=html --htmldir=flake8_report

![](img/p12-flake8-report-2022-07-16-213208.png)  
