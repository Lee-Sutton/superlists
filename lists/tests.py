from django.test import TestCase


class SmokeTest(TestCase):

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
