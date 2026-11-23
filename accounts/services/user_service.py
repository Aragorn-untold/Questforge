from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.http import urlsafe_base64_encode

from accounts.models import Profile
# from accounts.services.email_service import UserEmailService
from accounts.services.user_activation_token_service import UserActivationTokenService

User = get_user_model()


class UserService:
    def __init__(self, token_service: UserActivationTokenService):
        self._token_service = token_service
        # self._email_service = email_service

    def _get_uid(self, user: User):
        return urlsafe_base64_encode(str(user.pk).encode())

    def _get_activation_link(self, url: str, user: User):
        uid = self._get_uid(user)
        token = self._token_service.make_token(user)

        return f"{url}accounts/activate/{uid}/{token}/"

    def register_user(self, username: str, email: str, password: str, url: str) -> User:
        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=True
            )
            # user.groups.add(Group.objects.get(name="InactiveUser"))
            Profile.objects.create(user=user)
            activation_link = self._get_activation_link(url, user)
            # Todo: send email
            print("Email sent")
            print(activation_link)

        return user
