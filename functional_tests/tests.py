import os
import inspect
import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase

MAX_TIMEOUT_S = 10


def current_file_directory():
    """
    Returns string containing the path to the
    current file directory
    """
    return os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe())))


class NewVisitorTest(LiveServerTestCase):
    """
    Tests when a new user views the site
    """

    def setUp(self):
        """
        Initialization of the browser
        """
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """
        Quits browser when tests are finished
        """
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """
        Checks if the input row text exists in the todo list table
        """
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_TIMEOUT_S:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertTrue('To-Do' in self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'),
                         'Enter a to-do item')

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        input_box.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        input_box.send_keys(Keys.ENTER)

        row_text = '1: Buy peacock feathers'
        self.wait_for_row_in_list_table(row_text)

        # There is still a text box inviting her to add another item
        # she enters "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again and now shows both items in her list
        row_text = '1: Buy peacock feathers'
        self.wait_for_row_in_list_table(row_text)
        row_text = '2: Use peacock feathers to make a fly'
        self.wait_for_row_in_list_table(row_text)

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)
        self.fail('Finish the test!')

        # The page updates again, and now shows both items on her list

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep
