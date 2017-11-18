import urllib2
import sys
# import re
from threading import Thread
from bs4 import BeautifulSoup


# GET user value from argument or using 'default'
active_user = "twittersoz"
if len(sys.argv) == 2:
    active_user = sys.argv[1]


class Crawler(Thread):
    users = []
    scanned_users = []
    active_user = ""

    def __init__(self, active_user):
        Thread.__init__(self)
        self.active_user = active_user

    # Thread worker for active_user
    def run (self):
        print "Analizyng user: " + active_user

        # Parse active user
        response = urllib2.urlopen('https://www.instagram.com/' + active_user)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        # Parse users
        self.parse_users(soup)


    def parse_users(self, soup):
        file_users = open("users_" + active_user + ".txt","w") 
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
                            if usuari not in self.users:
                                self.users.append(usuari)
                                file_users.write(usuari + "\n")
                            #if re.match(r'.*[\%\$\^\*\@\!\_\-\(\)\:\;\'\"\{\}\[\]].*', element):
                            #if set('[~!@#$%^&*()_+{}":;\']+$').intersection(element):
                            #print element
        file_users.close()
        #Add user to users analized
        file_users_analized = open("analized_users.txt","w")
        file_users_analized.write(self.active_user + "\n")
        file_users_analized.close() 


    def join( self ):
        Thread.join( self )
        return self.users




# Llista threads actius
e = Crawler(active_user)
e.start()
print e.join()


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
