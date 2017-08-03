from django.db import models

# Create your models here.

class Food(models.Model):
	name = models.CharField(max_length=100)
	brname = models.CharField(max_length=100, default="")
	ndbno = models.IntegerField()
	altmeasurename = models.CharField(max_length=100, default="")
	altmeasuregram = models.FloatField(default=0)
	def __str__(self):
		return self.name

class Nutrient(models.Model):
	name = models.CharField(max_length=200)
	value = models.FloatField()
	unit = models.CharField(max_length=10)
	food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='foodname')
	def __str__(self):
		return self.name + ' - ' + self.food.name

class Measure(models.Model):
	label = models.CharField(max_length=200)
	eqv = models.FloatField()
	nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE, related_name='nutrientname')
	def __str__(self):
		return self.label + ' - ' + self.nutrient.name + ' - ' + self.nutrient.food.name
