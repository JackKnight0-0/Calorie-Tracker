from django import forms
from .models import UserCalorieData, Food


class UserCalorieDataForm(forms.ModelForm):
    class Meta:
        model = UserCalorieData
        fields = ('gender', 'age', 'height', 'weight', 'physical_activity')
        widgets = {
            'gender': forms.Select(choices=UserCalorieData.GenderChoose,
                                   attrs={'class': 'form-control'}),
            'age': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'height': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Height'}),
            'weight': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Weight'}),
            'physical_activity': forms.Select(choices=UserCalorieData.PhysicalActivityChoose,
                                              attrs={'class': 'form-control'})
        }


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = (
            'food',
            'calories',
        )

        widgets = {
            'food': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of food'}),
            'calories': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Calorie in food'}),
        }
