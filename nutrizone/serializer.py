from rest_framework import serializers
from .models import Nutrient, Food, Measure


class MeasuresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = ("label", "eqv")
        depth = 2

class NutrientSerializer(serializers.ModelSerializer):
    measures = MeasuresSerializer(many=True)
    class Meta:
        model = Nutrient
        fields = ('name','value', 'unit', 'measures')
        depth = 1


class FoodSerializer(serializers.ModelSerializer):
    nutrients = NutrientSerializer(many=True)
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
            measure_data = nutrient.pop('measures')
            nutrientobj = Nutrient.objects.create(food=food, **nutrient)
            for measure in measure_data:
                Measure.objects.create(nutrient=nutrientobj, **measure)
        return food