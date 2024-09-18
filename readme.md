A anime recommendation website that data scrapes anime and recommends them through genres, scores, and other different attributes.


![Screenshot 2024-09-18 001403](https://github.com/user-attachments/assets/8be1e197-0685-4513-ab5a-bde22897d172)

Frameworks:
Django, Django_restframework, React, Pandas, BeautifulSoup 4

Requirements: 
React, Pip, Pipenv 

How to Run:

Before running, makesure you have pipenv installed as well as postgresql
the local database config is
"       'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'aniproj',
        'USER': 'postgres',
        'PASSWORD' : 'postgres'"
To set up pipenv, use "pipenv install" and then "pipenv shell" to activate a virtual environment.
To run the following programs, you need to have activated a pipenv VE.
Scrape data:
  In the scraper folder, use ./py scraper.py or ./python scraper.py
  then go to server and type : "./python ./manage.py import_json"

To start server:
  go to ./server and type "./python ./manage.py makemigrations" and then "./python ./manage.py migrate"
  then to start server, type "./python ./manage.py runserver"

To start client:
  "npm install"
  "npm start"
