# DOCUMENTATION


### ABOUT
Hosted on [www.sudogami.com](www.sudogami.com)

TO DO list at the bottom.

This is an RSS feed for the [Merveilles webring project](https://github.com/XXIIVV/Webring/), it's a static page that's updated once daily with all the recent articles written by the community.

## HOW DOES IT WORK?

On the backend, we're running a postgres database that is populated and maintained by the python scripts below. Cron is used to ensure that these scripts are run in a certain order once daily at 08:00 ET. These scripts eventually output to a JSON file that the front end uses to populate a static web page.

You can see the database schema [here](https://github.com/LiminalCrab/fucking-bulletproof). This is the meme way I'm storing backups of the database. It's completely unncessary.

## CODE

### data/pull.py
This is the start point for the backend. This is the first script ran by Cron. The links here are only scraped from their **titles** and **urls** and they're submitted to a postgres database.

### data/date.py 
This is the second script that Cron runs seconds after pull.py,
it's purpose is to simply scrape the dates from each article of each website in the urls array and submit it to the database. This is to take some of the load off of pull.py. 

### data/matchdrop.py 
This is the third script that Cron runs seconds after date.py. 
It's job is to look for any tables/rows that might be missing data or is a duplicate of something already stored and remove it from the database. I still have some work to do here, but for now it gets the job done.
This script returns an exception if there are no duplicates.

### createHTML.py 
This replaces the old linkhandler.js, and is responsible for populating the HTML with the data from the db.

# TO DO

- [X] Jinja implementation
    - [X] Remove Javascript / JSON, allow the database to populate the html directly.
    - [ ] make it so their website favicons show up beside their articles
    - [ ] limit posts per page to 50 or 100.
    - [ ] add post summaries. 
- [ ] POSTGRESQL
    - [ ] add row for post_summaries, url_favicon, url_name.
- [ ] pull.py
    - [ ] Scrape for favicons.
    - [ ] Scrape for post_summaries and only collect (250 characters?)
- [X] order.py
    - [ ] decouple from JSON
    - [ ] direct db output to html.
    - [X] this might actually become obsolete.
- [ ] Docker
    - [ ] Create a Dockerfile
    - [ ] Have a run script to output the HTML file