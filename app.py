# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

# testing
import time as T

# Environment
import os
from dotenv import load_dotenv
load_dotenv()

# Date & Time
from datetime import date, datetime, timedelta, time

# open website
url = os.environ.get("URL")
driver_path = os.environ.get("DRIVER_PATH")
profile_path = os.environ.get("PROFILE_PATH")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=" + profile_path)
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
driver.get(url)

# login if required
if (len(driver.find_elements(By.LINK_TEXT, "Create Account")) > 0):
    email  = os.environ.get("EMAIL")
    pw = os.environ.get("PW")
    email_input = driver.find_element(By.ID, "UserNameOrEmail")
    pw_input = driver.find_element(By.ID, "Password")
    login_button = driver.find_element(By.CSS_SELECTOR, "#loginForm > button")
    email_input.send_keys(email)
    pw_input.send_keys(pw)
    login_button.click()
    driver.get(url) # website does not redirect correctly after login

# confirm correct page is loaded
title_locator = (By.CSS_SELECTOR, "span.fn-inner-text")
title_text = "Pickleball Reservations"
page_loaded = WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element(title_locator, title_text))

if (page_loaded):
    # reset to today
    counter = 0
    reset_button = driver.find_element(By.XPATH, '//*[@id="ConsolidatedScheduler"]/div/span[1]/button[1]')
    reset_button.click()
    # can only book up to next 7 days
    # while (counter < 7): 
    try:
        # check for open slots
        open_slots = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.LINK_TEXT, "Reserve")))
    except TimeoutException:
        # go to next day
        next_button = driver.find_element(By.XPATH, '//*[@id="ConsolidatedScheduler"]/div/span[1]/button[3]')
        next_button.click()
        counter += 1
    else:
        # find bookable slots
        # start time must be > 30 min from current time (if today)
        for slot in open_slots:
            data_str = slot.get_attribute("data-href")
            start_idx = 51
            end_idx = data_str.find("&courtType")
            datetime_str = data_str[start_idx:end_idx]
            now = datetime.now()
            print(datetime_str)
            print(now.time())
            print(now.date())
        



T.sleep(7)