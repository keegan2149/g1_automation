from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import json
import time

#reads username and password and stores in a dictionary credentials[email:"your@wmail.com",password:"password"

def get_creds(): 
  cred_file = open("./credentials.json", "r")
  credentials = cred_file.read()
  credentials = json.loads(credentials)
  cred_file.close()
  return credentials   


def open_driver(options=['--ignore-certificate-errors',"--test-type"],driver_path='./chromedriver'):
  driver_options = webdriver.ChromeOptions()
  for x in options:
  	driver_options.add_argument(x)

  driver = webdriver.Chrome(executable_path=driver_path,chrome_options=driver_options)
  return driver 


def send_sms(credentials,driver,start_url='https://www.politicalcomms.com/users/sign_in',message_count=30000):
  driver.get(start_url)
  #login
  driver.find_element_by_id('user_email').send_keys(credentials['email'])
  driver.find_element_by_id ('user_password').send_keys(credentials['password'])
  driver.find_element_by_name('commit').submit()

  #Accept TOS
  driver.find_element_by_name('accepted').click()
  driver.find_element_by_name('commit').submit()

  #Open SMS Project
  #if there are multiple projects then one can be found by name or element id
  try:
    driver.find_element_by_xpath("//a[text()='Send']").click()
  except Exception as e:
    print("no jobs found")
    driver.stop_client()
    driver.quit()


  #Send message_count messages

  try:
    for x in range(message_count):
      #driver.find_element_by_xpath("//input[@name='commit']").submit()
      element_to_click = WebDriverWait(driver, 13).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='commit']")))
      element_to_click.submit()

  except Exception as e:
    print("couldn't find send button")
    for x in range(message_count):
      #driver.find_element_by_xpath("//input[@name='commit']").submit()
      element_to_click = WebDriverWait(driver, 13).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='commit']")))
      element_to_click.submit()

    if driver:
      driver.quit()
    else:
      close() 	
  
  #close window
  driver.quit()


credentials = get_creds()
driver = open_driver()
send_sms(credentials,driver)

#cool overloaded function call

#send_sms(get_creds(),open_driver())