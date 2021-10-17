import os
import sys
import time
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

WAIT_INTERVAL = 1
MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time >MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        # Edith wants to use a web app with To-Do capabilities.
        # Edith visits our homepage
        self.browser.get(self.live_server_url)

        # Edith sees the title and header with To-Do in it
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Edith is prompted to enter a to-do list item
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual("Enter a to-do item", inputbox.get_attribute('placeholder'))

        # Edith enters "Get milk and eggs"
        inputbox.send_keys("Get milk and eggs")

        # Edith hits enter, the list is updated
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Get milk and eggs')

        # There is still a box asking Edith to enter a to-do list item

        # Edith types "make cake batter"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Make cake batter")
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('2: Make cake batter')
        self.wait_for_row_in_list_table('1: Get milk and eggs')

        # Satisfied she goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Get milk and eggs")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Get milk and eggs')

        # She notices that her list has a unique rls
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")

        # Now a new user, Francis, comes along to the site
        ## We use a new browser session to make sure that
        ## no information of Edith's is coming through from cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the page, there is no sign of Edith's list

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn("Get milk and eggs", page_text)
        self.assertNotIn("Make cake batter", page_text)

        # Francis starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Go to school")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Go to school")

        # Francis gets his own unique url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # There is no trace of Edith's list on Francis' list
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Get milk and eggs", page_text)
        self.assertIn("Go to school", page_text)

        # Satisfied, they both go back to sleep

    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + (inputbox.size['width'] / 2),
            512,
            delta=6)

        # She starts a new list and sees that the input box is nicely centered there too.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Edith wants everything centered")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Edith wants everything centered")
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + (inputbox.size['width'] / 2),
            512,
            delta=6)

