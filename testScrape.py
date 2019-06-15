import requests
import json
from urllib import urlopen
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self):
        #We can begin to call the url modifier
        pass

    #Getters and Setters

    def encodeString(self, string):
        return string.encode('utf8')

    def urlMod(self, pages):
        URL = ""
        shows = []
        for i in xrange(pages):
            URL = "https://www4.gogoanime.io/anime-list.html?page={0}".format(i)
            self.scrapeShowLogic(URL, shows)
        
        print shows

    def scrapeShowLogic(self, url, shows):
        website = urlopen(url).read()
        soup = BeautifulSoup(website, 'html.parser')
        
        #Start to find all of the show titles for each of the shows

        #The main section is in the body so we can start with that
        body = soup.body

        #Within the body we can find a specfic div with id

        aniDiv = soup.find('div', attrs={'class':'anime_list_body'})

        aniListings = aniDiv.find('ul', attrs={'class':'listing'})

        listItems = aniListings.findAll('li')  

        linkShows = []

        #Each list Item will have an a tag that will have to be followed and then scrapped
        #A show will now have a list of episodes and then hopefully video links or some sort of source
        
        if(len(listItems)): 
            for item in listItems:
                show = {}
                showTitle = self.encodeString(item.text)
                show['showTitle'] = showTitle
                #This is returning more html code that needs to be scrapped further
                linkAttrs = self.encodeString(item.attrs['title'])
                soup = BeautifulSoup(linkAttrs, 'html.parser')
                
                meta = []
                for i in soup.findAll('p'):
                    meta.append(self.encodeString(i.text))
                show['meta'] = meta
                linkShows.append(show)
                pass
            shows.append(linkShows)
        print "#### DONE ####"


while __name__ == '__main__':
    #Main
    scrape = Scraper()
    scrape.urlMod(50)
    break