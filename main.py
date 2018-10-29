import time
import csv
from Browser import Browser
from Jscrapper import Jscrapper
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException




def main():

	# First, we are going to create a browser
	google_chrome_driver_path = '/home/hamid/Desktop/javad/research/VENV/JTest/chromedriver'
	google_chrome_object = Browser(google_chrome_driver_path)
	google_chrome = google_chrome_object.create_chrome_tab()


	# Then we are going to start our browser to crawl the webpage
	url_for_scrapping = 'https://marketplace.atlassian.com/search?category=Time%20tracking&product=jira'
	google_chrome.get(url_for_scrapping)


	# After that we are using the wait().until to make us sure that the webpage loads successfully
	try:

		wait_time = 5000
		element = WebDriverWait(google_chrome, wait_time).until(
        	EC.presence_of_element_located((By.XPATH, "//h3[@class='sc-ghsgMZ giyMKw sc-kkbgRg hkWXqv']")))


		javad_spider = Jscrapper(google_chrome)

		# Calculate the number of click on "More Results" button
		number_per_page = 24
		search_result_count = javad_spider.search_result_count_finder()
		number_for_click_on_button = (search_result_count) // (number_per_page)

		for num in range(number_for_click_on_button):
			
			# Click on button for seeing all plugins
			javad_spider.more_result()

			# wait for loading the page successfully
			javad_spider.wait_for_loading()

		# Create CSV file
		javad_spider.csv_maker()

		# Start collecting all the plugins information
		plugins = javad_spider.plugin_finder()
		javad_spider.fetch_data(plugins)

	finally:
		google_chrome.quit()




# Run the scrapper
if __name__ == '__main__':
	main()