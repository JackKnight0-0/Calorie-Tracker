from django.urls import path
from .views import CalorieSetUpView, ShowChangeTheCalorieData, MyDailyCalorieView, FoodDeleteView

urlpatterns = [
    path('setup-calorie-data/', CalorieSetUpView.as_view(), name='setup_calorie_data'),
    path('my-calorie-data/', ShowChangeTheCalorieData.as_view(), name='show_change_calorie_data'),
    path('daily-calorie/', MyDailyCalorieView.as_view(), name='daily_calorie'),
    path('delete/food/<int:food_pk>/', FoodDeleteView.as_view(), name='delete_food'),

]
