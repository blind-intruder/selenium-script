from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def open_chrome_with_proxy(proxy):
    chrome_options = Options()
    chrome_options.add_argument('--disable-application-cache')
    #chrome_options.add_argument(f'--proxy-server={proxy}') #uncomment this line, if using proxy

    service = Service(executable_path='/Users/mbp/Desktop/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver

def __scroll_down_page(driver, speed=4):
    current_scroll_position, new_height= 0, 0
    while current_scroll_position <= new_height:
        current_scroll_position += speed
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        new_height = driver.execute_script("return document.body.scrollHeight")

def __scroll_up_page(driver, speed=4):
    current_scroll_position, new_height= driver.execute_script("return document.body.scrollHeight"), 0
    while current_scroll_position >= new_height:
        current_scroll_position -= speed
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))


def main():
    proxies = ["1"]; #add proxies here

    for proxy in proxies:
        try:
            driver = open_chrome_with_proxy(proxy)
            driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled":True})
            driver.get("https://www.google.com/")
            time.sleep(5)  

            search_box = driver.find_element("name", "q")
            search_box.send_keys("myipv4address.com")
            search_box.send_keys(Keys.RETURN)
            time.sleep(5) 

            link = driver.find_element(By.XPATH,"//a[@href='https://myipv4address.com/']")
            link.click()

            time.sleep(5)
            __scroll_down_page(driver)
            time.sleep(2)
            __scroll_up_page(driver)
            time.sleep(5)
            driver.delete_all_cookies()

            driver.quit()
            break

        except Exception as e:
            print(f"Error using proxy {proxy}: {e}")

if __name__ == "__main__":
    main()
