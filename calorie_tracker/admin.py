from django.contrib import admin
from .models import UserCalorieData, CalorieAtePerDay, Food


class FoodInline(admin.StackedInline):
    extra = 0
    model = Food
    fields = ('food', 'calories')


@admin.register(CalorieAtePerDay)
class ColorieAtePerDayAdmin(admin.ModelAdmin):
    list_display = ('calorie_data', 'max_calorie', 'current_calorie', 'destroy_data', 'create_data')
    inlines = [FoodInline, ]


@admin.register(UserCalorieData)
class UserCalorieDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'age', 'calorie_per_day')
