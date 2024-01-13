import datetime

from django.contrib.auth import get_user_model
from django.db import models


class UserCalorieData(models.Model):
    PHYSICAL_ACTIVITY = [1.2, 1.375, 1.55, 1.725, 1.9]

    GENDER_CALORIE = [88.362, 447.593]

    class GenderChoose(models.IntegerChoices):
        MALE = (1, 'male')
        FEMALE = (2, 'female')
        __empty__ = "Gender"

    class PhysicalActivityChoose(models.IntegerChoices):
        WITHOUT = (0, 'without')
        LIGHT = (1, 'light')
        MIDDLE = (2, 'middle')
        HIGH = (3, 'high')
        VERY_HiGH = (4, 'very high')
        __empty__ = "Physical Activity"

    user = models.OneToOneField(to=get_user_model(), related_name='calorie_data', on_delete=models.CASCADE)
    gender = models.IntegerField(choices=GenderChoose)
    age = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    calorie_per_day = models.PositiveIntegerField(editable=False)
    physical_activity = models.IntegerField(choices=PhysicalActivityChoose)

    def __str__(self):
        return self.user.username

    def save(
            self, *args, **kwargs
    ):
        """
        Calculates the daily calorie count for the day and save it.
        """
        gender = self.gender - 1
        if gender == 0:
            BMR = self.GENDER_CALORIE[gender] + (13.397 * float(self.weight)) + (4.799 * self.height) - (
                    5.677 - self.age)
        else:
            BMR = self.GENDER_CALORIE[gender] + (9.247 * float(self.weight)) + (3.098 * self.height) - (
                    4.330 - self.age)

        calories = BMR * self.PHYSICAL_ACTIVITY[self.physical_activity]

        self.calorie_per_day = calories
        super().save(*args, **kwargs)


class CalorieAtePerDay(models.Model):
    calorie_data = models.ForeignKey('UserCalorieData', related_name='calorie_history', on_delete=models.CASCADE)
    max_calorie = models.PositiveIntegerField(editable=False)
    current_calorie = models.PositiveIntegerField(editable=False, default=0, null=True, blank=True)
    create_data = models.DateField(editable=False, auto_now_add=True)
    destroy_data = models.DateField(editable=False,
                                    default=datetime.datetime.now().date() + datetime.timedelta(days=1))

    def __str__(self):
        return self.calorie_data.user.username + ' data'


class Food(models.Model):
    food = models.CharField(max_length=255)
    calories = models.PositiveIntegerField()
    time_of_add = models.DateTimeField(editable=False, auto_now_add=datetime.datetime.now().time(), )
    calorie_today = models.ForeignKey(to='CalorieAtePerDay', on_delete=models.CASCADE, related_name='foods')

    def __str__(self):
        return self.food[:50]
