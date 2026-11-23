from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from chats.models import Message


class MessageUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

    def test_func(self):
        return self.get_object().user_id == self.request.user.pk
