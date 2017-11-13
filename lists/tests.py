"""
Unit tests for the lists application
"""
from django.test import TestCase
from lists.models import Item


class HomePageTest(TestCase):
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

    def test_can_save_post_request(self):
        """test_can_save_POST_request
        Tests that the home page can save the data from
        a post request with the input todo item
        """
        response = self.client.post('/',
                                    data={'item_text': 'A new list item'})
        # The posted item should be saved in the database
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        """
        Test that the home page returns a redirect
        after a post request
        """
        response = self.client.post('/',
                                    data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_only_saves_item_when_necessary(self):
        """
        Check that the requests on the home page only
        save data when needed ie. during a post request
        """
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_list_items(self):
        """
        The home page should display all the list items
        """
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())



class ItemModelTest(TestCase):
    """
    Unit Tests for the item model class.
    """

    def test_saving_and_retrieving_data(self):
        """
        Check that the we are able to create new todo Items
        save the data and retrieve them
        """
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text,
                         'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

