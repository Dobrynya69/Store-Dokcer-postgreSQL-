from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from .views import *

class GameListPageTest(TestCase):


    def setUp(self):
        self.url_reverse = reverse('game_list')
        self.response = self.client.get(reverse('game_list'))


    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)


    def test_template(self):
        self.assertTemplateUsed(self.response, 'games/list.html')


    def test_url_resolves(self):
        view = resolve(self.url_reverse)
        self.assertEqual(view.func.__name__, GamesListView.as_view().__name__)


class GameDetailPageTest(TestCase):

    def setUp(self): 
        self.studio = Studio.objects.create(name='Studio')
        self.game = Game.objects.create(
            name='Game',
            description='Desc',
            cost='1.1',
            studio=self.studio
        )
        self.url_reverse = reverse('game', kwargs={'pk': self.game.pk})
        self.response = self.client.get(reverse('game', kwargs={'pk': self.game.pk}))


    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)


    def test_template(self):
        self.assertTemplateUsed(self.response, 'games/detail.html')


    def test_url_resolves(self):
        view = resolve(self.url_reverse)
        self.assertEqual(view.func.__name__, GamesDetailView.as_view().__name__)