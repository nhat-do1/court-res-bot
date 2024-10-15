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

#open website
url = os.environ.get("URL")
path = os.environ.get("DRIVER_PATH")
driver = webdriver.Chrome(service=Service(path))
driver.get(url)

#login
email  = os.environ.get("EMAIL")
pw = os.environ.get("PW")
email_input = driver.find_element(By.ID, "Username")
pw_input = driver.find_element(By.ID, "Password")
login_button = driver.find_element(By.CSS_SELECTOR, "#loginForm > button")
email_input.send_keys(email)
pw_input.send_keys(pw)
login_button.click()


