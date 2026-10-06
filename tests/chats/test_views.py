from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from chats.models import Message
from tests.helpers import create_user


class MessageViewTests(TestCase):
    def setUp(self):
        self.author = create_user("tavern-author-view")
        self.other_user = create_user("tavern-other-view")
        self.list_url = reverse("chats:chats-message-list")
        self.create_url = reverse("chats:chats-message-create")

    def test_message_list_shows_messages_and_composer_only_to_signed_in_users(self):
        message = Message.objects.create(user=self.author, content="Welcome to the tavern.")

        response = self.client.get(self.list_url)

        self.assertContains(response, message.content)
        self.assertNotContains(response, "Share something with the tavern")

        self.client.force_login(self.author)
        response = self.client.get(self.list_url)

        self.assertContains(response, message.content)
        self.assertContains(response, "Share something with the tavern")

    def test_message_list_orders_newest_first(self):
        older = Message.objects.create(user=self.author, content="Older message")
        newer = Message.objects.create(user=self.other_user, content="Newer message")
        Message.objects.filter(pk=older.pk).update(
            created_at=timezone.now() - timedelta(days=1)
        )

        response = self.client.get(self.list_url)

        self.assertEqual(list(response.context["message_list"]), [newer, older])

    def test_anonymous_users_are_redirected_from_message_creation(self):
        response = self.client.post(self.create_url, {"content": "Anonymous post"})

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response["Location"])
        self.assertFalse(Message.objects.filter(content="Anonymous post").exists())

    def test_authenticated_user_is_assigned_as_message_author(self):
        self.client.force_login(self.author)

        response = self.client.post(self.create_url, {"content": "A new message"})

        self.assertRedirects(response, self.list_url)
        message = Message.objects.get(content="A new message")
        self.assertEqual(message.user, self.author)

    def test_only_message_author_can_edit_or_delete(self):
        message = Message.objects.create(user=self.author, content="Original text")
        update_url = reverse("chats:chats-message-update", args=[message.pk])
        delete_url = reverse("chats:chats-message-delete", args=[message.pk])
        self.client.force_login(self.other_user)

        self.assertEqual(self.client.get(update_url).status_code, 404)
        self.assertEqual(self.client.post(delete_url).status_code, 404)
        self.assertTrue(Message.objects.filter(pk=message.pk).exists())

        self.client.force_login(self.author)
        response = self.client.post(update_url, {"content": "Updated text"})

        self.assertRedirects(response, self.list_url)
        message.refresh_from_db()
        self.assertEqual(message.content, "Updated text")

        response = self.client.post(delete_url)

        self.assertRedirects(response, self.list_url)
        self.assertFalse(Message.objects.filter(pk=message.pk).exists())
