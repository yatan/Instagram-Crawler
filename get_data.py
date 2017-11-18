from bs4 import BeautifulSoup
import selenium.webdriver as webdriver

from clarifai import rest
from clarifai.rest import ClarifaiApp

url = 'http://instagram.com/umnpics/'
driver = webdriver.Chrome()
driver.set_window_size(300, 300) # set window size
driver.get(url)

soup = BeautifulSoup(driver.page_source, "html.parser")

for foto in soup.findAll('img'):
    print foto.get('alt', '')
    print foto.get('src', '')


driver.close()

app = ClarifaiApp(api_key='f607cf42c8b64ff499931bdf6a5a53a6')

# get the general model
model = app.models.get("general-v1.3")

# predict with the model
response = model.predict_by_url(url='https://samples.clarifai.com/metro-north.jpg')

concepts = response['outputs'][0]['data']['concepts']
for concept in concepts:
    print(concept['name'], concept['value'])