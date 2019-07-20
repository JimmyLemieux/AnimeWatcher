![Some Anime](http://is2.4chan.org/c/1560470679005.jpg) ![Other Anime](http://is2.4chan.org/c/1558566884494.jpg)

## What we have

So most of the basic things are done so far. We have a class that can modify a URL and scrape through every single show title that is on each of these pages.


    > What I plan to do next is gather more information about each of these show titles. Maybe brief synopsis and genre. I will also have to go through each of the links associated with the tiles and find all episodes

    > A Quick update I have started to find more of the other tags that are related to the name of the show. Such as Genre, Status, Date and Plot Summary!
        I need to set up the *SSH* for my bitbucket to make it easier to push things to my repo

    > Another update, I was able to put all of the shows on the main page into a big object. The next step is to get the individual episodes from each show title

    Before I continue I need to make sure that I can actually find and somehow get the source URL for a video

## Quick Road Block

    > So I ran into a weird problem when scraping the individual episodes for a show. It appears that when I try to scrape the page, there is JS that is still to be executed, therefore I cannot find the specific elements that I need.
    There is a tool called Selenium that has controls for me to either wait or force execute these JS triggers. 

    **I am going to leave this for now and continue with just scrapping. I still need to follow each show link to get the individual
    episodes!**

## Some more updates
    Today was a very productive day in the sense of these things. I figured out the issues I was having with the scraper. It was a simple fix that had something to do with the selenium driver. I was finding all the a tags on the current screen and I was getting random episodes that apperered in redundant locations across the screen. So instead I just limited the area of search. Which is something that I should have done from the beginning.

    I also was able to get a local mongodb set up on ubuntu. I can start to store things in a local database 