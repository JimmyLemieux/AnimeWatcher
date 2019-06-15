import requests
from urllib import urlopen
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self):
        #We can begin to call the url modifier
        pass

    def urlMod(self, pages):
        URL = ""
        for i in xrange(pages):
            URL = "https://www4.gogoanime.io/anime-list.html?page={0}".format(i)
            self.scrapeShowLogic(URL)


    def scrapeShowLogic(self, url):
        website = urlopen(url).read().decode('utf8')
        soup = BeautifulSoup(website, 'html.parser')
        
        #Start to find all of the show titles for each of the shows

        #The main section is in the body so we can start with that
        body = soup.body

        #Within the body we can find a specfic div with id

        aniDiv = soup.find('div', attrs={'class':'anime_list_body'})

        aniListings = aniDiv.find('ul', attrs={'class':'listing'})

        listItems = aniListings.findAll('li')  

        if(len(listItems)): 
            for item in listItems:
                print (item.text).encode('utf8')    
        
        print "#### DONE ####"


while __name__ == '__main__':
    #Main

    scrape = Scraper()
    scrape.urlMod(50)
    break