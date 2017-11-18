from clarifai import rest
from clarifai.rest import ClarifaiApp
import os, sqlite3

db = sqlite3.connect('./web/data/crawler')


cursor = db.cursor()
cursor.execute('SELECT * FROM links')
for row in cursor:
    # row['name'] returns the name column in the query, row['email'] returns email column.
    print "Geting: " + str(row[0]) + " " + row[2]

    #print('Getting info link id {0} = {1}'.format(row["id"], row["link"]))

    url1 = row[2]

    app = ClarifaiApp(api_key='f607cf42c8b64ff499931bdf6a5a53a6')
    # get the general model
    model = app.models.get("general-v1.3")
    # predict with the model
    response = model.predict_by_url(url=url1)

    concepts = response['outputs'][0]['data']['concepts']
    for concept in concepts:
        print(concept['name'], concept['value'])

db.close()




    






