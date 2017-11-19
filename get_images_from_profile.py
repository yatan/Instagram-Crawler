from bs4 import BeautifulSoup
import os
import selenium.webdriver as webdriver
import sqlite3

db = sqlite3.connect('web/data/crawler')

# Check user not exist on DB
def check_existed_user(username):
    cursor = db.cursor()
    cursor.execute('SELECT COUNT(*) FROM links WHERE nickname="' + username + '"')
    if cursor.fetchone()[0] == 0:
        return False
    else:
        return True

def get_img_url(url):
    direccions = []

    url = 'http://instagram.com/' + url
    driver = webdriver.Chrome()
    driver.set_window_size(300, 300) # set window size
    driver.get(url)


    soup = BeautifulSoup(driver.page_source, "html.parser")

    for foto in soup.findAll('img'):
        #print foto.get('alt', '')
        direccions.append( foto.get('src', '') )

    driver.close()
    print direccions
    return direccions

for filename in os.listdir('.'):
    # print filenames of dir
    if ("users_" in filename):
        user = filename.split("users_")[1]
        userbo = user.split(".txt")[0]
        if (check_existed_user(userbo) == False):
            file_links = open("links_" + userbo + ".txt","w") 
            links = get_img_url(userbo)
            for items in links:
                file_links.write(items + "\n")
            file_links.close()


