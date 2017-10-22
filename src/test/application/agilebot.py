import os
import time
from datetime import datetime
from threading import Thread

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from main.application.agilebot import run
from main.data.environment import set_env

application = None
driver = None
try:
    set_env()
    application = Thread(target=run)
    application.daemon = True
    application.start()
    TESTER_PASSWORD = os.environ.get("TESTER_PASSWORD")

    TESTER_EMAIL = os.environ.get("TESTER_EMAIL")

    CHROME_DRIVER_PATH = os.environ.get("CHROME_DRIVER_PATH")
    SLACK_URL = os.environ.get("SLACK_URL")

    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    driver.get(SLACK_URL)
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((By.ID, "signin_btn")))
    email = driver.find_element_by_id("email")
    password = driver.find_element_by_id("password")

    email.send_keys(TESTER_EMAIL)
    password.send_keys(TESTER_PASSWORD)

    sign_in = driver.find_element_by_id("signin_btn")
    sign_in.click()

    wait.until(EC.title_contains("general"))

    driver.get(SLACK_URL + "messages/agilebot-test")
    wait.until(EC.title_contains("agilebot-test"))

    wait.until(EC.presence_of_element_located((By.ID, "msg_input")))
    message_input = driver.find_element_by_id("msg_input")
    assert message_input is not None

    actions = ActionChains(driver)
    actions.move_to_element(message_input)
    actions.click()
    actions.send_keys("@AgileBot givemystatus " + datetime.today().strftime("%m/%d/%Y"))
    actions.send_keys(Keys.RETURN)
    actions.perform()

    time.sleep(5)

    tester_request = driver.find_element_by_xpath(
        '(//div[@class="message_content"]//span[@class="message_body"][starts-with(text()," givemystatus")]/..//div[@class="message_content_header_left"]//a[text()="Tester"])[last()]')
    assert tester_request is not None
    next_message_xpath = '../../../../following-sibling::ts-message'
    message = tester_request
    while message is not None:
        try:
            message = message.find_element_by_xpath(next_message_xpath)
            print(message.text)
            if message.text.startswith('AgileBot'):
                assert ('@Tester Here is your status for ' + datetime.today().strftime("%m/%d/%Y")) in message.text
                print('Test passed')
                break
        except NoSuchElementException:
            print('Test failed')
            message = None
finally:
    driver.quit()
