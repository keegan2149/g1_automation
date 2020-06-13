from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
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


def send_sms(credentials,driver,start_url='https://www.politicalcomms.com/users/sign_in',message_count=3000):
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
    driver.find_element_by_link_text("/sms/425/send_message").click()  
  except Exception as e:
    print("no jobs found")
    driver.stop_client()
    driver.quit()


  #Send message_count messages

  for x in range(message_count):
    driver.find_element_by_name('commit').submit()
    WebDriverWait(driver, 3)

  #close window
  driver.quit()


credentials = get_creds()
driver = open_driver()
send_sms(credentials,driver)

#cool overloaded function call

#send_sms(get_creds(),open_driver())