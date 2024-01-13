from django_project.celery_app import app

import datetime

from .models import CalorieAtePerDay


@app.task
def delete_add_new_calorie_today():
    old_calories = CalorieAtePerDay.objects.filter(destroy_data__lte=datetime.date.today())
    for old_calorie in old_calories:
        calorie_data = old_calorie.calorie_data
        CalorieAtePerDay.objects.create(max_calorie=calorie_data.calorie_per_day, calorie_data=calorie_data)
        old_calorie.delete()
