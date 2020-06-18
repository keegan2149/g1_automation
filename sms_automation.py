from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import datetime



def print_time(message = ""):
  now = datetime.datetime.now()
  print("\n")
  if message:
    print(message)
  else:
    print ("Current date and time : ")
  print (now.strftime("%Y-%m-%d %H:%M:%S"))
  print ("\n")

#reads username and password and stores in a dictionary credentials[email:"your@wmail.com",password:"password"

def get_creds(): 
  cred_file = open("./credentials.json", "r")
  credentials = cred_file.read()
  credentials = json.loads(credentials)
  cred_file.close()
  return credentials   


def open_driver(options=['--ignore-certificate-errors',"--test-type"],driver_path='./chromedriver'):
  print_time()
  driver_options = webdriver.ChromeOptions()
  for x in options:
    driver_options.add_argument(x)

  driver = webdriver.Chrome(executable_path=driver_path,chrome_options=driver_options)
  return driver 

def clean_up(driver):
  try:
    print_time()
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
      if driver.find_element_by_class_name('notice'):
        print("all jobs finished")
        return False
    except:
      return True
  except Exception as e:
    print("unknown error")
    return False


      

def send_sms(driver,message_count=30000, fail_limit = 100):

  #Open SMS Project
  #if there are multiple projects then one can be found by name or element id


  #Send message_count messages
  fail_count = 0
  click_count = 0
  if project_available(driver):
    for x in range(message_count):
      #driver.find_element_by_xpath("//input[@name='commit']").submit()
      try:
        element_to_click = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='commit']")))
        element_to_click.submit()
        fail_count = 0
        click_count +=1
      except:
        try:
          print("miss.. retrying")
          element_to_click = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='commit']")))
          element_to_click.submit()
          click_count +=1
        except:
          #try to detect if we are at the job screen
          #currently not working
          #try to detect if we are at the job screen
          #currently not working
          print("retry failed..")
          if project_available(driver):
            print("SMS Project found Resuming")
          else:
            print("No Project Found")
            clean_up(driver)

          fail_count += 1
          print("oops.. missed one. Unknown error.")
          if fail_count >= fail_limit:
            print(fail_limit + " consecutive click failures exiting..")
            clean_up(driver)
  else:
  	clean_up(driver)

  
#close window

credentials = get_creds()
driver = open_driver()
send_sms(login(driver,credentials))

