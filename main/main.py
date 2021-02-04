from Scrape import *
import mysql.connector as sql

while __name__ == '__main__':
    AnimeDB = sql.connect( #running local MySql
        db="SHOWS",
        host="localhost",
        user="root",
        password="[8AdQGs_#BsA&/:{"
    )

    cursor = AnimeDB.cursor()
    # cursor.execute("CREATE DATABASE SHOWS")
    scrape = Scrape(50, AnimeDB)
    break





