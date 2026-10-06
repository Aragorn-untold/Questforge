from django.views import generic

from compendium.items.forms import ItemSearchForm
from compendium.items.models import Item


class ItemListView(generic.ListView):
    model = Item
    template_name = "compendium/items/item_list.html"
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item_search_form"] = ItemSearchForm(initial={"name": self.request.GET.get("name", "")})
        context["clear"] = context.get("item_search_form", "")["name"].value() or None
        return context

    def get_queryset(self):
        queryset = Item.objects.all()
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class ItemDetailView(generic.DetailView):
    model = Item
    template_name = "compendium/items/item_detail.html"
