from django.shortcuts import render


def compendium_view(request):
    return render(request, "compendium/compendium_page.html")
