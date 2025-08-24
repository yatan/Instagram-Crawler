import sqlite3
import os.path

#Check file db exist
file_exist = os.path.isfile('./web/data/crawler') 

db = sqlite3.connect('web/data/crawler')

# Si no existeix, inicialitzem la DB
if not file_exist:
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE users(id INTEGER PRIMARY KEY, nickname TEXT)
    ''')
    db.commit()

cursor = db.cursor()
for filename in os.listdir('.'):
    # print filenames of dir
    if ("users_" in filename):
        user = filename.split("users_")[1]
        userbo = user.split(".txt")[0]
        #Insert userbo
        cursor.execute('''INSERT INTO users(nickname) VALUES(?)''', ((userbo,)) )
        print("Adding: " + userbo + " to DB.")

db.commit()

# Tanca DB
db.close()