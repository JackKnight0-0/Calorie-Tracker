from django.views import View
from django.views.generic import FormView
from django.shortcuts import reverse, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserCalorieDataForm, FoodForm
from .models import CalorieAtePerDay, Food, UserCalorieData


class CalorieSetUpView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = UserCalorieDataForm
    template_name = 'calorie_tracker/setup_data.html'

    def get_success_url(self):
        return redirect(reverse('profile', kwargs={'slug': self.request.user.user_profile.slug}))

    def form_valid(self, form):
        form = form.save(commit=False)
        form.user = self.request.user
        form.save()
        return self.get_success_url()

    def test_func(self):
        try:
            UserCalorieData.objects.get(user=self.request.user)
        except UserCalorieData.DoesNotExist:
            return True
        return False


class ShowChangeTheCalorieData(LoginRequiredMixin, FormView):
    template_name = 'calorie_tracker/show_change_calorie.html'

    def get_context_data(self, **kwargs):
        context = dict()
        context['form'] = UserCalorieDataForm(instance=self.request.user.calorie_data)
        return context

    def get_success_url(self):
        return redirect(reverse('profile', kwargs={'slug': self.request.user.user_profile.slug}))

    def post(self, request, *args, **kwargs):
        form = UserCalorieDataForm(self.request.POST, instance=self.request.user.calorie_data)
        if form.is_valid():
            form.save()
            return self.get_success_url()

        return self.render_to_response(context={'form': form})


class MyDailyCalorieView(LoginRequiredMixin, FormView):
    template_name = 'calorie_tracker/daily_calorie.html'
    form_class = FoodForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calorie_data = self.request.user.calorie_data
        context['calorie_data'] = calorie_data
        context['today_calories'] = calorie_data.calorie_history.first()
        return context

    def form_valid(self, form):
        form = form.save(commit=False)
        calorie_data = self.request.user.calorie_data
        calorie_today = calorie_data.calorie_history.first()
        form.calorie_today = calorie_today  # making relationship between CalorieAtePerDay and Food
        form.save()
        calorie_today.current_calorie += form.calories  # changing today calorie data
        calorie_today.save()
        return redirect(reverse('daily_calorie'))


class FoodDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, food_pk, *args, **kwargs):
        food = get_object_or_404(Food, pk=food_pk)
        calorie_today = get_object_or_404(CalorieAtePerDay, foods=food)
        calorie_today.current_calorie -= food.calories  # minus the calorie from food and CalorieAtePerDay
        calorie_today.save()
        food.delete()
        return redirect(self.request.META.get('HTTP_REFERER', 'home'))

    def test_func(self):
        pk = self.kwargs.get('food_pk', None)
        food = get_object_or_404(Food, pk=pk)
        return food.calorie_today.calorie_data.user == self.request.user
