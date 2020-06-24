from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import datetime
import os



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
  print
  log_entry("opening browser instance")
  driver_options = webdriver.ChromeOptions()
  for x in options:
    driver_options.add_argument(x)

  driver = webdriver.Chrome(executable_path=driver_path,chrome_options=driver_options)
  return driver 

def clean_up(driver):
  os.system('echo "\a"')
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
    except:
      try:
        driver.find_element_by_xpath("//a[text()='Return']").click()
        log_entry("all jobs finished")
        return False
      except:
        log_entry("unknown screen")
        return True
      try:
        driver.find_element_by_xpath("//p[contains(text(), 'All messages for you sent')")
        log_entry("all jobs finished")
        return False
      except:
        log_entry("unknown screen")
        return True


      return True
  except Exception as e:
    log_entry("unknown error")
    return False
  
  return True


      

def send_sms(driver,message_count=30000, fail_limit = 100):
  fail_count = 0
  click_count = 0

  def increment_fail_count(fail_count,fail_limit = 15):
    log_entry("fail count = " + str(fail_count))
    fail_count += 1
    log_entry("oops.. missed one. Unknown error.")
    if fail_count >= fail_limit:
      print(str(fail_limit) + " consecutive click fails exiting. ")
      return False
    else:
      return fail_count

  #Open SMS Project
  #if there are multiple projects then one can be found by name or element id


  #Send message_count messages
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
          log_entry("retry failed.. are we at the project screen?")
          if project_available(driver):
            fail_count += 1 
            log_entry("yes!")
            log_entry("SMS Project found Resuming")
          else:
            fail_count = increment_fail_count(fail_count)
            if not fail_count:
              clean_up(driver)
  else:
    log_entry("No Jobs Found")
    clean_up(driver)

  
#close window

credentials = get_creds()
driver = open_driver()
send_sms(login(driver,credentials))

