# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# testing
import time

# Environment
import os
from dotenv import load_dotenv
load_dotenv()

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
    driver.get(url) # website does not redirect correctly after log in

time.sleep(10)