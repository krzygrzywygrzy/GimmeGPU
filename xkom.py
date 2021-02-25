from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time

# setup
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# path https://www.x-kom.pl/szukaj?q=rtx%203060&f%5Bgroups%5D%5B5%5D=1&sort_by=accuracy_desc&f%5Bcategories%5D%5B345%5D=1
#path to 12GB VRAM https://www.x-kom.pl/szukaj?q=rtx%203060%2012gb&f%5Bgroups%5D%5B5%5D=1&sort_by=accuracy_desc&f%5Bcategories%5D%5B345%5D=1

driver.get("https://www.x-kom.pl/szukaj?q=rtx%203060%2012gb&f%5Bgroups%5D%5B5%5D=1&sort_by=accuracy_desc&f%5Bcategories%5D%5B345%5D=1")
driver.maximize_window()

def add_to_cart():
    cards_amount = 1  # choose cards amount you want to buy
    index = 1
    in_basket = 0

    item_count = len(driver.find_elements_by_xpath('//*[@id="listing-container"]/div[1]/div/div[2]/div[3]/div/div/div/div/span'))

    while in_basket != cards_amount:
        if index <=item_count:
            # find the offer card
            container = driver.find_element_by_xpath("//*[@id='listing-container']/div['" + str(index+1) + "']/div")
            container.click()
            index += 1
            # find button that ads item to basket
            try:
                #check if page is loaded
                price_div = WebDriverWait(driver, 3)\
                    .until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/div[1]/div/div')))
                price = int(price_div.text.split(",")[0].replace(" ", ""))

                # check if product is of grahic card and if the price is right
                is_GPU = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[1]/div[2]/div[1]/div/ul/li[3]/div/a').text
                if (price >= 1500) and (price < 4000) and (is_GPU == "Karty graficzne"):
                    # choose amount
                    # TODO: try to repair choosing amount
                    amount_picker = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div/div')
                    amount_picker.click()
                    select_amount = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div/div/span[1]/div[2]')
                    driver.execute_script("arguments[0].setAttribute('aria-activedescendant', arguments[1])", select_amount, "react-select-6--option-1")

                    # add to basket
                    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/button').click()
                    time.sleep(2)
                    in_basket += 1

            except TimeoutException:
                print("Element not found")
            except ValueError:
                print("Cannot convert price to integer")
            except NoSuchElementException:
                print("Element doesn't exist")

            driver.get(
                'https://www.x-kom.pl/szukaj?q=rtx%203060%2012gb&f%5Bgroups%5D%5B5%5D=1&sort_by=accuracy_desc&f%5Bcategories%5D%5B345%5D=1')

def scan():
    while True:
        print("searching.....")
        price_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="listing-container"]/div[1]/div/div[2]/div[3]/div/div/div/div/span')))
        price = int(price_div.text.split(",")[0].replace(" ", ""))
        if price <= 4000:
            break
        time.sleep(5)
        driver.refresh()
    add_to_cart()

#scan for the cards
scan()

# go to cart
driver.get("https://www.x-kom.pl/koszyk")
try:
    forward = WebDriverWait(driver, 3) \
        .until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div/div[1]/div[2]/div[2]/button')))
    forward.click()

    forward = WebDriverWait(driver, 3) \
        .until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="app"]/div/div[1]/div/div[2]/div[1]/a[1]'))).click()

    # fill the form
    payment = WebDriverWait(driver, 3) \
        .until(EC.presence_of_element_located((By.XPATH, '//*[@id="platnosc"]/div[2]/div[5]/div[1]/label')))
    payment.click()

    # imie
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/form/div/div[1]/section[1]/div/div[1]/label/input'). \
        send_keys("")

    # adres
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/form/div/div[1]/section[1]/div/div[2]/label/input').send_keys(
        "")

    # kod pocztowy
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/form/div/div[1]/section[1]/div/div[3]/label/input').send_keys(
        "")

    # poczta
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/form/div/div[1]/section[1]/div/div[4]/label/input').send_keys(
        "")

    # email
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/form/div/div[1]/section[1]/div/div[5]/label/input').send_keys(
        "")

    # nr tel
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/form/div/div[1]/section[1]/div/div[6]/label/input').send_keys(
        "")

    checkbox = WebDriverWait(driver, 3).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="app"]/div/div[2]/form/div/div[1]/div[4]/div/div[2]/div[1]/label')))
    checkbox.click()
    # driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/form/div/div[1]/div[4]/div/div[2]/div[1]/label').click()
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/form/div/div[3]/div/div[1]/div[3]/div[3]/button').click()

    # buy
    # buy = WebDriverWait(driver, 15)\
    #     .until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/form/div/div[2]/div/div[1]/div/div[3]/button')))
    # buy.click()

except TimeoutException:
    print("Element doesn't exist")



