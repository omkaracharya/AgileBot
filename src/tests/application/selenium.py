# Selenium tests.

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

from main.application.action_builder import ActionBuilder
from main.application.agilebot import run
from main.data.commands import GIVEMYSTATUS, GROOMBACKLOG, PLANSPRINT
from main.data.environment import set_env, set_var
from tests.application.xpathhelper import get_latest_sent_message, next_message_xpath

AT_TESTER = '@Tester '

driver = None
message_input = None
actions = None


def check_response_in_following_messages(tester_request, expected_response_header, expected_response_body):
    message = tester_request
    while message is not None:
        try:
            message = message.find_element_by_xpath(next_message_xpath)
            if message.text.startswith('AgileBot'):
                assert_true(expected_response_header in message.text)
                assert_true(expected_response_body in message.text)
                break
        except NoSuchElementException:
            message = None
            # Fail on exception
            assert_true(False)


def get_odd_date():
    return datetime.strptime("10/23/2017", "%m/%d/%Y")


def get_even_date():
    return datetime.strptime("10/22/2017", "%m/%d/%Y")


def perform_action(date, action):
    actions = ActionChains(driver)
    actions.move_to_element(message_input)
    actions.click()
    actions.send_keys("@AgileBot " + action.command + ' ' + date.strftime("%m/%d/%Y"))
    actions.send_keys(Keys.RETURN)
    actions.perform()


def action_test(action, date, expected_response_body):
    perform_action(date, action)
    time.sleep(5)
    tester_request = driver.find_element_by_xpath(get_latest_sent_message(action))
    assert_is_not_none(tester_request)
    expected_response_header = AT_TESTER + action.RESPONSE_HEADER
    check_response_in_following_messages(tester_request, expected_response_header, expected_response_body)


class TestActions(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        global driver, message_input, actions
        set_env()
        set_var('MOCK', 'True')
        application = Thread(target=run)
        application.daemon = True
        application.start()
        driver = webdriver.Chrome(os.environ.get("CHROME_DRIVER_PATH"))
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
        assert_is_not_none(message_input)

    @classmethod
    def tearDownClass(self):
        driver.quit()

    def test_no_commits(self):
        date = get_even_date()
        action = ActionBuilder.build(GIVEMYSTATUS)
        action_test(action, date, action.INVALID_RESPONSE)

    def test_no_backlog(self):
        date = get_even_date()
        action = ActionBuilder.build(GROOMBACKLOG)
        action_test(action, date, action.INVALID_RESPONSE)

    def test_no_sprint(self):
        date = get_even_date()
        action = ActionBuilder.build(PLANSPRINT)
        action_test(action, date, action.INVALID_RESPONSE)

    def test_commits(self):
        date = get_odd_date()
        action = ActionBuilder.build(GIVEMYSTATUS)
        action_test(action, date, "\nSome commit message for some commit id.")

    def test_backlog(self):
        date = get_odd_date()
        action = ActionBuilder.build(GROOMBACKLOG)
        action_test(action, date,
                    "Story #1: First Story (Points: 1)\nStory #2: Second Story (Points: 2)\nStory #3: Third Story ("
                    "Points: 3)")

    def test_sprint(self):
        date = get_odd_date()
        action = ActionBuilder.build(PLANSPRINT)
        action_test(action, date,
                    "\nStory #1: First Story (Owner: @jsingh8 Points = 10)\nStory #2: Second Story (Owner: @yvlele "
                    "Points = 20)\nStory #3: Third Story (Owner: @oachary Points = 15)")
