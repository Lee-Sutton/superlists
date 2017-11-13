from django.test import TestCase


class SmokeTest(TestCase):
    """
    Unit tests for the lists application
    """

    def test_uses_home_template(self):
        """
        Tests the home page returns the required html content
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))

    def test_can_save_POST_request(self):
        """test_can_save_POST_request
        Tests that the home page can save the data from
        a post request with the input todo item
        """
        response = self.client.post('/',
                                    data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
