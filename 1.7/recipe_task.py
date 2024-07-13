from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql.expression import or_

# Database connection
USERNAME = 'cf-python'
PASSWORD = 'password'
HOST = 'localhost'
DATABASE = 'task_database'

# SQLAlchemy Engine: Create the engine to manage the database connection
engine = create_engine(f'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}')

# Base Class: All model classes will inherit from this class
Base = declarative_base()

# Session: Set up the mechanism to interact with the database
# The session will be used to query and commit transactions
Session = sessionmaker(bind=engine)
session = Session()

class Recipe(Base):
    # Table name: Define the table name
    __tablename__ = 'final_recipes'

    # Columns: Define the columns of the table
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        # Representation: Used for debugging purposes, showing a quick string representation of the object
        return f'<Recipe(id={self.id}, name={self.name}, difficulty={self.difficulty})>'

    def __str__(self):
        # String Representation: Formats recipe details in a user-friendly way
        ingredients_list = self.ingredients.split(',')
        formatted_ingredients = '\n'.join(f' - {ingredient.title()}' for ingredient in ingredients_list)
        return (f'Recipe ID: {self.id}\n'
                f' Name: {self.name.title()}\n'
                f' Ingredients:\n {formatted_ingredients}\n'
                f' Cooking Time: {self.cooking_time} minutes\n'
                f' Difficulty: {self.difficulty}\n')

    def return_ingredients_as_list(self):
        # Convert ingredients string to a list
        if not self.ingredients:
            return []
        return self.ingredients.split(',')

    def calculate_difficulty(self):
        # Placeholder for difficulty calculation logic
        if self.cooking_time < 30:
            self.difficulty = 'Easy'
        elif self.cooking_time <= 60:
            self.difficulty = 'Medium'
        else:
            self.difficulty = 'Hard'


# Create Tables: Execute the SQL query to create the table
Base.metadata.create_all(engine)

def create_recipe():
    # Display the header for the create recipe function.
    print()
    print("==================================================")
    print("           *** Create New Recipes ***             ")
    print("==================================================")
    print("Please follow the steps below to add new recipes!\n")

    # Loop to get the number of recipes the user wants to add.
    # Validates that the input is a positive integer.
    while True:
        try:
            num_of_recipes = int(input("How many recipes would you like to enter? "))
            if num_of_recipes < 1:
                print('Please enter a positive number.')
            else:
                break
        except ValueError:
            print('Please enter a valid number.')

    # Loop to get the details of each recipe.
    for i in range(num_of_recipes):
        print(f'\nEnter recipe #{i+1}')
        print('-----------------')

        # Input validation for recipe name, ensuring it's within the character limit.
        while True:
            name = input('Enter the recipe name: ').strip()
            if 0 < len(name) <= 50:
                break
            else:
                print('Please enter a name with at most 50 characters.')

        # Input validation for cooking time, ensuring it's a positive integer.
        while True:
            try:
                cooking_time = int(input('Enter the cooking time (in minutes): '))
                if cooking_time > 0:
                    break
                else:
                    print('Please enter a positive number.')
            except ValueError:
                print('Please enter a valid number.')

        # Input validation for ingredients, ensuring it's within the character limit.
        while True:
            ingredients_input = input('Enter the ingredients (separated by commas): ').strip()
            if ingredients_input:
                break
            else:
                print('Please enter at least one ingredient.')

        # Create a new recipe instance and add it to the session.
        new_recipe = Recipe(name=name, ingredients=ingredients_input, cooking_time=cooking_time)
        new_recipe.calculate_difficulty()

        # Add the new recipe to the session and attempt to commit it to the database.
        session.add(new_recipe)
        try:
            session.commit()
            print(f'\nRecipe "{name}" has been added successfully!')

        except Exception as err:
            # Rollback in case of error during commit.
            session.rollback()
            print(f'An error occurred: {err}')

    # Display a final message after all recipes have been added.
    final_message = 'Recipe successfully added!' if num_of_recipes == 1 else 'All recipes successfully added!'
    print()
    print('--------------------------------------------------')
    print(f'            {final_message}            ')
    print('--------------------------------------------------\n')

    # Pause the execution and wait for the user to press enter.
    pause()

def view_all_recipes():
    # Retrieve all recipes from the database
    recipes = session.query(Recipe).all()

    # Check if there are any recipes in the database.
    if not recipes:
        print('***************************************************************')
        print('         There are no recipes in the database to view.         ')
        print('                 Please create a new recipe!                   ')
        print('***************************************************************\n')
        pause()
        return None

    # Header display for viewing all recipes.
    print('==================================================')
    print('            *** All Available Recipes ***          ')
    print('==================================================')

    # Display the number of recipes found.
    recipe_count = len(recipes)
    recipe_word = 'recipe' if recipe_count == 1 else 'recipes'
    print(f'There are {recipe_count} {recipe_word} in the database.\n')

    # Loop through each recipe and display its details.
    for i, recipe in enumerate(recipes, start=1):
        print(f'Recipe #{i}\n----------')
        print(format_recipe_for_search(recipe))
        print()

    # Footer display for viewing all recipes.
    print('--------------------------------------------------')
    print('          End of Available Recipes List            ')
    print('--------------------------------------------------\n')

    # Pause the execution and wait for the user to press enter.
    pause()

