from unittest import skip

from selenium.webdriver.common.keys import Keys

from .base import FunctionalTests


class ItemValidationTest(FunctionalTests):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit an empty list item.
        self.browser.get(self.live_server_url)
        # She hits enter on an empty input box
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request and does not load the list page
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

        # She tries again with some text for the item and it works.
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))

        # And she can submit successfully
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Perversely, she now decides to enter a second empty list item.
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Again the browser will not comply
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

        # She can correct the error by entering some text.
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # Edith goes to the home page and starts a new list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Dupe the duke')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Dupe the duke')

        # She accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys('Dupe the duke')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # She sees a helpful error message about duplicate lists
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You've already got this item in your list"
        ))
