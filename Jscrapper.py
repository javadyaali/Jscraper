import time
import csv
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException



class Jscrapper:
  
  def __init__(self, browser, wait_time=10):
        self.browser = browser
        self.wait_time = wait_time


  def search_result_count_finder(self):
    search_result_information = self.browser.find_elements_by_xpath("//*[@class='sc-bJHhxl jNtRSa']")
    search_result_count = search_result_information[0].text.split(' ')

    return int(search_result_count[0])


  def plugin_finder(self):

    # find all plugins that available in the page
    plugins = self.browser.find_elements_by_xpath("//*[@class='sc-ekulBa RptFD']")

    return plugins


  def csv_maker(self):
      with open('output.csv', 'w') as out_csv:
          writer = csv.writer(out_csv)
          writer.writerow(["Name", "Description", "Lables", "Reviews", "Installs"])



  def fetch_data(self, plugins):

      for plugin in plugins:
          
          plugin_data = plugin.text.split('\n')
          number_lables = ["installs", "install", "downloads", "download"]

          # Handel specific plugins that don't have some part of data
          if len(plugin_data) == 5:

            reviews_count = plugin_data[3].split(' ')[0]

            # Handling numbers with 'k'
            if 'k' in reviews_count:
              reviews_count = float(reviews_count.split('k')[0]) * 1000
              plugin_data[3] = reviews_count
            
            else:
              plugin_data[3] = float(reviews_count)

            if any(word in plugin_data[4] for word in number_lables):
              installs_count = plugin_data[4].split(' ')[0]

              # Handling numbers with 'k'
              if 'k' in installs_count:
                installs_count = float(installs_count.split('k')[0]) * 1000
                plugin_data[4] = installs_count

              else:  
                plugin_data[4] = float(installs_count)


          # Converting strings to integer
          elif len(plugin_data) == 4:

            if 'reviews' in plugin_data[3]:
              reviews_count = plugin_data[3].split(' ')[0]

              # Handling numbers with 'k'
              if 'k' in reviews_count:
                reviews_count = float(reviews_count.split('k')[0]) * 1000
                plugin_data[3] = reviews_count
              
              else:
                plugin_data[3] = float(reviews_count)
                plugin_data.append(0)

            elif any(word in plugin_data[3] for word in number_lables):
              installs_count = plugin_data[3].split(' ')[0]

              # Handling numbers with 'k'
              if 'k' in installs_count:
                installs_count = float(installs_count.split('k')[0]) * 1000
                plugin_data[3] = 0
                plugin_data.append(installs_count)
              else:
                plugin_data[3] = 0
                plugin_data.append(float(installs_count))

            if 'reviews' in plugin_data[2]:
              reviews_count = plugin_data[2].split(' ')[0]

              # Handling numbers with 'k'
              if 'k' in reviews_count:
                reviews_count = float(reviews_count.split('k')[0]) * 1000
                plugin_data[3] = reviews_count
                plugin_data[2] = ''
              
              else:
                plugin_data[3] = float(reviews_count)
                plugin_data[2] = ''

          if len(plugin_data) == 3:

            if 'reviews' in plugin_data[2]:
              reviews_count = plugin_data[2].split(' ')[0]

              # Handling numbers with 'k'
              if 'k' in reviews_count:
                reviews_count = float(reviews_count.split('k')[0]) * 1000
                plugin_data[2] = ''
                plugin_data.extend([reviews_count,0])
              
              else:
                plugin_data[2] = ''
                plugin_data.extend([float(reviews_count),0])

            elif any(word in plugin_data[2] for word in number_lables):
              installs_count = plugin_data[2].split(' ')[0]

              # Handling numbers with 'k'
              if 'k' in installs_count:
                installs_count = float(installs_count.split('k')[0]) * 1000
                plugin_data[2] = ''
                plugin_data.extend([0,installs_count])
              else:
                plugin_data[2] = ''
                plugin_data.extend([0,float(installs_count)])




          # write data in file
          with open('output.csv', 'a') as out_csv:
              writer = csv.writer(out_csv)
              writer.writerow(plugin_data)



  # waiting until a new plugins are loaded
  def wait_for_loading(self):
         time.sleep(self.wait_time)


  def more_result(self):
    more_result_button = self.browser.find_elements_by_xpath("//*[@class='sc-eEieub cCgAHo sc-TOsTZ bJGwYp']")

    # click on More result button on the page
    more_result_button[0].click()



class PriceMiner:

  def __init__(self, browser, wait_time=10):
    self.browser = browser
    self.wait_time = wait_time

  def csv_maker(self):
    with open('prices.csv', 'w') as out_csv:
      writer = csv.writer(out_csv)
      writer.writerow(["Name", "Active Installs", "Cloud - less than 10", "Cloud - 11 to 100", "Server - 10", "Server - 25", "Server - 50", "Server - 100", "Server - 250"])
  
  
  def plugin_finder(self):
    # find all plugins that available in the page
    plugins = self.browser.find_elements_by_xpath("//*[@class='sc-gGCbJM cLxDqP sc-dznXNo dgqdUb sc-gbzWSY kMIpUY']")

    return plugins


  def fetch_data(self, plugins):
    
    href = {}
    for plugin in plugins:

      href.update({plugin.text.split('\n')[0]:plugin.get_attribute('href')})

    return href

