from .models import Food, Nutrient


def food_info(foodname):

    context = {}

    food = Food.objects.filter(brname=foodname)[0] # TEMPORARIO
    nutrients = Nutrient.objects.filter(food__brname=foodname)

    energy = nutrients.get(name='Energy')
    fat = nutrients.get(name='Total lipid (fat)')
    if nutrients.filter(name='Sugars, total').exists():
        sugars = nutrients.get(name='Sugars, total')
        context['sugars'] = sugars

    context.update({
        'food': food, 
        'energy': energy,
        'fat':fat,
    })

    return context, energy, fat, sugars 