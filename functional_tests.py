from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):


        #User wants to visit a web app with To-Do capabilities. User visits the homepage
        self.browser.get("http://localhost:8000")

        #User sees the title and header with To-Do in it
        self.assertIn('To-Do', self.browser.title)
        self.fail("Finish the test!")


        #User is prompted to enter a to-do list item

        # User enters "1: get milk and eggs"
        # When user hits enter, the list is updated
        # There is still a box asking user to enter a to-do list item

        # User enters "make cake batter"
        # User presses enter and the list updates again showing both items
        # User wants the site to remember her list of items.
        # A unique URL is generated for the user and there are some instructions explaining the same
        # User visits the given url and can see the previous list

if __name__ == '__main__':
    # unittest.main(warnings='ignore')
    unittest.main()