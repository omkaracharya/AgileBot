import os
import time
import unittest
from datetime import datetime
from threading import Thread

from nose.tools import assert_is_not_none, assert_true
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from main.application.agilebot import run
from main.data.environment import set_env

driver = None


class TestActions(unittest.TestCase):
    def setUp(self):
        set_env()
        application = Thread(target=run)
        application.daemon = True
        application.start()
        global driver
        driver = webdriver.Chrome(os.environ.get("CHROME_DRIVER_PATH"))

    def tearDown(self):
        driver.quit()

    def test_no_commits(self):
        driver.get(os.environ.get("SLACK_URL"))
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.ID, "signin_btn")))
        email = driver.find_element_by_id("email")
        password = driver.find_element_by_id("password")

        email.send_keys(os.environ.get("TESTER_EMAIL"))
        password.send_keys(os.environ.get("TESTER_PASSWORD"))

        sign_in = driver.find_element_by_id("signin_btn")
        sign_in.click()

        wait.until(EC.title_contains("general"))

        driver.get(os.environ.get("SLACK_URL") + "messages/agilebot-test")
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
        assert_is_not_none(tester_request)
        next_message_xpath = '../../../../following-sibling::ts-message'
        message = tester_request
        while message is not None:
            try:
                message = message.find_element_by_xpath(next_message_xpath)
                if message.text.startswith('AgileBot'):
                    assert_true(
                        ('@Tester Here is your status for ' + datetime.today().strftime("%m/%d/%Y")) in message.text)
                    break
            except NoSuchElementException:
                message = None

    def test_no_backlog(self):
        driver.get(os.environ.get("SLACK_URL"))
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.ID, "signin_btn")))
        email = driver.find_element_by_id("email")
        password = driver.find_element_by_id("password")

        email.send_keys(os.environ.get("TESTER_EMAIL"))
        password.send_keys(os.environ.get("TESTER_PASSWORD"))

        sign_in = driver.find_element_by_id("signin_btn")
        sign_in.click()

        wait.until(EC.title_contains("general"))

        driver.get(os.environ.get("SLACK_URL") + "messages/agilebot-test")
        wait.until(EC.title_contains("agilebot-test"))

        wait.until(EC.presence_of_element_located((By.ID, "msg_input")))
        message_input = driver.find_element_by_id("msg_input")
        assert message_input is not None

        actions = ActionChains(driver)
        actions.move_to_element(message_input)
        actions.click()
        actions.send_keys("@AgileBot groombacklog")
        actions.send_keys(Keys.RETURN)
        actions.perform()

        time.sleep(5)

        tester_request = driver.find_element_by_xpath(
            '(//div[@class="message_content"]//span[@class="message_body"][starts-with(text()," groombacklog")]/..//div[@class="message_content_header_left"]//a[text()="Tester"])[last()]')
        assert_is_not_none(tester_request)
        next_message_xpath = '../../../../following-sibling::ts-message'
        message = tester_request
        while message is not None:
            try:
                message = message.find_element_by_xpath(next_message_xpath)
                if message.text.startswith('AgileBot'):
                    assert_true(('@Tester Groomed Backlog:') in message.text)
                    break
            except NoSuchElementException:
                message = None

    def test_no_sprint(self):
        driver.get(os.environ.get("SLACK_URL"))
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.ID, "signin_btn")))
        email = driver.find_element_by_id("email")
        password = driver.find_element_by_id("password")

        email.send_keys(os.environ.get("TESTER_EMAIL"))
        password.send_keys(os.environ.get("TESTER_PASSWORD"))

        sign_in = driver.find_element_by_id("signin_btn")
        sign_in.click()

        wait.until(EC.title_contains("general"))

        driver.get(os.environ.get("SLACK_URL") + "messages/agilebot-test")
        wait.until(EC.title_contains("agilebot-test"))

        wait.until(EC.presence_of_element_located((By.ID, "msg_input")))
        message_input = driver.find_element_by_id("msg_input")
        assert message_input is not None

        actions = ActionChains(driver)
        actions.move_to_element(message_input)
        actions.click()
        actions.send_keys("@AgileBot plansprint " + datetime.today().strftime("%m/%d/%Y"))
        actions.send_keys(Keys.RETURN)
        actions.perform()

        time.sleep(5)

        tester_request = driver.find_element_by_xpath(
            '(//div[@class="message_content"]//span[@class="message_body"][starts-with(text()," plansprint")]/..//div[@class="message_content_header_left"]//a[text()="Tester"])[last()]')
        assert_is_not_none(tester_request)
        next_message_xpath = '../../../../following-sibling::ts-message'
        message = tester_request
        while message is not None:
            try:
                message = message.find_element_by_xpath(next_message_xpath)
                if message.text.startswith('AgileBot'):
                    assert_true(('@Tester Tentative Sprint Plan for ' + datetime.today().strftime("%m/%d/%Y")) in message.text)
                    break
            except NoSuchElementException:
                message = None
