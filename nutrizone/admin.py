from django.contrib import admin

from .models import Food, Nutrient, Measure, UserMeal, MealIngredient
# Register your models here.

admin.site.register(Food)
admin.site.register(Nutrient)
admin.site.register(Measure)
admin.site.register(UserMeal)
admin.site.register(MealIngredient)