def search_recipe():
    # Retrieve all recipes from the database
    results = session.query(Recipe.ingredients).all()

    # If no recipes are found, display a message and return to the main menu.
    if not results:
        print('***************************************************************')
        print('         There are no recipes in the database to search.        ')
        print('                 Please create a new recipe!                   ')
        print('***************************************************************\n')
        pause()
        return None

    # Initialize a set to store all unique ingredients
    all_ingredients = set()
    for result in results:
        ingredients_list = result[0].split(',')
        for ingredient in ingredients_list:
            all_ingredients.add(ingredient.strip())

    # Print header for search recipe function.
    print()
    print('==================================================')
    print('      *** Search for Recipe By Ingredient ***     ')
    print('==================================================')
    print('Please enter a number to see all recipes that contain the ingredient.\n')

    # Sort and display each unique ingredient with its corresponding number
    sorted_ingredients = sorted(all_ingredients)
    for i, ingredient in enumerate(sorted_ingredients):
        print(f'{i+1}. {ingredient.title()}')

    # Prompt user to enter one or more ingredient numbers, separated by commas
    print()
    while True:
        try:
            choices = input('Enter ingredient numbers (separated by commas): ').strip()
            selected_indices = [int(choice) for choice in choices.split(',')]
            if all(1 <= choice <= len(all_ingredients) for choice in selected_indices):
                break
            else:
                print('Please enter number within the list range.\n')
        except ValueError:
            print('Please enter a valid number.\n')

    # Convert user input into a list of selected ingredients.
    search_ingredients = [sorted_ingredients[index - 1] for index in selected_indices]

    # Build a search query using the selected ingredients.
    search_conditions = [Recipe.ingredients.ilike(f"%{ingredient}%") for ingredient in search_ingredients]
    search_results = session.query(Recipe).filter(or_(*search_conditions)).all()

    # Format the string of selected ingredients for display.
    if len(search_ingredients) > 1:
        selected_ingredients_str = ", ".join(ingredient.title() for ingredient in search_ingredients[:-1])
        selected_ingredients_str += ", or " + search_ingredients[-1].title()
    else:
        selected_ingredients_str = search_ingredients[0].title()

    # Display the search results or an appropriate message if no results are found.
    if search_results:
        print()
        print(f'Here are the recipes that contain {selected_ingredients_str}:\n')
        for recipe in search_results:
            print(f'{format_recipe_for_search(recipe)}\n')
    else:
        print()
        print(f'Sorry, no recipes contain {selected_ingredients_str}.\n')

    pause()

def delete_recipe():
    # Retrieve all recipes from the database
    recipes = session.query(Recipe).all()

    # If no recipes are found, display a message and return to the main menu.
    if not recipes:
        print('***************************************************************')
        print('         There are no recipes in the database to delete.       ')
        print('                 Please create a new recipe!                   ')
        print('***************************************************************\n')
        pause()
        return None

    # Print header for delete recipe function.
    print()
    print('==================================================')
    print('             *** Delete A Recipe ***              ')
    print('==================================================')

    # Display each recipe with its index number.
    for i, recipe in enumerate(recipes, start=1):
        print(f'{i}. {recipe.name.title()}')

    # Prompt the user to select the recipe number to delete.
    print()
    while True:
        try:
            choice = int(input('Enter the recipe number to delete: '))
            if 1 <= choice <= len(recipes):
                recipe_to_delete = recipes[choice - 1]
                break
            else:
                print('Please enter a number within the list range.')
        except ValueError:
            print('Please enter a valid number.')

    # Confirm the deletion action.
    print()
    print(f'Are you sure you want to delete the recipe "{recipe_to_delete.name.title()}"?')
    confirmation = input('Type "yes" to confirm or "no" to cancel: ').strip().lower()

    if confirmation == 'yes':
        # Perform the deletion.
        session.delete(recipe_to_delete)
        try:
            session.commit()
            print(f'\nRecipe "{recipe_to_delete.name.title()}" has been deleted successfully!')
        except Exception as err:
            # Rollback in case of error during commit.
            session.rollback()
            print(f'An error occurred: {err}')
    else:
        print('\nDeletion cancelled.')

    pause()

def pause():
    # Pauses the program until the user presses Enter
    input('Press Enter to continue...')

def format_recipe_for_search(recipe):
    # Formats the recipe details for display in search results
    ingredients_list = recipe.return_ingredients_as_list()
    formatted_ingredients = '\n'.join(f' - {ingredient.title()}' for ingredient in ingredients_list)
    return (f'Recipe ID: {recipe.id}\n'
            f' Name: {recipe.name.title()}\n'
            f' Ingredients:\n {formatted_ingredients}\n'
            f' Cooking Time: {recipe.cooking_time} minutes\n'
            f' Difficulty: {recipe.difficulty}\n')

def main_menu():
    # Main menu for the application.
    while True:
        print()
        print("==================================================")
        print("                Recipe Management                 ")
        print("==================================================")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for a recipe by ingredient")
        print("4. Delete a recipe")
        print("5. Exit")
        print("==================================================")

        # Input validation for the menu choice.
        try:
            choice = int(input("Enter your choice (1-5): "))
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and 5.")
            continue

        if choice == 1:
            create_recipe()
        elif choice == 2:
            view_all_recipes()
        elif choice == 3:
            search_recipe()
        elif choice == 4:
            delete_recipe()
        elif choice == 5:
            print("\nExiting Recipe Management. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main_menu()
