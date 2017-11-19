from clarifai import rest
from clarifai.rest import ClarifaiApp
import os, sqlite3

db = sqlite3.connect('./web/data/crawler')

def check_existed_link_id(link_id):
    cursor = db.cursor()
    cursor.execute('SELECT COUNT(*) FROM data WHERE link_id="' + link_id + '"')
    if cursor.fetchone()[0] == 0:
        return False
    else:
        return True

def get_API(photo_url):
    app = ClarifaiApp(api_key='f607cf42c8b64ff499931bdf6a5a53a6')
    # get the general model
    model = app.models.get("general-v1.3")
    # predict with the model
    response = model.predict_by_url(url=photo_url)

    concepts = response['outputs'][0]['data']['concepts']
    return concepts

'''     for concept in concepts:
        print(concept['name'], concept['value']) '''

cursor = db.cursor()
cursor.execute('SELECT * FROM links')
for row in cursor:
    # row['name'] returns the name column in the query, row['email'] returns email column.
    photo_id = str(row[0])
    if not check_existed_link_id(photo_id):
        print "Geting info id: " + photo_id + " url: " + row[2]

        #print('Getting info link id {0} = {1}'.format(row["id"], row["link"]))
        # Get API info to DB
        # for concept in concepts:
        #    print(concept['name'], concept['value'])
        concepts = get_API(row[2])
        cursor2 = db.cursor()
        for concept in concepts:
            cursor2.execute('INSERT INTO data(link_id, type, posible) VALUES(?,?,?)', ((str(row[0]), concept['name'], str(concept['value'])) ))
            print "Adding id: " + str(row[0]) + " " + concept['name'] + ":" + str(concept['value']) + " to DB."
        # Write Changes
        db.commit()
    else:
        print photo_id + " ja existeix."

db.close()




    






