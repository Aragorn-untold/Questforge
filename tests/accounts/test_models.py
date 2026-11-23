from django.test import TestCase
from django.urls import reverse

from tests.helpers import create_user


class UserModelTests(TestCase):
    def test_profile_url_uses_the_users_primary_key(self):
        user = create_user("url-user")

        self.assertEqual(user.get_absolute_url(), reverse("accounts:user-detail", args=[user.pk]))

    def test_string_representation_includes_username_and_id(self):
        user = create_user("string-user")

        self.assertEqual(str(user), f"string-user id: {user.pk}")
