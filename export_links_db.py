import sqlite3
import os.path

db = sqlite3.connect('web/data/crawler')

# Get links from file and return
def get_links(username):
    links = []
    file_exist = os.path.isfile('./links_' + username + ".txt") 
    if file_exist:
        file_links = open("links_" + username + ".txt","r") 
        for line in file_links:
            links.append(line)
        file_links.close()
    return links

cursor = db.cursor()
for filename in os.listdir('.'):
    # print filenames of dir
    if ("links_" in filename):
        user = filename.split("links_")[1]
        userbo = user.split(".txt")[0]
        llistat = get_links(userbo)
        #Insert link
        for link in llistat:
            cursor.execute('''INSERT INTO links(nickname, link) VALUES(?,?)''', ((userbo,link, )) )
            print "Adding: " + userbo + " amb link: " + link + " to DB."

db.commit()

# Tanca DB
db.close()


