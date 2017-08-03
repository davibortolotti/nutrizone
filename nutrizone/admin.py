from django.contrib import admin

from .models import Food, Nutrient, Measure
# Register your models here.

admin.site.register(Food)
admin.site.register(Nutrient)
admin.site.register(Measure)