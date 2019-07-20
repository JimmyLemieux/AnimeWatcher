from testScrape import *
from database import *


while __name__ == '__main__':
    #First we are going to config the database and then start the scraping

    #When we create the new database object, we should return an instance of the db and then send it into the scraper

    db = DataBase()
    showCollection = db.getShowCollection()
    scrape = Scraper(50, showCollection)




    break





