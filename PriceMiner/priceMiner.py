import time
import csv
from Browser import Browser
from Jscrapper import Jscrapper
from Jscrapper import PriceMiner
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys



def main():
    # First, we are going to create a browser
    google_chrome_driver_path = '/home/hamid/Desktop/javad/research/VENV/Jscrapper/chromedriver'
    google_chrome_object = Browser(google_chrome_driver_path)
    google_chrome = google_chrome_object.create_chrome_tab()


    # Then we are going to start our browser to crawl the webpage
    url_for_scrapping = 'https://marketplace.atlassian.com/search?category=Time%20tracking&product=jira'
    google_chrome.get(url_for_scrapping)


    # After that we are using the wait().until to make us sure that the webpage loads successfully
    try:

        wait_time = 50
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


        # Creating price miner object
        price_miner = PriceMiner(google_chrome)

        # Making file for output
        price_miner.csv_maker()

        plugins = price_miner.plugin_finder()
        href = price_miner.fetch_data(plugins)



        services = {'cloud':"//*[@class='pup-pricing-block-amount']", 'server':"//*[@class='amount']"}

        for key in href:
            
            href[key] = href[key].replace('overview', 'pricing')
            google_chrome.get(href[key])
            google_chrome.implicitly_wait(8)
            active_installs = google_chrome.find_elements_by_xpath("//*[@class='plugin-active-installs-total']")
            
            if len(active_installs) != 0:
                active_installs = float(active_installs[0].text.replace(',',''))
            else:
                active_installs = 0

            print(href[key])
            service_type = href[key][href[key].find('?'):href[key].find('&')].split('=')[1]
            is_finished = False
            line = [key, active_installs]


            while not is_finished:
                
                if service_type == 'cloud':
                    print('im in cloud')
                    google_chrome.get(href[key])
                    google_chrome.implicitly_wait(8)

                    # Check is it a free app or not
                    is_free = google_chrome.find_elements_by_xpath("//*[@class='free-addon-text']")
                    if len(is_free) == 0:
                        cloud_prices = google_chrome.find_elements_by_xpath(services[service_type])

                        for price in cloud_prices:
                            price = price.text.replace(',','')
                            price = float(price.split('$')[1])
                            line.append(price)
                        
                        # Check server service
                        href[key] = href[key].replace('cloud', 'server')
                        google_chrome.get(href[key])
                        google_chrome.implicitly_wait(8)

                        # Check server prices
                        server_prices = google_chrome.find_elements_by_xpath(services['server'])
                        if len(server_prices) != 0:
                            i = 1
                            for price in server_prices:
                                if i <=5 :
                                    print(price.text,i)
                                    price = price.text.replace(',','')
                                    price = float(price.split('$')[1])
                                    line.append(price)
                                    i += 1
                            

                if service_type == 'server':
                    print('im in server')
                    is_free = google_chrome.find_elements_by_xpath("//*[@class='free-addon-text']")
                    if len(is_free) == 0:
                        server_prices = google_chrome.find_elements_by_xpath(services[service_type])
                        for price in server_prices:
                            price = price.text.replace(',','')
                            price = float(price.split('$')[1])
                            line.append(price)   


                # write data in file
                with open('price.csv', 'a') as out_csv:
                    writer = csv.writer(out_csv)
                    writer.writerow(line)

                is_finished = True 
        google_chrome.quit()





        
    finally:
        print('Done!!')

if __name__ == '__main__':
    main()