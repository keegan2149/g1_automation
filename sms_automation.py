from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 

import time

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
#options.binary_location = "/usr/bin/chromium"
driver = webdriver.Chrome(executable_path='./chromedriver',chrome_options=options)
driver.get('https://www.politicalcomms.com/users/sign_in')
driver.find_element_by_id('user_email').send_keys('keegan2149@gmail.com')
driver.find_element_by_id ('user_password').send_keys('G1consulting')
driver.find_element_by_name('commit').submit()
driver.find_element_by_name('accepted').click()
driver.find_element_by_name('commit').submit()
driver.find_element_by_link_text("/sms/425/send_message").click()


for x in range(3000):
   driver.find_element_by_name('commit').submit()
   WebDriverWait(driver, 3)

driver.quit()

driver.find_element_by_name('commit').click()


