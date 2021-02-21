import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from Helper import *
import Constant
import time

class Scrape:
    def __init__(self, numPages, AnimeDB):
        cursor = AnimeDB.cursor()
        for i in xrange(numPages - 1):
            URL = Constant.ANIME_URL + "{0}".format(i+1)
            print ('Scraping page ' + URL)
            shows = self.scrapeShowLogic(URL)
            print ("Starting db stuff")
            for show in shows:
                print (show)
                continue
                sql = "INSERT INTO providedShows (showTitle, showURL) VALUES (%s, %s)"
                val = (show["showTitle"], show["showURL"])
                cursor.execute(sql, val)
                AnimeDB.commit()

                rowId = cursor.lastrowid()
                for episode in show['episodes']:
                    sql = "INSERT INTO providedEpisodes (episodeName, episodeIFrame, showID) VALUE (%s, %s, %d)"
                    val = (episode)
                print(cursor.rowcount, "record inserted.")
        pass

    def scrapeShowLogic(self, url):
        shows = []
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
        
        for _, item in enumerate(listItems):
            show = {}
            showTitle = Helper().encodeString(item.text)

            showURL = Helper().showUrlMod(item)
            print (showURL)

            showPage = requests.get(showURL).content
            animeSoup = BeautifulSoup(showPage, 'html.parser')

            imageDiv = animeSoup.find('div', attrs={'class': 'anime_info_body_bg'})
            show['showImg'] = imageDiv.find('img')['src']

            show['showURL'] = showURL
            
            #Here since we now have the url that will take us to the episodes we can then call the code that will handle this page
            episodeLinks = self.scrapeShowEpisodeLogic(showURL)
            print (episodeLinks)

            videoLinks = []

            for link in episodeLinks:
                videoLink = self.scrapeEpisodeVideo(link)
                # print (videoLink)
                videoLinks.append(videoLink)


            show['episodes'] = videoLinks
            show['showTitle'] = showTitle

            linkAttrs = Helper().encodeString(item.attrs['title'])
            soup = BeautifulSoup(linkAttrs, 'html.parser')
            
            meta = []
            for i in soup.findAll('p'):
                meta.append(Helper().encodeString(i.text))

            show['meta'] = meta
            shows.append(show)
            # this should to a database
            print (show)
    
        print ("#### DONE ####")
        return shows

    #This is for when we actuallly want to get the video embed link...
    def scrapeEpisodeVideo(self, url):
        website = requests.get(url).content

        soup = BeautifulSoup(website, 'html.parser');
        #I need to know find a div with id load_anime
        animeDiv = soup.find("div", attrs={"id":"load_anime"})
        if (not animeDiv): return ""
        animeIframe = animeDiv.find("iframe")
        showLink = "https:" + Helper().encodeString(animeIframe.attrs["src"])
        return showLink
        #Now that we have the show link we can go ahead and go into the  scrapping og that page

    #Need Selenium for this section of the code
    #This will find the episodes and the link to the page where the video will be
    def scrapeShowEpisodeLogic(self, url):

        website = requests.get(url).content

        episodes = []
        #The url here is for each of the internal episodes for the show
        options = Options()
        options.headless = False

        browser = webdriver.Chrome(executable_path="./bin/chromedriver",options=options)
        browser.get(url)
        browser.implicitly_wait(5000)

        #Use the BSoup parser here to speed this up

        #bs_obj = BeautifulSoup(website, 'html.parser')
        try:
            parent = browser.find_element_by_id(id='episode_related')
            print("debug")
            #parent = bs_obj.find(id='load_ep')
            links = parent.find_element_by_tag_name("a")
            #links = parent.findAll("a")
        except:
            print ('An error with the ep with selenium')
            return

        for link in links:
            try:
                episodeLink = link.get_attribute('href')
                #episodeLink = link.find('href').text
                episodes.append(Helper().encodeString(episodeLink))
            except:
                print ("Error")
                pass
        browser.close()
        return episodes
