import urllib2
import sys
# import re
import threading

from bs4 import BeautifulSoup
#from BeautifulSoup import BeautifulSoup

# GET user value from argument or using 'default'
active_user = "twittersoz"
if len(sys.argv) == 2:
    active_user = sys.argv[1]


# Thread worker for active_user
def worker(active_user):
    print "Analizyng user: " + active_user


    

    return

# Llista threads actius
threads = list()

t = threading.Thread(target=worker, args=(active_user,))
threads.append(t)
t.start()

# Parse active user
response = urllib2.urlopen('https://www.instagram.com/' + active_user)
html = response.read()
soup = BeautifulSoup(html, "html.parser")


users = []
scanned_users = []


file_users = open("users_" + active_user + ".txt","w") 


def parse_users(soup):
    for coses in soup.find_all('a'):
        #print coses.get('a')
        #nicks = coses.find_all('a')
        conv = str(coses)
        for tag in conv.split('>'):
            if "@" in tag:
                tag2 = tag.split(' ')
                for element in tag2:
                    if "@" in element:
                        usuari = element.replace("@", "")
                        if usuari not in users:
                            users.append(usuari)
                            file_users.write(usuari + "\n")
                        #if re.match(r'.*[\%\$\^\*\@\!\_\-\(\)\:\;\'\"\{\}\[\]].*', element):
                        #if set('[~!@#$%^&*()_+{}":;\']+$').intersection(element):
                        #print element

parse_users(soup)

file_users.close()
print users
    #print '*****' + str(coses)

'''
print soup
for line in soup.split('\n'):
    for line2 in line.split('@'):
        print line2'''

'''for link in soup.find_all('link'):
    print link
    #print(link.get('href'))'''


'''
for line in html.split('\n'):
    for line2 in line.split('@'):
        print [pos for pos, char in enumerate('@') if char == '@']'''


    #res = [k for k in line if '@' in k]
    #print res
