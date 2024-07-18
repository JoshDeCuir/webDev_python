# Class Definition: Recipe

class Recipe:
    # Class variable to store all unique ingredients from all recipes
    all_ingredients = set()

    def __init__(self, name, cooking_time):
        # Initialization method with name and cooking time
        self.name = name
        self.cooking_time = cooking_time
        self.ingredients = []
        self.difficulty = None

    def add_ingredients(self, *args):
        # Method to add ingredients to the recipe
        for ingredient in args:
            self.ingredients.append(ingredient)
        self.update_all_ingredients()

    def update_all_ingredients(self):
        # Method to update the class variable all_ingredients
        for ingredient in self.ingredients:
            Recipe.all_ingredients.add(ingredient)

    def calculate_difficulty(self):
        # Method to calculate the difficulty of the recipe
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"

    def get_name(self):
        # Method to get the name of the recipe
        return self.name

    def set_name(self, name):
        # Method to set the name of the recipe
        self.name = name

    def get_cooking_time(self):
        # Method to get the cooking time of the recipe
        return self.cooking_time

    def set_cooking_time(self, cooking_time):
        # Setter for the cooking time of the recipe
        self.cooking_time = cooking_time 
    
    def get_ingredients(self):
        # Getter for the ingredients of the recipe
        return self.ingredients
    
    def get_difficulty(self):
        # Getter for the difficulty, calculates it if not already calculated
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty
    
    def search_ingredient(self, ingredient):
        # Method to search for an ingredient in the recipe
        return ingredient in self.ingredients
    
    def __str__(self):
        # String representation of the recipe
        self.calculate_difficulty()
        return f'Recipe Name: {self.name}\nIngredients: {", ".join(self.ingredients)}\nCooking Time: {self.cooking_time} minutes\nDifficulty: {self.get_difficulty()}'
    
# Function recipe_search

def recipe_search(data, search_term):
    # Search for recipes containing a specific ingredient
    for recipe in data:
        if recipe.search_ingredient(search_term):
            print(recipe)

# Main Code

# Creating instances of the Recipe class and adding ingredients
tea = Recipe('Tea', 5)
tea.add_ingredients('Water', 'Tea Leaves', 'Sugar')
print(tea)

coffee = Recipe('Coffee', 5)
coffee.add_ingredients('Water', 'Coffee Powder', 'Sugar')
print(coffee)

cake = Recipe('Cake', 50)
cake.add_ingredients('Flour', 'Sugar', 'Butter', 'Eggs', 'Baking Powder', 'Vanilla Essence', 'Milk')
print(cake)

banana_smoothie = Recipe('Banana Smoothie', 5)
banana_smoothie.add_ingredients('Banana', 'Milk', 'Sugar', 'Ice', 'Peanut Butter')
print(banana_smoothie)

# Creating a list of all recipes
recipes_list = [tea, coffee, cake, banana_smoothie]

# Using recipe_search function to find recipes containing specific ingredients
print('\nRecipes containing Water:')
recipe_search(recipes_list, 'Water')

print('\nRecipes containing Sugar:')
recipe_search(recipes_list, 'Sugar')

print('\nRecipes containing Banana:')
recipe_search(recipes_list, 'Banana')
