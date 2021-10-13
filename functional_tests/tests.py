import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self) -> None:
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User wants to visit a web app with To-Do capabilities. User visits the homepage
        self.browser.get(self.live_server_url)

        # User sees the title and header with To-Do in it
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # User is prompted to enter a to-do list item
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual("Enter a to-do item", inputbox.get_attribute('placeholder'))

        # User enters "1: get milk and eggs"
        inputbox.send_keys("Get milk and eggs")

        # When user hits enter, the list is updated
        inputbox.send_keys(Keys.ENTER)
        time.sleep(0.5)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")

        # There is still a box asking user to enter a to-do list item
        time.sleep(0.5)
        self.check_for_row_in_list_table('1: Get milk and eggs')

        # User enters "make cake batter"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Make cake batter")
        time.sleep(0.5)

        # User presses enter and the list updates again showing both items
        inputbox.send_keys(Keys.ENTER)
        time.sleep(0.5)

        self.check_for_row_in_list_table('1: Get milk and eggs')
        self.check_for_row_in_list_table('2: Make cake batter')

        # Now a new user, Francis, comes along to the site
        ## We use a new browser session to make sure that no information of Edith's is coming  through from the cookies
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the page, there is no sign of Edith's list

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(page_text, "Get milk and eggs")
        self.assertNotIn(page_text, "Make cake batter")

        # Francis starts a new list by entering a new item.

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Go to school")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(0.5)

        # Francis gets his own unique url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # There is no trace of Edith's list on Francis' list
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn(page_text, "Get milk and eggs")
        self.assertIn("Go to school", page_text)

        # Satisfied, they both go back to sleep
