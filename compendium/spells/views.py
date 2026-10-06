from django.views import generic

from compendium.spells.forms import SpellSearchForm
from compendium.spells.models import Spell


class SpellListView(generic.ListView):
    model = Spell
    template_name = "compendium/spells/spell_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["spell_search_form"] = SpellSearchForm(initial={"name": self.request.GET.get("name", "")})
        context["clear"] = context.get("spell_search_form", "")["name"].value() or None
        return context

    def get_queryset(self):
        queryset = Spell.objects.prefetch_related("allowed_classes")
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class SpellDetailView(generic.DetailView):
    model = Spell
    template_name = "compendium/spells/spell_detail.html"
