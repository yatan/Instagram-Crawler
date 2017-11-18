from clarifai import rest
from clarifai.rest import ClarifaiApp

url1 = "https://scontent-mad1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/22500209_124269068257773_2270043748131930112_n.jpg"

app = ClarifaiApp(api_key='f607cf42c8b64ff499931bdf6a5a53a6')
# get the general model
model = app.models.get("general-v1.3")
# predict with the model
response = model.predict_by_url(url=url1)

concepts = response['outputs'][0]['data']['concepts']
for concept in concepts:
    print(concept['name'], concept['value'])

    






