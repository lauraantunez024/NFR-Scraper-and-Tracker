# National Film Registry Scraper and Tracker


By itself, this creates a mongoDB connection for your movies and pings to make sure it's connected propertly.

Use the command line arguments for scraping, enriching scraped data, and adding feedback about movies watched. 

## Features and commands

In a .env file you can also add your Radarr api key and the ip address of the machine you're using to host Radarr to have random movies from the national film registry be added to your library for you to enjoy. 

`python scraper.py -s` will do a fresh scrape of the National Film Registry list and insert them into a MongoDB database. 

`python scraper.py -d` enriches movie data by aggregating from OMDB (Open Movie Database)

A user can mark a movie as watched with 

`python scraper.py --watched "Movie Title" ` 

To leave a comment it's

`python scraper.py --rate "Movie Title" 8 "Comments, critiques, etc"`


example would be:

```
python scraper.py --watched "The Lion King"

python scraper.py --rate "The Lion King" 7 "Hey this kind of reminds me of Hamlet??"
```


## Additional Features being currently added
- A web UI to make tracking movies easier

## Future plans:
List of ideas to add
- A way to add marked movies to a csv that can be imported to letterboxd if the user would like to also keep track of their viewed movies there.
- user profiles so people can keep track of the movies from the national film registry they've seen 


If you want to know more about me or work together check out [my website](https://lauraantunez.com)
