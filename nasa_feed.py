import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#open browser
driver = selenium.webdriver.Firefox()

#load url
driver.get("https://www.nasa.gov/multimedia/imagegallery/iotd.html")

#wait until the button loads to load more images
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "trending"))
    )

    #once the button loads, click it 16 times
    i =0
    while i <= 15:
        driver.find_element_by_xpath('//*[@id="trending"]').click()
        i += 1
        time.sleep(1)
finally:
    print(i)

