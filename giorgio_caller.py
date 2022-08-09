# -*- coding: utf-8 -*-

import os
from datetime import datetime
import yagmail
import logging
import sqlite3
import googleapiclient.discovery
import googleapiclient.errors

logging.basicConfig(filename='logcaller.txt', format= "%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger()

sender_email = os.environ.get("sender_mail")
receiver_email = os.environ.get("receiver_mail")
yag = yagmail.SMTP(sender_email, oauth2_file='oauth2_creds.json')

def send_email(status, msg):
    dt = datetime.now()
    subject = "Giorgio Poi caller log: {status}".format(status = status)
    body = """Esito: {text}
    Email generated: {dt}
    """.format(text = msg, dt = dt)
    yag.send(to=receiver_email,subject = subject,contents = body)
    return


def table_update(id,title,url):
    logger.info("Connecting to the DB..")
    try:
        sqliteConnection = sqlite3.connect('Songstest.db') #test database
        cursor = sqliteConnection.cursor()
    except Exception as e:
        logger.error("Error while connecting to the DB", exc_info=True)
        status = "KO"
        msg = e
        send_email(status, msg)

    logger.info("Querying the DB..")
    try:
        for element in range(len(id)):
            sqlite_insert_query  = """INSERT OR REPLACE INTO Songs
                                  (Autore, Titolo, URL) 
                                   VALUES 
                                  ("Giorgio Poi", "{title}", "{url}") 
                                  """.format(title = title[element], url = url[element])
            #print(sqlite_insert_query)
            count = cursor.execute(sqlite_insert_query)
            sqliteConnection.commit()
    except Exception as e:
        logger.error("Error while inserting the query", exc_info=True)
        status = "KO"
        msg = e
        send_email(status, msg)

    try:
        logger.info("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
    except:
        pass
    cursor.close()
    status = "OK"
    msg = "OK."
    send_email(status, msg)


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
    try: #calling youtube
        request = youtube.search().list(
            part="snippet",
            channelId="UCNGqOnZoBRKPp51xOmXDCRQ", #https://www.youtube.com/channel/UCNGqOnZoBRKPp51xOmXDCRQ Giorgio poi tema
            maxResults=40,
            type="video"
        )
        response = request.execute()
    except Exception as e:
        logger.error("Error while calling youtube", exc_info=True)
        status = "KO"
        msg = e
        send_email(status, msg)

    logger.info("Cycling on the response")
    try:
        for i in response['items']: #get info from the response
            id_number += 1
            id.append(id_number)
            title.append(str(i['snippet']['title'])) #get the title
            url.append(youtube_prefix + str(i['id']['videoId'])) #get and compose the URL: "https://www.youtube.com/watch?v=" + videoId
    except Exception as e:
        logger.error("Error while cycling on the response", exc_info=True)
        status = "KO"
        msg = e
        send_email(status, msg)

    table_update(id,title,url)

if __name__ == "__main__":
    main()