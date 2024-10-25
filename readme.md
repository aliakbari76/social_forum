
## **how to run this project**

1- creat virtual environment : 

            python -m venv <virtual environment name>

2- install requirements.txt : 

            pip install -r requirements.txt

3- run postgres in your local machine and set postgres connection data in your dev.env

4- run redis on your local machine and set redis connection data in your dev.env

5- migrate models

        python manage.py migrate

6- run celery worker on a new terminal : 

on windows :

        celery -A bitpin_forum worker -l info -P eventlet

on ubuntu : 

        <virtual environment name>/bin/celery -A bitpin_forum worker --loglevel=info

7- run celery beat on a new terminal : 

on windows : 

        celery -A bitpin_forum beat -l info

on ubuntu : 

        <virtual environment name>/bin/celery -A bitpin_forum beat -l info

8- finaly run project :

        python manage.py runserver



 **for using apps there is a rest_call folder that contain all apis in curl format**