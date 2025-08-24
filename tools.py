import sqlite3
import os
import sys
from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
import requests

def get_images_from_profile():
    db = sqlite3.connect('web/data/crawler')
    def check_existed_user(username):
        cursor = db.cursor()
        cursor.execute('SELECT COUNT(*) FROM links WHERE nickname=?', (username,))
        return cursor.fetchone()[0] != 0
    def get_img_url(url):
        from selenium.webdriver.chrome.options import Options
        import time
        direccions = []
        url = 'https://www.instagram.com/' + url
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1200,800')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(5)  # Espera para cargar JS
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for foto in soup.find_all('img'):
            src = foto.get('src', '')
            if src and 'profile_pic' not in src:
                direccions.append(src)
        if not direccions:
            print("No se encontraron imágenes. Puede que Instagram requiera login o el contenido esté protegido.")
            print("HTML obtenido:")
            print(driver.page_source[:2000])  # Muestra los primeros 2000 caracteres para depuración
        driver.close()
        print(direccions)
        return direccions
    for filename in os.listdir('.'):
        if ("users_" in filename):
            user = filename.split("users_")[1].split(".txt")[0]
            if not check_existed_user(user):
                file_links = open("links_" + user + ".txt","w")
                links = get_img_url(user)
                for items in links:
                    file_links.write(items + "\n")
                file_links.close()
    db.close()

def show_users():
    db = sqlite3.connect('./web/data/crawler')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute('SELECT nickname FROM users')
    for row in cursor:
        print('{0}'.format(row['nickname']))
    db.close()

def export_links_db():
    db = sqlite3.connect('web/data/crawler')
    def get_links(username):
        links = []
        file_exist = os.path.isfile('./links_' + username + ".txt")
        if file_exist:
            with open("links_" + username + ".txt","r") as file_links:
                for line in file_links:
                    links.append(line.strip())
        return links
    def check_existed_user(username):
        cursor = db.cursor()
        cursor.execute('SELECT COUNT(*) FROM links WHERE nickname=?', (username,))
        return cursor.fetchone()[0] != 0
    cursor = db.cursor()
    for filename in os.listdir('.'):
        if ("links_" in filename):
            user = filename.split("links_")[1].split(".txt")[0]
            if not check_existed_user(user):
                llistat = get_links(user)
                for link in llistat:
                    cursor.execute('INSERT INTO links(nickname, link) VALUES(?,?)', (user, link))
                    print(f"Adding: {user} con link: {link} a la DB.")
    db.commit()
    db.close()

def get_data_from_image():
    db = sqlite3.connect('./web/data/crawler')
    def check_existed_link_id(link_id):
        cursor = db.cursor()
        cursor.execute('SELECT COUNT(*) FROM data WHERE link_id=?', (link_id,))
        return cursor.fetchone()[0] != 0
    def get_API(photo_url):
        # Adaptación para la API REST v4 de Clarifai
        api_key = 'f607cf42c8b64ff499931bdf6a5a53a6'
        model_id = 'general-image-recognition'
        url = f'https://api.clarifai.com/v2/models/{model_id}/outputs'
        headers = {
            'Authorization': f'Key {api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'inputs': [
                {
                    'data': {
                        'image': {
                            'url': photo_url
                        }
                    }
                }
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        concepts = response.json()['outputs'][0]['data']['concepts']
        return concepts
    cursor = db.cursor()
    cursor.execute('SELECT * FROM links')
    for row in cursor:
        photo_id = str(row[0])
        if not check_existed_link_id(photo_id):
            print(f"Obteniendo info id: {photo_id} url: {row[2]}")
            concepts = get_API(row[2])
            cursor2 = db.cursor()
            for concept in concepts:
                cursor2.execute('INSERT INTO data(link_id, type, posible) VALUES(?,?,?)', (str(row[0]), concept['name'], str(concept['value'])))
                print(f"Agregando id: {row[0]} {concept['name']}:{concept['value']} a la DB.")
            db.commit()
        else:
            print(f"{photo_id} ya existe.")
    db.close()

def export_users_db():
    file_exist = os.path.isfile('./web/data/crawler')
    db = sqlite3.connect('web/data/crawler')
    if not file_exist:
        cursor = db.cursor()
        cursor.execute('CREATE TABLE users(id INTEGER PRIMARY KEY, nickname TEXT)')
        db.commit()
    cursor = db.cursor()
    for filename in os.listdir('.'):
        if ("users_" in filename):
            user = filename.split("users_")[1].split(".txt")[0]
            cursor.execute('INSERT INTO users(nickname) VALUES(?)', (user,))
            print(f"Agregando: {user} a la DB.")
    db.commit()
    db.close()

def main():
    print("Selecciona la herramienta a ejecutar:")
    print("1. Obtener imágenes de perfiles (get_images_from_profile)")
    print("2. Mostrar usuarios (show_users)")
    print("3. Exportar links a la DB (export_links_db)")
    print("4. Obtener datos de imágenes (get_data_from_image)")
    print("5. Exportar usuarios a la DB (export_users_db)")
    opcion = input("Opción [1-5]: ")
    if opcion == '1':
        get_images_from_profile()
    elif opcion == '2':
        show_users()
    elif opcion == '3':
        export_links_db()
    elif opcion == '4':
        get_data_from_image()
    elif opcion == '5':
        export_users_db()
    else:
        print("Opción no válida.")

if __name__ == "__main__":
    main()
