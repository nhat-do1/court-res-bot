# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

# Environment
import os
from dotenv import load_dotenv
load_dotenv()

# Date & Time
from datetime import datetime, time

# testing
import time as T

# open website
url = os.environ.get('URL')
driver_path = os.environ.get('DRIVER_PATH')
profile_path = os.environ.get('PROFILE_PATH')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('user-data-dir=' + profile_path)
# chrome_options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
driver.get(url)

# login if required
if (len(driver.find_elements(By.LINK_TEXT, 'Create Account')) > 0):
    email  = os.environ.get('EMAIL')
    pw = os.environ.get('PW')
    email_input = driver.find_element(By.ID, 'UserNameOrEmail')
    pw_input = driver.find_element(By.ID, 'Password')
    login_button = driver.find_element(By.CSS_SELECTOR, '#loginForm > button')
    email_input.send_keys(email)
    pw_input.send_keys(pw)
    login_button.click()
    driver.get(url) # website does not redirect correctly after login

# confirm correct page is loaded
title_locator = (By.CSS_SELECTOR, 'span.fn-inner-text')
title_text = 'Pickleball Reservations'
page_loaded = WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element(title_locator, title_text))

if (page_loaded):
    # reset to today
    counter = 0
    reset_button = driver.find_element(By.XPATH, '//*[@id="ConsolidatedScheduler"]/div/span[1]/button[1]')
    reset_button.click()
    # skip today & book up to next 7 days
    while (counter < 7): 
        next_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ConsolidatedScheduler"]/div/span[1]/button[3]')))
        next_button.click()
        counter += 1
        try:
            # check for open slots
            open_slots = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.LINK_TEXT, 'Reserve')))
        except TimeoutException:
            # go to next day
            next_button.click()
            counter += 1
        else:
            for slot in open_slots:
                # get data attr value
                data_str = slot.get_attribute('data-href')
                # parse for date & times
                start_idx = 51
                end_idx = data_str.find('&courtType')
                datetime_str = data_str[start_idx:end_idx]
                datetime_parts = datetime_str.split('%20')
                slot_date_str = datetime_parts[0]
                # parse for start time
                slot_starttime_str = datetime_parts[1] + ' ' + datetime_parts[2][:2]
                slot_starttime_obj = datetime.strptime(slot_starttime_str, '%I:%M %p').time()
                # book slots w/ preferred start time >= 6:30PM and < 9:00PM
                if (slot_starttime_obj >= time(18, 30) and slot_starttime_obj <= time(21,0)):
                    # open reservation modal for time slot: 
                    slot_button = driver.find_element(By.XPATH, f'//a[@data-href="{data_str}"]')
                    try:
                        slot_button.click()
                    # bypass stale element after auto-scroll
                    except StaleElementReferenceException:
                        slot_button = driver.find_element(By.XPATH, f'//a[@data-href="{data_str}"]')
                        slot_button.click()
                    # wait for final total due to populate to confirm duration
                    final_total = WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'label.total-due-amount'), '$13.00'))
                    # check discloure agreement box
                    checkbox = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="createReservation-Form-container"]/div[3]/div[2]/div/div/span')))
                    checkbox.click()
                    # attempt to save booking
                    save_button = driver.find_element(By.XPATH, '//*[@id="createReservation-Form"]/div[3]/div/button[2]')
                    save_button.click()
                    try:  # default 1 hr duration cannot be accomodated
                        msg_locator = (By.ID, 'span.fn-inner-text')
                        msg_text = 'Sorry, no available courts for the time requested.'
                        msg_loaded = WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element(msg_locator, msg_text))
                        ok_button = driver.find_element(By.CSS_SELECTOR, 'button.swal2-confirm swal2-styled')
                        ok_button.click()
                        close_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="createReservation-Form"]/div[1]/div[2]/button[1]')))
                        close_button.click()
                    except TimeoutException: # booking successful
                        print(f'Booking successful for {slot_date_str} at {slot_starttime_str}')
                        # one reservation per day
                        break

T.sleep(20)