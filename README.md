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


## Future plans:
List of ideas to add
- A front end attached to a movie api to give movie names their movie posters
- Just some kind of user friendly front end situation in general


If you want to know more about me or work together check out [my website](https://lauraantunez.com)