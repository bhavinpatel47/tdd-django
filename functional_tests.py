import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import wait

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.wait = WebDriverWait(self.browser, 10)
        self.browser.implicitly_wait(3)

    def tearDown(self) -> None:
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        self.wait.until(EC.StaleElementReferenceException)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User wants to visit a web app with To-Do capabilities. User visits the homepage
        self.browser.get("http://localhost:8000")

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

        # There is still a box asking user to enter a to-do list item
        time.sleep(1)
        self.check_for_row_in_list_table('1: Get milk and eggs')

        # self.assertTrue(any(row.text == '1: Get milk and eggs' for row in rows),
        #                 f'New to-do item did not appear in table.\nIt was {table.text}')

        # User enters "make cake batter"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Make cake batter")
        time.sleep(1)

        # User presses enter and the list updates again showing both items
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table('1: Get milk and eggs')
        self.check_for_row_in_list_table('2: Make cake batter')

        # User wants the site to remember her list of items.
        # A unique URL is generated for the user and there are some instructions explaining the same
        # User visits the given url and can see the previous list
        self.fail("Finish the test!")


if __name__ == '__main__':
    # unittest.main(warnings='ignore')
    unittest.main()
