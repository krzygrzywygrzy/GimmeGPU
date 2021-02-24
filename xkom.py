from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

# setup
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# path https://www.x-kom.pl/szukaj?q=rtx3060
driver.get("https://www.x-kom.pl/g-5/c/345-karty-graficzne.html")
driver.maximize_window()

for x in range(2):
    # find the offer card
    # path = str('//*[@id="listing-container"]/div[' + str(x) + ']/div')
    container = driver.find_element_by_xpath("//*[@id='listing-container']/div['" + str(x) + "']/div")
    container.click()

    # find button that ads item to basket
    try:
        #check if page is loaded
        price_div = WebDriverWait(driver, 15)\
            .until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/div[1]/div/div')))
        price = int(price_div.text.split(",")[0].replace(" ", ""))

        #check if product is of grahic card and if the price is right
        is_GPU = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[1]/div[2]/div[1]/div/ul/li[3]/div/a').text
        if (price >= 100) and (price < 10000) and (is_GPU == "Karty graficzne"):
            # choose amount
            # TODO: try to repair choosing amount
            amount_picker = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div/div')
            amount_picker.click()
            select_amount = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div/div/span[1]/div[2]')
            # print(select_amount.get_attribute("aria-activedescendant"))
            driver.execute_script("arguments[0].setAttribute('aria-activedescendant', arguments[1])", select_amount, "react-select-6--option-1")

            # add to basket
            basket_button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/button').click()

    except TimeoutException:
        print("Element not found")
    except ValueError:
        print("Cannot convert price to integer")
    except NoSuchElementException:
        print("Element doesn't exist")
    driver.get("https://www.x-kom.pl/g-5/c/345-karty-graficzne.html")

# go to cart
driver.get("https://www.x-kom.pl/koszyk")
try:
    is_empty = WebDriverWait(driver, 15)\
        .until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/span/h2')))
    if is_empty.text != "Twój koszyk jest pusty":
        print("works")

except TimeoutException:
    print("Element doesn't exist")






