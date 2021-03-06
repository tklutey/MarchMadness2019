# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv

def instantiate_driver():
    print("Instantiating driver...")
    options = Options()
    # options.add_argument('-headless')
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 5)
    return driver, wait
    

def read_csv_element(url, driver, wait):
    print("Reading CSV element...")

    csv_element_xpath = "//*[@id=\"all_adv_school_stats\"]/div[1]/div/ul/li[2]/div/ul/li[4]/button"
    dropdown_xpath = "//*[@id=\"all_adv_school_stats\"]/div[1]/div/ul/li[2]/span"
    csv_text = "//*[@id=\"csv_adv_school_stats\"]"

    driver.get(url)

    wait.until(EC.presence_of_element_located((By.XPATH, dropdown_xpath))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, csv_element_xpath))).click()
    csv_element = driver.find_element_by_xpath(csv_text).text
    return csv_element

def write_csv_string_to_file(csv_element, filename):
    print("Writing csv element to file...")
    csv_rows = csv_element.split('\n')
    
    with open(filename, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for line in csv_rows:
                writer.writerow(line.split(','))

def run_workflow():
    driver, wait = instantiate_driver()
    base_url = '/Users/kluteytk/development/projects/MarchMadness2019/data/external/bball_reference/advanced/'
    for year in range(1993, 2020):
        print(str(year) + '...')
        url = 'https://www.sports-reference.com/cbb/seasons/' + str(year) + '-advanced-school-stats.html'
        print(url)
        csv_text = read_csv_element(url, driver, wait)
        url = base_url + str(year) + 'SchoolAdvanced.csv'
        write_csv_string_to_file(csv_text, url)

if __name__ == '__main__':
    run_workflow()
