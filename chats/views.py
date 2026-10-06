from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from chats.forms import MessageForm
from chats.mixin import MessageUserMixin
from chats.models import Message


class MessageListView(generic.ListView):
    model = Message
    template_name = "chats/message_list.html"
    context_object_name = "message_list"
    ordering = ("-created_at", "-pk")
    paginate_by = 30

    def get_queryset(self):
        return super().get_queryset().select_related("user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message_form"] = MessageForm()
        return context


class MessageCreateView(LoginRequiredMixin, generic.CreateView):
    model = Message
    form_class = MessageForm
    template_name = "chats/message_form.html"
    success_url = reverse_lazy("chats:chats-message-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MessageUpdateView(MessageUserMixin, generic.UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "chats/message_form.html"
    success_url = reverse_lazy("chats:chats-message-list")


class MessageDeleteView(MessageUserMixin, generic.DeleteView):
    model = Message
    template_name = "chats/message_confirm_delete.html"
    success_url = reverse_lazy("chats:chats-message-list")
