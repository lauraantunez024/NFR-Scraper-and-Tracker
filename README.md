# National Film Registry Scraper and Tracker


This scrapes the National Film Registry site, adds the year released and film title to a Mongodb database, and leaves room for a rating and comment. 

A user can mark a movie as watched with 

`python scraper.py --watched "Movie Title" ` 

To leave a comment it's

`python scraper.py --rate "Movie Title" 8 "Comments, critiques, etc"`


example would be:

```
python scraper.py --watched "The Lion King"

python scraper.py --rate "The Lion King" 7 "Timon and Pumba are still my favorite characters of this movie.... 22 years later"
```

Also left the csv of the national film registry movie names for whoever wants them for themselves

## Additional Features I've added
- Added radarr so that when a movie is picked, it can automatically start downloading to a folder to then be served through either Plex or Jellyfin
- Added movie API that includes additional information not initially provided by the film registry graph. Can be added to a local mongodb.
- Added a movie API with a front end that adds the movie posters to better be able to select them 

## Future plans:
List of ideas to add
- A way to add marked movies to a csv that can be imported to letterboxd if the user would like to also keep track of their viewed movies there.


If you want to know more about me or work together check out [my website](https://lauraantunez.com)
