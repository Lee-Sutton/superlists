import os
import inspect
import unittest
import requests
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def current_file_directory():
    return os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe())))


class WebServer(object):
    """
    Class to control starting and stopping the webserver
    """
    url = 'http://localhost:8000'

    def __init__(self):
        self.server = None

    def start(self):
        """
        Starts the webserver if it is not already running
        """
        try:
            requests.get(self.url)

        except Exception:
            self._start_server()

    def _start_server(self):
        command = ['/Users/Lee/.virtualenvs/django/bin/python',
                   self._path_to_server(), 'runserver']
        self.server = subprocess.Popen(command)

    def _path_to_server(self):
        return os.path.join(current_file_directory(), 'manage.py')

    def stop(self):
        """
        Stops the web server by sending a SIGTERM
        """
        if self.server:
            self.server.terminate()


class NewVisitorTest(unittest.TestCase):
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

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(any(row.text == '1: Buy peacock feathers' for
                            row in rows))

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


def main():
    """
    Starts the django webserver before running the unit tests
    """
    server = WebServer()
    server.start()
    try:
        unittest.main()
    except Exception:
        server.stop()


if __name__ == '__main__':
    main()
