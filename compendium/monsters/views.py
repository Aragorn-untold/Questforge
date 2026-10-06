from django.views import generic

from compendium.monsters.forms import MonsterSearchForm
from compendium.monsters.models import Monster


class MonsterListView(generic.ListView):
    model = Monster
    template_name = "compendium/monsters/monster_list.html"
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["monster_search_form"] = MonsterSearchForm(initial={"name": self.request.GET.get("name", "")})
        context["clear"] = context.get("monster_search_form", "")["name"].value() or None
        return context

    def get_queryset(self):
        queryset = Monster.objects.all()
        name = self.request.GET.get("name", "").strip()
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class MonsterDetailView(generic.DetailView):
    model = Monster
    template_name = "compendium/monsters/monster_detail.html"
