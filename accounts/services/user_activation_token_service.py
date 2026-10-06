from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator

User = get_user_model()


class UserActivationTokenService(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: User, timestamp: int):
        return f"{user.pk}{user.password}{timestamp}{user.email}{user.is_active}"

activation_token_service = UserActivationTokenService()
