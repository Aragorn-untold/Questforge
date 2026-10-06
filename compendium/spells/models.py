from django.db import models

from characters.models import CharacterClass


class Spell(models.Model):
    class SpellLevelChoice(models.IntegerChoices):
        CANTRIP = 0, "Cantrip"
        FIRST = 1, "1st level"
        SECOND = 2, "2nd level"
        THIRD = 3, "3rd level"
        FOURTH = 4, "4th level"
        FIFTH = 5, "5th level"
        SIXTH = 6, "6th level"
        SEVENTH = 7, "7th level"
        EIGHTH = 8, "8th level"
        NINTH = 9, "9th level"

    class SpellSchoolChoice(models.TextChoices):
        ABJURATION = "ABJ", "Abjuration"
        CONJURATION = "CON", "Conjuration"
        DIVINATION = "DIV", "Divination"
        ENCHANTMENT = "ENC", "Enchantment"
        EVOCATION = "EVO", "Evocation"
        ILLUSION = "ILL", "Illusion"
        NECROMANCY = "NEC", "Necromancy"
        TRANSMUTATION = "TRA", "Transmutation"

    class SavingThrowChoice(models.TextChoices):
        STRENGTH = "STR", "Strength"
        DEXTERITY = "DEX", "Dexterity"
        CONSTITUTION = "CON", "Constitution"
        INTELLIGENCE = "INT", "Intelligence"
        WISDOM = "WIS", "Wisdom"
        CHARISMA = "CHA", "Charisma"

    allowed_classes = models.ManyToManyField(CharacterClass, related_name="allowed_spells")
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    level = models.PositiveSmallIntegerField(choices=SpellLevelChoice.choices)
    school = models.CharField(max_length=78, choices=SpellSchoolChoice.choices)
    concentration_required = models.BooleanField()
    cast_as_ritual = models.BooleanField() # adds 10 min to cast_time
    cast_time = models.CharField(max_length=66) # 1 action or 1 min or 1 hour
    spell_range = models.CharField(max_length=50) # Touch or num ft or Self(num ft)
    spell_duration = models.CharField(max_length=55) # Instantaneous or num mins/hours with Concentration if concentration_required=True or Special
    saving_throw = models.CharField(max_length=5, choices=SavingThrowChoice.choices, null=True, blank=True)
    damage = models.CharField(max_length=30, null=True, blank=True) # 1d8 + type(if present) or Weapon + 1d8 + type(if present)

    def __str__(self) -> str:
        return f"{self.name} | {self.get_school_display()} | {self.get_level_display()}"

    class Meta:
        ordering = ["name"]
