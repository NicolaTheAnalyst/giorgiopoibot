# -*- coding: utf-8 -*-

import os
import logging
import sqlite3
import googleapiclient.discovery
import googleapiclient.errors

logging.basicConfig(filename='logcaller.txt', format= "%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger()

def table_update(id,title,url):
    logger.info("Connecting to the DB..")
    try:
        sqliteConnection = sqlite3.connect('Songstest.db') #test database
        cursor = sqliteConnection.cursor()
    except:
        logger.error("Error while connecting to the DB", exc_info=True)

    logger.info("Querying the DB..")
    try:
        for element in range(len(id)):
            sqlite_insert_query  = """INSERT OR REPLACE INTO Songs
                                  (Autore, Titolo, URL) 
                                   VALUES 
                                  ("Giorgio Poi", "{title}", "{url}") 
                                  """.format(title = title[element], url = url[element])
            print(sqlite_insert_query)
            count = cursor.execute(sqlite_insert_query)
            sqliteConnection.commit()
    except:
        logger.error("Error while inserting query", exc_info=True)

    logger.info("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
    cursor.close()


def main():
    api_service_name = "youtube"
    api_version = "v3"
    api_key = os.environ.get("API_KEY")
    id_number = 0
    id = []
    title = []
    url = []
    youtube_prefix = "https://www.youtube.com/watch?v="
    youtube = googleapiclient.discovery.build(api_service_name,api_version, developerKey = api_key)

    logger.info("Calling youtube..")
    try:
        request = youtube.search().list(
            part="snippet",
            channelId="UCNGqOnZoBRKPp51xOmXDCRQ", #https://www.youtube.com/channel/UCNGqOnZoBRKPp51xOmXDCRQ Giorgio poi tema
            maxResults=40,
            type="video"
        )
        response = request.execute()
    except:
        logger.error("Error while calling youtube", exc_info=True)

    logger.info("Cycling on the response")
    try:
        for i in response['items']:
            id_number += 1
            id.append(id_number)
            title.append(str(i['snippet']['title']))
            url.append(youtube_prefix + str(i['id']['videoId']))
    except:
        logger.error("Error while cycling on the response", exc_info=True)

    table_update(id,title,url)

if __name__ == "__main__":
    main()