# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

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
            # print(datetime_str)  10/24/2024%209:30%20PM&end=10/24/2024%2010:00%20PM
            # print(now.time())    11:15:44.657467
            # print(now.date())    2024-10-24
            today_str = str(now.date().strftime("%m/%d/%Y"))
            datetime_parts = datetime_str.split("%20")
            # print(datetime_parts)  ['10/24/2024', '9:30', 'PM&end=10/24/2024', '10:00', 'PM']
            slot_date = datetime_parts[0]
            slot_starttime_str = datetime_parts[1] + " " + datetime_parts[2][:2]
            slot_starttime_obj = datetime.strptime(slot_starttime_str, '%I:%M %p').time()
            dt = datetime.combine(now, slot_starttime_obj)
            # not allowed to book time slots w/ start time w/i 30 min of current time 
            if (today_str == slot_date and dt - now <= timedelta(minutes=30)):
                continue
            else:
                # book slot
                # later conditions: start time >= 6:30PM && end time >= start time + 1 HR
                slot_button = driver.find_element(By.XPATH, f'//a[@data-href="{data_str}"]')
                try:
                    slot_button.click()
                except StaleElementReferenceException:
                    slot_button = driver.find_element(By.XPATH, f'//a[@data-href="{data_str}"]')
                    slot_button.click()
                break



        



T.sleep(7)