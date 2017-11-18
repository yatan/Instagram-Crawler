import urllib2
import re
from bs4 import BeautifulSoup
#from BeautifulSoup import BeautifulSoup
active_user = "twittersoz"
response = urllib2.urlopen('https://www.instagram.com/' + active_user)
html = response.read()
soup = BeautifulSoup(html, "html.parser")

users = []
file_users = open("users.txt","w") 


for coses in soup.find_all('a'):
    #print coses.get('a')
    #nicks = coses.find_all('a')
    conv = str(coses)
    for tag in conv.split('>'):
        if "@" in tag:
            tag2 = tag.split(' ')
            for element in tag2:
                if "@" in element:
                    users.append(element.replace("@", ""))
                    file_users.write(element.replace("@", "") + "\n")
                    #if re.match(r'.*[\%\$\^\*\@\!\_\-\(\)\:\;\'\"\{\}\[\]].*', element):
                    #if set('[~!@#$%^&*()_+{}":;\']+$').intersection(element):
                    #print element

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
