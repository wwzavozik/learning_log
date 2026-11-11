from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Topic


class TopicAccessTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner')
        self.other = User.objects.create_user(username='other')
        self.topic = Topic.objects.create(text='Django', owner=self.owner)
        self.topic_url = reverse('learning_logs:topic', args=[self.topic.id])

    def test_guest_is_sent_to_login(self):
        response = self.client.get(self.topic_url)
        self.assertRedirects(
            response,
            reverse('users:login') + '?next=' + self.topic_url,
        )

    def test_owner_can_open_topic(self):
        self.client.force_login(self.owner)
        response = self.client.get(self.topic_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.topic.text)

    def test_other_user_cannot_open_topic(self):
        self.client.force_login(self.other)
        response = self.client.get(self.topic_url)
        self.assertEqual(response.status_code, 404)

    def test_get_does_not_log_user_out(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 405)
        self.assertIn('_auth_user_id', self.client.session)
