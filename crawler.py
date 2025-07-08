# Compatible con Python 3
import sys, subprocess, time, os
from threading import Thread, Lock
from bs4 import BeautifulSoup
import urllib.request

max_crawl = 5
actual_crawl = 0
actual_crawl_lock = Lock()


# GET user value from argument or using 'default'
active_user = "twittersoz"
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
            response = urllib.request.urlopen('https://www.instagram.com/' + self.active_user)
            html = response.read()
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

        with open("users_" + self.active_user + ".txt", "w") as file_users:
            for coses in soup.find_all('a'):
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

        with open("analized_users.txt", "a") as file_users_analized:
            file_users_analized.write(self.active_user + "\n")

        with actual_crawl_lock:
            actual_crawl -= 1

        for usuari in self.users:
            with actual_crawl_lock:
                if actual_crawl > max_crawl:
                    need_sleep = True
                else:
                    need_sleep = False
            if need_sleep:
                time.sleep(5)
            else:
                print("worker " + usuari)
                if not self.check_exist(usuari):
                    with actual_crawl_lock:
                        actual_crawl += 1
                    self.child = subprocess.Popen([sys.executable, os.path.abspath(__file__), usuari])

    def join(self):
        Thread.join(self)
        return self.users

# Llista threads actius
if __name__ == "__main__":
    e = Crawler(active_user)
    e.start()
    print(e.join())

