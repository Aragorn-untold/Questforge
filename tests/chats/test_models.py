from django.test import TestCase

from chats.models import Message
from tests.helpers import create_user


class MessageModelTests(TestCase):
    def test_author_reverse_relation_returns_their_messages(self):
        author = create_user("tavern-author")
        message = Message.objects.create(user=author, content="The road is clear.")

        self.assertEqual(author.chat_messages.get(), message)
        self.assertEqual(message.content, "The road is clear.")
