import csv, requests
from bs4 import BeautifulSoup


url =  'https://www.loc.gov/programs/national-film-preservation-board/film-registry/complete-national-film-registry-listing/'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    films = []
    table_body = soup.find('tbody')
    if table_body:
        rows = table_body.find_all('tr')
        for row in rows:
            film_name = row.find('th')
            if film_name:
                films.append(film_name.text.strip())
    with open('films.csv', mode='w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Film Name'])
        for film in films:
            writer.writerow([film])
    print('Films csv successfully created')
else: 
    print('Error {response.status_code}')






