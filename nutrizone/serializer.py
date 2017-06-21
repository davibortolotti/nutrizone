from rest_framework import serializers
from .models import Nutrients, Food

class NutrientsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Nutrients
		fields = ('name','value', 'unit')
		depth = 1


class FoodSerializer(serializers.ModelSerializer):
    nutrients = NutrientsSerializer(many=True)
    class Meta:
        model = Food
        fields = ('name','nutrients', 'ndbno')

class ReportSerializer(serializers.Serializer):
	food = FoodSerializer()

class USDASerializer(serializers.Serializer):
	report = ReportSerializer()
	def create(self, validated_data):

		report_data = validated_data.pop('report')
		food_data = report_data.pop('food')	
		nutrient_data = food_data.pop('nutrients')

		food = Food.objects.create(**food_data)

		for nutrient in nutrient_data:
			Nutrients.objects.create(food=food, **nutrient)
		
		return food