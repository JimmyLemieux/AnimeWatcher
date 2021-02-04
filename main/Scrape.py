import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from Helper import *
import Constant

class Scrape:
    def __init__(self, numPages):
        for i in xrange(numPages - 1):
            URL = Constant.ANIME_URL + "{0}".format(i+1)
            self.scrapeShowLogic(URL)
            print ('Scraping page ' + URL)
        pass

    def scrapeShowLogic(self, url):
        website = requests.get(url).content
        soup = BeautifulSoup(website, 'html.parser')
        body = soup.body

        # Soup parsing
        aniDiv = soup.find('div', attrs={'class':'anime_list_body'})
        aniListings = aniDiv.find('ul', attrs={'class':'listing'})
        listItems = aniListings.findAll('li')  

        if(not listItems): 
            print ("Couldn't find the shows page")
            return
        
        for item in enumerate(listItems):
            show = {}
            showTitle = Helper().encodeString(item.text)

            showURL = Helper().showUrlMod(item)
            print (showURL)

            show['showURL'] = showURL
            
            #Here since we now have the url that will take us to the episodes we can then call the code that will handle this page
            episodeLinks = self.scrapeShowEpisodeLogic(showURL)

            videoLinks = []

            for link in episodeLinks:
                videoLink = self.scrapeEpisodeVideo(link)
                videoLinks.append(videoLink)


            show['episodes'] = videoLinks
            show['showTitle'] = showTitle

            linkAttrs = Helper().encodeString(item.attrs['title'])
            soup = BeautifulSoup(linkAttrs, 'html.parser')
            
            meta = []
            for i in soup.findAll('p'):
                meta.append(Helper().encodeString(i.text))

            show['meta'] = meta
            print (show)
            # this should to a database
        print ("#### DONE ####")

    #This is for when we actuallly want to get the video embed link...
    def scrapeEpisodeVideo(self, url):
        website = requests.get(url).content
        soup = BeautifulSoup(website, "html.parser")
        #I need to know find a div with id load_anime
        animeDiv = soup.find("div", attrs={"id":"load_anime"})
        animeIframe = animeDiv.find("iframe")
        showLink = "https:" + Helper().encodeString(animeIframe.attrs["src"])
        return showLink
        #Now that we have the show link we can go ahead and go into the  scrapping og that page

    #Need Selenium for this section of the code
    #This will find the episodes and the link to the page where the video will be
    def scrapeShowEpisodeLogic(self, url):
        episodes = []
        #The url here is for each of the internal episodes for the show
        options = Options()
        options.headless = True
        browser = webdriver.Firefox(options=options)
        browser.get(url)

        try:
            parent = browser.find_element_by_id('load_ep')
            links = parent.find_elements_by_tag_name("a")
        except:
            print ('An error with the ep with selenium')
            return

        for link in links:
            try:
                episodeLink = link.get_attribute('href')
                episodes.append(Helper().encodeString(episodeLink))
            except:
                pass        
        return episodes
