from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import datetime



def log_entry(message = ""):
  now = datetime.datetime.now()
  print (now.strftime("%Y-%m-%d %H:%M:%S") + ": " + message)

#reads username and password and stores in a dictionary credentials[email:"your@wmail.com",password:"password"

def get_creds(): 
  cred_file = open("./credentials.json", "r")
  credentials = cred_file.read()
  credentials = json.loads(credentials)
  cred_file.close()
  return credentials   


def open_driver(options=['--ignore-certificate-errors',"--test-type"],driver_path='./chromedriver'):
  log_entry("opening browser instance")
  driver_options = webdriver.ChromeOptions()
  for x in options:
    driver_options.add_argument(x)

  driver = webdriver.Chrome(executable_path=driver_path,chrome_options=driver_options)
  return driver 

def clean_up(driver):
  try:
    log_entry("quitting.")
    driver.quit()
    quit()
  except Exception as e:
    quit()

def login(driver,credentials,start_url='https://www.politicalcomms.com/users/sign_in',):
  driver.get(start_url)
  #login
  driver.find_element_by_id('user_email').send_keys(credentials['email'])
  driver.find_element_by_id ('user_password').send_keys(credentials['password'])
  driver.find_element_by_name('commit').submit()

  #Accept TOS
  driver.find_element_by_name('accepted').click()
  driver.find_element_by_name('commit').submit()

  return driver

def project_available(driver):

  #Open SMS Project
  #if there are multiple projects then one can be found by name or element id
  #if there are none or if we are done return false
  try:
    driver.find_element_by_xpath("//a[text()='Send']").click()
    try:
      element_to_click = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='commit']")))
      if element_to_click:
      	return True
      elif driver.find_element_by_class_name('notice'):
          log_entry("all jobs finished")
          return False
    except:
      return True
  except Exception as e:
    log_entry("unknown error")
    return False
  
  return True


      

def send_sms(driver,message_count=30000, fail_limit = 100):

  #Open SMS Project
  #if there are multiple projects then one can be found by name or element id


  #Send message_count messages
  fail_count = 0
  click_count = 0
  if project_available(driver):
    log_entry("working..")
    for x in range(message_count):
      #driver.find_element_by_xpath("//input[@name='commit']").submit()
      try:

        element_to_click = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='commit']")))
        element_to_click.submit()
        if fail_count > 0:
          log_entry("resuming.. ")
        fail_count = 0
        click_count +=1
      except:
        try:
          log_entry("miss.. retrying")
          element_to_click = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='commit']")))
          element_to_click.submit()
          if fail_count > 0:
            log_entry("resuming.. ")
          fail_count = 0
          click_count +=1
        except:
          #try to detect if we are at the job screen
          #currently not working
          #try to detect if we are at the job screen
          #currently not working
          log_entry("retry failed..")
          if project_available(driver):
            log_entry("SMS Project found Resuming")
          else:
            log_entry("No Project Found")

          fail_count += 1
          log_entry("oops.. missed one. Unknown error.")
          if fail_count >= fail_limit:
            print(fail_limit + " consecutive click failures exiting..")
            clean_up(driver)
  else:
  	log_entry("No Jobs Found")
  	clean_up(driver)

  
#close window

credentials = get_creds()
driver = open_driver()
send_sms(login(driver,credentials))

