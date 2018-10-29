from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException


# making a browser
class Browser():

	def __init__(self, chrome_driver_path):
		
		self.chrome_driver_path = chrome_driver_path

	def create_chrome_tab(self):
		option = webdriver.ChromeOptions()
		chrome = webdriver.Chrome(executable_path=self.chrome_driver_path, chrome_options=option)

		return chrome