A anime recommendation website that data scrapes anime and recommends them through genres, scores, and other different attributes.

![Screenshot 2024-09-18 004340](https://github.com/user-attachments/assets/6f418063-9322-47e8-ba46-acd2aa0d3e5f)

![Screenshot 2024-09-18 004426](https://github.com/user-attachments/assets/fd70b89c-3c87-43c7-b068-aa7194de1a8c)

![Screenshot 2024-09-18 004504](https://github.com/user-attachments/assets/bc065db9-3be9-4b97-8ef4-30e03a417189)

Frameworks:
Django, Django_restframework, React, Pandas, BeautifulSoup 4

Requirements: 
React, Pip, Pipenv 

How to Run:

Before running, makesure you have docker installed and opened.

Run
docker-compose -f docker-compose.fullstack.yml up --build

If this is your first time, you need to scrape and obtain anime metadata. Do do this, make sure the container is up and run:
docker exec -it aniproj_backend python manage.py scraper
docker exec -it aniproj_backend python manage import_json
