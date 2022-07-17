![forthebadge](https://forthebadge.com/images/badges/cc-0.svg)
![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)  



# ocr-p12 Développez une architecture back-end sécurisée en utilisant Django ORM

- Table of Content
  - [Disclaimer](#disclaimer)
  - [Introduction](#introduction)
  - [Quick Start](#quick-start)
  - [Security and Privacy](#security-and-privacy)
  - [Epic Events API documentation](#Epic-Events-API-documentation)
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

## Introduction

Epic Events does host the funniest and greatest parties in this quarter of the Universe. We manage the full event to ease all the tedious preparation work for our Very Important Clients!

For Managing its Customer Relations, Epic Events uses an internal CRM solution which allows to create & deal with Users, Clients, Contracts and follow Events.


Our I.T department has just improved and secured the internal CRM solution to better support our Customer's and our own business.
For our partners to develop mobile front-end applications as well as for our own staff, we release our API Rest server.

You will find here guidance and a brief introduction on how to install and use our secured API server.

**Have fun, Devs!**



## Quick start


In order to install and use locally the Epic Events CRM back-end API server, assuming you have Python 3 instyalled, open bash prompt: 

1.  clone the ocr-p12 directory into your local copy.  
    `git clone https://github.com/dev-KC20/ocr-p12.git`   
  
2.  move to the working directory   
    `cd ocr-p12`   
  
3. create a python virtual environment named ENV  
    `python -m venv ENV`   
  
4.  do not forget to active the ENV virtual environment  
    `ENV\scripts\activate.bat`   

5.  install all the requirments,  
    `pip install -r requirements-dev.txt`   

6.  move into the source directory,  
    `cd eecrm`       
  
7.  create a .env file in order to keep all secrets local and safe (see hereunder for details),  
     ``` 
        SECRET_KEY = *"yourverystrongandsecurekey"*
        DEBUG = True
        # db postgreSQL
        PG_NAME = eecrm
        PG_USER = admin-oc
        PG_PASSWORD = *"yourverystrongandsecurepassword"*
        PG_HOST = localhost
        ADMIN_ID = admin-oc
        ADMIN_PASSWORD = *"yourverystrongandsecurepassword"*
        #PYTHONPATH = *"yourlocalpathtopython"*
        ALLOWED_HOSTS=localhost, 127.0.0.1 
        #.herokuapp.com
     ``` 
  
8.  download PostgreSQL database from [PostgreSQL: Downloads](https://www.postgresql.org/download/) and follow their instructions.  
   
    You will have to provide an account and password for PostgreSQL root user.  
    Our team uses psql in version 14 and also installed the full SQL admin studio 'pgAdmin 4'  
  
9.  open the psql shell provided with at step 8. and connect to the database  
```  
            psql  
            Server [localhost]:  
            Database [postgres]:  
            Port [5432]:  
            Username [postgres]: PostgreSQL root user  
            Mot de passe pour l'utilisateur PostgreSQL root user :  
```  
11. create a dedicated database for the Epic Events CRM,  
```sql  
            CREATE DATABASE eecrm  
                WITH  
                OWNER = "PostgreSQL root user"  
                ENCODING = 'UTF8'  
                LC_COLLATE = 'French_France.1252'  
                LC_CTYPE = 'French_France.1252'  
                TABLESPACE = pg_default  
                CONNECTION LIMIT = -1;  
  
            ALTER ROLE "PostgreSQL root user" SET default_transaction_isolation TO "read committed";  
            ALTER ROLE "PostgreSQL root user"  SET timezone TO "UTC";  
            GRANT ALL PRIVILEGES ON DATABASE "eecrm" TO "PostgreSQL root user";  
            ALTER USER "PostgreSQL root user" CREATEDB;  
```  
     
      
12. back to the python prompt, build and run Django models migration    
    `python manage.py makemigrations`     
    `python manage.py migrate`    
    
13. create a Django superuser  
    `python manage.py createsuperuser`     
    Username: ADMIN_ID  
    Email address: adminoc@mail.fr  
    Password: ADMIN_PASSWORD  
    Password (again):  

14. Eventually run the server  
    `python manage.py runserver`      
   
  
## Security and privacy  
    
    Epic Events and its co-workers do take your privacy and your data safety very seriously. Out IT team has set several security measures to ensure nothing bad may happen to your data.  
    Epic Events publishes a developper technical guide which requires to protect our solutions against top 10 "owasp" security threats (see also the "credits and good reads" section).  
  
    First of all, we introduced the segregation of duties in how our staff is interacting with your data. Only the manager level has full access whereas salesmen only work on prospection and contract and the support team only care about the events we organize.  
  
  
    ` |dep./object  |	User      |  Customer | Contract |	Event    |`    
    ` |-------------|-------------|-----------|----------|-----------|`    
    ` |anonymous    |	forbidden |	forbidden | forbidden|	forbidden|`    
    ` |sales_team   |		      |  [CR]UDL  |    RL    |  RL       |`    
    ` |sales_contact|		      |   inherit |own [CR]UD|	own [CR] |`    
    ` |support_team |		      |    RL	  |    RL	 |    RL     |`    
    ` |supp_contact |			  |     	  |          |   own UD  |`    
    ` |managmnt_team|	  CRUDL   |	  CRUDL	  |  CRUDL	 |  CRUDL    |`    
  
    For instance, creating user or clients cannot be done thru our exposed back-end API server but need to use a dedicated Admin front-end whose access is strongly restricted.  
      
    On the exposed back-end API server side, we ensure that front-end clients don't temper with the url or the json request body they send to the server.  
  
    All technical operations are logged and help us to prevent and identify any mis-behavior or attacks

    Finally the code itself is secured by reducing the exposure of secrets to public repositories,   


### Secret's management

    Django use "secret" to generate its certificates and advises to keep this key secret.
    Epinc Events uses the python-decouplemodule to replace the secret key's values of the settings.py file by their decouple link :
    Storing actual secret in a .env file make its possible to keep them local provided one does exclude the .env file from the commits by regitering it in .gitignore.  
  
    For learners we, for ones allowed the commit of this (fake) .env file.  

    ```py
    from decouple import config
    ...
    SECRET_KEY = config("SECRET_KEY")

    ```  

## Epic Events API documentation


Postman documentation link [epicevents_ap](https://documenter.getpostman.com/view/19150435/UzQvt51y)

![](img/p12-end-points.png)  

### Business workflow

We could suggest the following workflow to support an event:

1. Sales adds the new prospect. 
2. Sales updates the prospect status of becoming a true client
3. Sales create a new Contract 
4. Sales updates the status of Contract when the client has signed
5. Sales creates a new Event and allocates it to the support staff
6. Support gets details of the newly allocated event
7. Support updates the event status from Open to Close
8. Management Create, Read, Update or Delete users when required to.

The application structure includes basically 3 levels of embedded models : Clients, Contracts, Events.

For these, the basic CRUD methods are provided thru the available end-points.

The permissions are granted following the user's role in the workflow:

1. Only authenticated user can acces end-points.
2. Only staff can access the admin site.
3. Only Superuser can create a superuser
4. Only Sales creates from Client, Contract, Event
5. Only Support updates the Event

Authentication is managed with Django auth `django.contrib.auth` as well as with ` simple-jwt`  tokens.
Authorization is managed thru the ` has_permission`  method of the permission class 

If you need mock user data for the above role segragation, here is what we suggest:

![](img/p12-sample-data.png)  
  
(A) Support ; (M) Management ; (S) Sales.

Two front ends app are needed for the workflow:
* the provided (and hidden) Django Admin
* the Postman client side.

For the latter, remember when checking User permissions that "admin-oc" is also the Epic Events API superuser.


## Tests passed  


### Django ApiTestCase pass 9/9

![](img/p12-tests-passed-2022-07-16-214829.png)  

![](img/p12-pytest-cov-2022-07-16-213906.png)  


## Credits and good reads.

Openclassrooms and even more the DA Python discord gals & guys!

Offical [Django](https://docs.djangoproject.com/fr/4.0/topics/security/#sql-injection-protection), [DRF](https://www.django-rest-framework.org/) et [pytest](https://docs.pytest.org/en/7.1.x/) documentation!  
  
On owasp and Django, 
[Django vs. the OWASP Top 10 - Part 1](https://blog.nvisium.com/django-vs-the-owasp-top-10-part-1)  
and [10 tips for making the Django Admin more secure | Opensource.com](https://opensource.com/article/18/1/10-tips-making-django-admin-more-secure)
where  Jeff Triplett & Lacey Williams Henschel recommend to change the default admin URL from `/admin/` to something else.

  
Nicely written and opiniated post on    [PyTest with Django REST Framework: From Zero to Hero - DEV Community](https://dev.to/sherlockcodes/pytest-with-django-rest-framework-from-zero-to-hero-8c4) 
kudos @LucasMiguel aka https://dev.to/sherlockcodes  
  
For his clear review of django's permissions, thx @Oluwole Majiyagbe
[Permissions in Django | TestDriven.io](https://testdriven.io/blog/django-permissions/)   

Again and on the previous topic, thank you  @ŠpelaGiacomelli (aka GirlLovesToCode) for your post series, [Custom Permission Classes in Django REST Framework | TestDriven.io](https://testdriven.io/blog/custom-permission-classes-drf/)  

One more on permissions which saved me hours is @marcuslind90 with
[How to restrict access with Django Permissions · Coderbook](https://coderbook.com/@marcus/how-to-restrict-access-with-django-permissions/)   
  
  
it has been a battle to find out how to test with a PostgreSQL database thx here @George Leslie-Waksman for
[Better PostgreSQL testing with Python: announcing pytest-pgsql and pgmock | by George Leslie-Waksman | Clover Health](https://technology.cloverhealth.com/better-postgresql-testing-with-python-announcing-pytest-pgsql-and-pgmock-d0c569d0602a)  
  
on Logging, thx @ Malik Albeik for [Monitoring user actions with LogEntry in Django Admin | Malik Albeik](https://malikalbeik.com/blog/monitoring-user-actions-with-logentry-in-django-ad)  
  
The Real Python not only runs a great podcast but also teaches well, here a review on Django Admin [What You Need to Know to Manage Users in Django Admin – Real Python](https://realpython.com/manage-users-in-django-admin/)  


## PEP 8 check

`flake8 --format=html --htmldir=flake8_report

![](img/p12-flake8-report-2022-07-16-213208.png)  
