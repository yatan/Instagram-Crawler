from bs4 import BeautifulSoup
import selenium.webdriver as webdriver

url = 'http://instagram.com/umnpics/'
driver = webdriver.Chrome()
driver.set_window_size(300, 300) # set window size
driver.get(url)


soup = BeautifulSoup(driver.page_source, "html.parser")

for foto in soup.findAll('img'):
    print foto.get('alt', '')
    print foto.get('src', '')


driver.close()