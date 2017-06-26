from django.db import models

# Create your models here.

class Food(models.Model):
	name = models.CharField(max_length=100)
	ndbno = models.IntegerField()
	def __str__(self):
		return self.name

class Nutrients(models.Model):
	name = models.CharField(max_length=200)
	value = models.FloatField()
	unit = models.CharField(max_length=10)
	food = models.ForeignKey(Food, related_name='food')
	def __str__(self):
		return self.name + ' - ' + self.food.name


