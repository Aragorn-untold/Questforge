from django.views import generic

from quests.forms import QuestSearchForm
from quests.models import Quest


class QuestListView(generic.ListView):
    model = Quest
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quest_search_form"] = QuestSearchForm(initial={"title": self.request.GET.get("title", "")})
        context["clear"] = context.get("quest_search_form", "")["title"].value() or None
        return context

    def get_queryset(self):
        queryset = Quest.objects.all()
        title = self.request.GET.get("title")
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset


class QuestDetailView(generic.DetailView):
    model = Quest
