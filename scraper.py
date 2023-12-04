from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import csv

def generate_leads():
    # collect user info to scrape information:
    user_username = input('What is your Linkedin Email:')
    user_password = input('what is your Linkedin Password: ')
    leadListLink = input('what is your LinkedIn Lead list URL: ')
    # start webscraper
    driver = webdriver.Chrome('/Users/jacobmolyneux/Desktop/chromedriver')
    print('starting scrape.....')
    driver.get(leadListLink)
    print('waiting for page to load')
    time.sleep(6)
        # Store iframe web element
    iframe = driver.find_element(By.TAG_NAME, "iframe")

        # switch to selected iframe
    driver.switch_to.frame(iframe)

    print('wait is over')

    print('finding username and password logins')

    username_input = driver.find_element(By.ID, 'username')
    password_input = driver.find_element(By.ID, 'password')
    print('found logins')
    print('sending login info')
    username_input.send_keys(user_username)
    time.sleep(1)
    password_input.send_keys(user_password)
    time.sleep(0.3)
    print('login info sent')
    login_button = driver.find_element(By.TAG_NAME, 'button')
    login_button.click()

    print('-----------------')
    print('WOOP! Login successful!')
    print('waiting for page to load')
    time.sleep(4)
    leads = []
    driver.switch_to.default_content()
    # needed if you have multiple linkedin accounts
    
    # select_contract = driver.find_elements(By.CLASS_NAME, 'action-select-contract')
    # select_contract[1].click()
   

    time.sleep(10)

    # for i in driver.find_elements(By.TAG_NAME, 'tr'):
    def scrape_leads():
        table = driver.find_element(By.TAG_NAME, 'tbody')
        table_rows = table.find_elements(By.TAG_NAME, 'tr')
        
        print(len(table_rows))
        for row in table_rows:
            name = row.find_element(By.CSS_SELECTOR, '[data-anonymize=person-name]').text
            #try to get the company
            try:
                company = row.find_element(By.CSS_SELECTOR,'[data-anonymize=company-name]').text
            except NoSuchElementException:
                company = 'N/A'
                pass
            #try to get the job title
            try:
                title = row.find_element(By.CSS_SELECTOR,'[data-anonymize=job-title]' ).text
            except NoSuchElementException:
                title = 'N/A'
                pass
            # try to get the location
            try:
                location = row.find_element(By.CSS_SELECTOR, '[data-anonymize=location]').text
            except NoSuchElementException:
                title = 'N/A'
                pass
            # getting the linkedin profile ** tricky and a pain in the ass because it changes **
            try:
                figure = row.find_element(By.TAG_NAME, 'figure')
                linkedIn = figure.find_element(By.TAG_NAME, 'a').get_attribute('href')
            except NoSuchElementException:
                linkedIn = 'N/A'
                pass
                
            leads.append({"Company": company, "Name": name, "Title": title, "Phone Number": '', "Name_Drop": "","Location": location, "LinkedIn": linkedIn})

        
    next_button = driver.find_element_by_css_selector('[aria-label=Next]')
    while next_button.is_enabled():
        print('scraping page')
        scrape_leads()
        next_button = driver.find_element_by_css_selector('[aria-label=Next]')
        time.sleep(4)
        next_button.click()
        time.sleep(3)

    # runs last time to scrape the last page
    scrape_leads()

    # print(leads)
    # create a csv file and save it to computer
    field_names = ['Company', 'Name', 'Title', "Phone Number","Name_Drop", "Location", "LinkedIn"]
    with open('/Users/jacobmolyneux/Desktop/NewLeads.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(leads)
    return leads

generate_leads()
