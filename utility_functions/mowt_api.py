import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime

def get_permit_details(permit_num, date_of_birth: datetime):
    date_of_birth = date_of_birth.strftime("%Y-%m-%d")
    driver = webdriver.Chrome(executable_path="chromedriver.exe",)
    #Go to website
    driver.get("https://apps.mowt.gov.tt/dpv")
    time.sleep(3)
    #Remove that pesky readonly attribute from the DOB field
    driver.execute_script('document.evaluate("//*[@id=\'mainMowtApps\']/div/section/div/div/div/div/form/div[3]/input", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.removeAttribute("readonly")')
    #Fill out date and license number fields
    date_of_birth_input = driver.find_element_by_xpath('//*[@id="mainMowtApps"]/div/section/div/div/div/div/form/div[3]/input').send_keys(date_of_birth)
    time.sleep(3)
    permit_num_input = driver.find_element_by_xpath('//*[@id="mainMowtApps"]/div/section/div/div/div/div/form/div[2]/input').send_keys(permit_num)
    time.sleep(3)


   #Click the search button
    driver.find_element_by_xpath('//*[@id="mainMowtApps"]/div/section/div/div/div/div/form/div[4]/button').click()
    # too bad captcha is a thing
    driver.close()



if __name__ == "__main__":
    dob = datetime(year=1993,month=2,day=19)
    print(get_permit_details("1021376",dob))