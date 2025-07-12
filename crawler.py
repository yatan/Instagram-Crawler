# Compatible con Python 3

import sys, subprocess, time, os
from threading import Thread, Lock
from bs4 import BeautifulSoup
# --- INICIO SELENIUM ---
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# --- FIN SELENIUM ---
import urllib.request

max_crawl = 5
actual_crawl = 0
actual_crawl_lock = Lock()


# GET user value from argument or using 'default'
active_user = "thewesborland"
if len(sys.argv) == 2:
    active_user = sys.argv[1]


class Crawler(Thread):
    def __init__(self, active_user):
        Thread.__init__(self)
        self.active_user = active_user
        self.users = []
        self.scanned_users = []

    # Thread worker for active_user
    def run(self):
        print("Analizyng user: " + self.active_user)
        try:
            # --- INICIO SELENIUM ---
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--window-size=1920,1080')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            url = f'https://www.instagram.com/{self.active_user}'
            driver.get(url)
            time.sleep(5)  # Espera a que cargue la página
            html = driver.page_source
            driver.quit()
            # --- FIN SELENIUM ---
            soup = BeautifulSoup(html, "html.parser")
            self.parse_users(soup)
        except Exception as e:
            print(f"Error fetching user {self.active_user}: {e}")

    def check_exist(self, username):
        if not os.path.exists("analized_users.txt"):
            return False
        with open("analized_users.txt", "r") as file_users_analized:
            loglist = file_users_analized.readlines()
        found = False
        for line in loglist:
            if str(username) in line:
                found = True
        return found


    def parse_users(self, soup):
        global actual_crawl
        global max_crawl
        global actual_crawl_lock

        def is_valid_username(username):
            # Solo letras, números, puntos y guiones bajos, y longitud típica de Instagram
            import re
            return re.fullmatch(r"[A-Za-z0-9._]{1,30}", username) is not None

        with open("users_" + self.active_user + ".txt", "w", encoding="utf-8") as file_users:
            for a in soup.find_all('a'):
                href = a.get('href', '')
                # Buscar enlaces de perfil tipo /username/
                if href.startswith('/') and href.count('/') == 2 and not href.startswith('/explore') and not href.startswith('/p/'):
                    username = href.strip('/').split('/')[0]
                    if is_valid_username(username) and username != self.active_user and username not in self.users:
                        self.users.append(username)
                        file_users.write(username + "\n")

        with open("analized_users.txt", "a", encoding="utf-8") as file_users_analized:
            file_users_analized.write(self.active_user + "\n")

        with actual_crawl_lock:
            actual_crawl -= 1

        for usuari in self.users:
            while True:
                with actual_crawl_lock:
                    if actual_crawl < max_crawl:
                        actual_crawl += 1
                        break
                time.sleep(1)  # Espera activa hasta que haya slot libre
            try:
                print("worker " + usuari)
            except Exception:
                print("worker (usuario con caracteres especiales)")
            if not self.check_exist(usuari):
                self.child = subprocess.Popen([sys.executable, os.path.abspath(__file__), usuari])

    def join(self):
        Thread.join(self)
        return self.users

# Llista threads actius
if __name__ == "__main__":
    # Instalar dependencias si es necesario
    try:
        import selenium
        import webdriver_manager
    except ImportError:
        print("Instalando dependencias necesarias para Selenium...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium", "webdriver-manager"])
    e = Crawler(active_user)
    e.start()
    print(e.join())

