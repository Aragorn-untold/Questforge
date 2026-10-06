from decimal import Decimal
from itertools import count

from django.contrib.auth import get_user_model

from accounts.models import Profile
from campaigns.models import Campaign
from characters.models import Character, CharacterClass, Race
from compendium.items.models import CampaignItem, Item
from compendium.monsters.models import CampaignMonster, Monster
from compendium.quests.models import CampaignQuest, Quest

_campaign_creator_ids = count()


def create_user(username="player", **kwargs):
    User = get_user_model()
    user = User.objects.create_user(
        username=username,
        email=f"{username}@example.com",
        password="StrongPass!234",
        **kwargs,
    )
    Profile.objects.create(user=user)
    return user


def create_campaign(creator=None, title="Test Campaign", **kwargs):
    creator = creator or create_user(f"game-master-{next(_campaign_creator_ids)}")
    defaults = {
        "description": "A campaign for tests.",
        "is_active": Campaign.ActiveChoice.ACTIVE,
    }
    defaults.update(kwargs)
    return Campaign.objects.create(title=title, creator=creator, **defaults)


def create_race(name="Elf"):
    race, _ = Race.objects.get_or_create(
        name=name,
        defaults={
            "ability": "Dexterity +2",
            "race_traits_description": "Keen senses and darkvision.",
        },
    )
    return race


def create_character_class(name="Ranger"):
    character_class, _ = CharacterClass.objects.get_or_create(
        name=name,
        defaults={
            "ability": "Dexterity",
            "class_traits_description": "A skilled wilderness explorer.",
        },
    )
    return character_class


def create_character(campaign, player, name="Test Hero", **kwargs):
    race = kwargs.pop("race", None) or create_race()
    character_class = kwargs.pop("character_class", None) or create_character_class()
    return Character.objects.create(
        campaign=campaign,
        player=player,
        name=name,
        race=race,
        character_class=character_class,
        **kwargs,
    )


def create_item(name="Test Item", **kwargs):
    defaults = {
        "type": Item.TypeChoice.WEAPON,
        "rarity": Item.RarityChoice.COMMON,
        "description": "A dependable test weapon.",
        "damage": "1d8 slashing",
        "protection": None,
        "effect": "Versatile",
        "weight": 3.0,
        "price": Decimal("15.00"),
    }
    defaults.update(kwargs)
    return Item.objects.create(name=name, **defaults)


def create_campaign_item(campaign, name="Campaign Test Item", **kwargs):
    defaults = {
        "type": Item.TypeChoice.WEAPON,
        "rarity": Item.RarityChoice.COMMON,
        "description": "An item assigned to one campaign.",
        "weight": 1.0,
        "price": Decimal("5.00"),
    }
    defaults.update(kwargs)
    return CampaignItem.objects.create(campaign=campaign, name=name, **defaults)


def create_quest(title="Test Quest", **kwargs):
    defaults = {
        "description": "Find the lost waystone.",
        "reward_description": "A pouch of silver.",
        "difficulty_rating": Quest.DifficultyChoice.MEDIUM,
        "level_recommendation": "1-3",
    }
    defaults.update(kwargs)
    return Quest.objects.create(title=title, **defaults)


def create_campaign_quest(campaign, title="Campaign Test Quest", **kwargs):
    defaults = {
        "description": "Recover an ancient map.",
        "reward_description": "A map case.",
        "difficulty_rating": Quest.DifficultyChoice.EASY,
        "level_recommendation": "1-2",
    }
    defaults.update(kwargs)
    return CampaignQuest.objects.create(campaign=campaign, title=title, **defaults)


def create_monster(name="Test Wolf", **kwargs):
    defaults = {
        "type": Monster.TypeChoice.BEAST,
        "alignment": Monster.AlignmentChoice.UNALIGNED,
        "challenge_rating": Monster.ChallengeChoice.EASY,
        "hit_points": 11,
        "armor_class": 13,
        "abilities": "Keen hearing and smell.",
    }
    defaults.update(kwargs)
    return Monster.objects.create(name=name, **defaults)


def create_campaign_monster(campaign, name="Campaign Test Monster", **kwargs):
    defaults = {
        "type": Monster.TypeChoice.BEAST,
        "alignment": Monster.AlignmentChoice.UNALIGNED,
        "challenge_rating": Monster.ChallengeChoice.EASY,
        "hit_points": 11,
        "armor_class": 13,
        "abilities": "Pack tactics.",
    }
    defaults.update(kwargs)
    return CampaignMonster.objects.create(campaign=campaign, name=name, **defaults)
