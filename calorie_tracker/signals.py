from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CalorieAtePerDay, UserCalorieData


@receiver(post_save, sender=UserCalorieData)
def first_calorie_ate_per_day(sender, instance, created, **kwargs):
    if created:
        calorie_data = instance
        CalorieAtePerDay.objects.create(max_calorie=calorie_data.calorie_per_day, calorie_data=calorie_data)

