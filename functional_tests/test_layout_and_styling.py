from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class LayoutAndStyling(FunctionalTest):

    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + (inputbox.size['width'] / 2),
            512,
            delta=6)

        # She starts a new list and sees that the input box is
        # nicely centered there too.
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Edith wants everything centered")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Edith wants everything centered")
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + (inputbox.size['width'] / 2),
            512,
            delta=6)
