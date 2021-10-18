from unittest import skip

from .base import FunctionalTests


class ItemValidationTest(FunctionalTests):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit an empty list item.
        # She hits enter on an empty input box

        # The home page refreshes, and there is an error message saying that list items cannot be blank.
        # She tries again with some text for the item and it works.
        # Perversely, she now decides to enter a second empty list item.

        # She receives a similar warning on the list page.
        # She can correct the error by entering some text.

        self.fail("finish the test")
