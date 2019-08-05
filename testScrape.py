import sys
import time
import requests
import json
from urllib import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

#mysql connector is beggining here
# import mysql.connector as mysql

class Scraper:
    def __init__(self, numPages, dbCollection):
        #we can begin to call the url modifier
        self.dbCollection = dbCollection
        self.initShowObject(numPages)
        pass

    #getters and setters

    def encodeString(self, string):
        return string.encode('utf8')

    def initShowObject(self, pages):
        URL = ""
        shows = []
        for i in xrange(pages - 1):
            URL = "https://www4.gogoanime.io/anime-list.html?page={0}".format(i + 1)
            print 'Scraping page ' + URL
            self.scrapeShowLogic(URL, shows)
        

    def showUrlMod(self, item):
        showURL = "https://www4.gogoanime.io"
        showEndpoint = self.encodeString(item.find('a').attrs['href'])
        showURL += showEndpoint
        return showURL


    def utilPrint(self, show):
        print 'PRINTING SHOW--'
        print 'TITLE: ' + show['showTitle']
        print 'EPs: '
        for i in show['episodes']:
            print i

        print 'META: '       
        for i in show['meta']:
           print i 


    def scrapeShowLogic(self, url, shows):
        try:
            website = urlopen(url).read()
            soup = BeautifulSoup(website, 'html.parser')
            
            #Start to find all of the show titles for each of the shows

            #The main section is in the body so we can start with that
            body = soup.body

            #Within the body we can find a specfic div with id

            aniDiv = soup.find('div', attrs={'class':'anime_list_body'})

            aniListings = aniDiv.find('ul', attrs={'class':'listing'})

            listItems = aniListings.findAll('li')  

            #Each list Item will have an a tag that will have to be followed and then scrapped
            #A show will now have a list of episodes and then hopefully video links or some sort of source

            if(len(listItems)): 
                counter = 1
                for item in listItems:
                    show = {}
                    showTitle = self.encodeString(item.text)

                    #check if the showTitle is already present in the database, if it is then skip this entry                    

                    #See if we can find all of the a tags and there source links from here

                    showURL = self.showUrlMod(item)

                    #With this showURL we should now ho and scrape each of the episodes that are apart of a show
                    #self.scrapeShowEpisodeLogic(showURL)

                    show['showURL'] = showURL

                    #Here since we now have the url that will take us to the episodes we can then call the code that will handle this page
                    episodeLinks = self.scrapeShowEpisodeLogic(show['showURL'])

                    videoLinks = []

                    # loop through the episode links and then you can add them in there

                    for link in episodeLinks:
                        videoLink = self.scrapeEpisodeVideo(link)
                        videoLinks.append(videoLink)



                    show['episodes'] = videoLinks


                    show['showTitle'] = showTitle


                    #This is returning more html code that needs to be scrapped further
                    linkAttrs = self.encodeString(item.attrs['title'])
                    soup = BeautifulSoup(linkAttrs, 'html.parser')
                    
                    meta = []
                    for i in soup.findAll('p'):
                        meta.append(self.encodeString(i.text))
                            
                                
                    show['meta'] = meta

                    self.dbCollection.insert_one(show)  
                    print "Inserted into the database"
                    print showTitle + "{0}/{1}".format(counter, len(listItems))
                    counter += 1
        except:
            print "There was an exception so we are skipping"
            pass
        print "#### DONE ####"




    #This is for when we actuallly want to get the video embed link...
    def scrapeEpisodeVideo(self, url):
        website = urlopen(url).read()
        soup = BeautifulSoup(website, "html.parser")
        #I need to know find a div with id load_anime
        animeDiv = soup.find("div", attrs={"id":"load_anime"})
        animeIframe = animeDiv.find("iframe")
        showLink = "https:" + self.encodeString(animeIframe.attrs["src"])
        return showLink
        #Now that we have the show link we can go ahead and go into the  scrapping og that page




    #Need Selenium for this section of the code
    #This will find the episodes and the link to the page where the video will be
    def scrapeShowEpisodeLogic(self, url):
        
        episodes = []
        #The url here is for each of the internal episodes for the show

        browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        browser.get(url)

        parent = browser.find_element_by_id('load_ep')

        links = parent.find_elements_by_tag_name("a")

        for link in links:
            try:
                episodeLink = link.get_attribute('href')
                episodes.append(self.encodeString(episodeLink))
            except:
                pass
        
        return episodes
