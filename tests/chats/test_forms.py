from django.test import SimpleTestCase

from chats.forms import MessageForm


class MessageFormTests(SimpleTestCase):
    def test_only_message_content_is_editable(self):
        form = MessageForm()

        self.assertEqual(tuple(form.fields), ("content",))
        self.assertEqual(form.fields["content"].widget.attrs["rows"], 3)
        self.assertEqual(
            form.fields["content"].widget.attrs["placeholder"],
            "Share something with the tavern…",
        )

    def test_empty_message_is_rejected(self):
        form = MessageForm(data={"content": "   "})

        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)
