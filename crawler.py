import urllib2
from bs4 import BeautifulSoup
#from BeautifulSoup import BeautifulSoup
response = urllib2.urlopen('https://www.instagram.com/twittersoz/')
html = response.read()
soup = BeautifulSoup(html, "html.parser")

for coses in soup.find_all('a'):
    #print coses.get('a')
    #nicks = coses.find_all('a')
    conv = str(coses)
    for tag in conv.split('>'):
        if "@" in tag:
            tag2 = tag.split(' ')
            for element in tag2:
                if "@" in element:
                    print element


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
