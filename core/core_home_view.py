from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import render

from campaigns.models import Campaign


def home_view(request):
    num_players = get_user_model().objects.count()
    num_campaigns = Campaign.objects.filter(~Q(is_active=Campaign.ActiveChoice.ENDED)).count()
    context = {
        "num_players": num_players,
        "num_campaigns": num_campaigns
    }
    return render(request, "home.html", context=context)
