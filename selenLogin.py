#!/usr/bin/env python

username = "username"
password = "password"

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re

driver = webdriver.Chrome('./chromedriver.exe')
driver.get("https://es-es.facebook.com/")

print "Perimene file....".upper()
driver.find_element_by_name('email').send_keys(username)
driver.find_element_by_name('pass').send_keys(password)
driver.find_element_by_id("loginbutton").click()

wait = driver.implicitly_wait(5) # seconds

# f = open(username+".txt", 'w')
# malakes = re.findall(ur'data-id=\"([0-9]*)\"', driver.page_source)[::-1]
# for malakas in malakes:
  # print >> f, malakas

# f.close()
driver.quit()