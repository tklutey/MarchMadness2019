# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver

driver = webdriver.Chrome()

xpath = "//*[@id=\"all_ratings\"]/div[1]/div/ul/li[1]/div/ul/li[4]/button"
url = "https://www.sports-reference.com/cbb/seasons/2018-ratings.html"
page = driver.get(url)
driver.find_element_by_xpath(xpath).click()
