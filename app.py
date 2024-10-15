from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
from dotenv import load_dotenv
load_dotenv()

url = os.environ.get("URL")
path = os.environ.get("DRIVER_PATH")
browser = webdriver.Chrome(service=Service(path))
browser.get(url)