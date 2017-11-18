from bs4 import BeautifulSoup
import selenium.webdriver as webdriver

url = 'http://instagram.com/umnpics/'
driver = webdriver.Chrome()
driver.set_window_size(300, 300) # set window size
driver.get(url)

soup = BeautifulSoup(driver.page_source, "html.parser")

for x in soup.findAll('img'):
    print x

driver.close()