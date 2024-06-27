# Empty lists for recipes and ingredients
recipes_list = []
ingredients_list = []

# Function to add a recipe
def take_recipe():
    name = input('Enter the name of the recipe: ')
    cooking_time = int(input('Enter the cooking time in minutes: '))
    ingredients = input('Enter the ingredients separated by commas: ').split(', ')
    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients
      }
    
    return recipe

# Function to add an ingredient
n = int(input('How many recipes would you like to enter? '))

# Iterating through the number of recipes
for i in range(n):
    recipe = take_recipe()

    # Checks wether an ingredient is already in the list
    for ingredient in recipe['ingredients']:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)

    recipes_list.append(recipe)

# Iterating through recipes_list to determine recipe difficulty
for recipe in recipes_list:
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Easy'
    elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'Medium'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Intermediate'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'Hard'

# Iterating through recipes_list to print the recipes
for recipe in recipes_list:
    print('Recipe:', recipe['name'])
    print('Cooking time (minutes):', recipe['cooking_time'])
    print('Ingredients:')
    for ingredient in recipe['ingredients']:
        print(ingredient)
    print('Difficulty:', recipe['difficulty'])

# Printing the ingredients list
def all_ingredients():
    print('All ingredients:')
    print('----------------')
    for ingredient in ingredients_list:
        print(ingredient)

all_ingredients()
