import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    password='password',
)

cursor = conn.cursor()

cursor.execute('CREATE DATABASE IF NOT EXISTS task_database')

cursor.execute('USE task_database')

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
               id INT AUTO_INCREMENT PRIMARY KEY,
               name VARCHAR(50),
               ingredients VARCHAR(255),
               cooking_time INT,
               difficulty VARCHAR(20)
)''')

def main_menu(conn, cursor):
    choice = ''
    while(choice != 'quit'):
        
        print("  _____           _                                   ")
        print(" |  __ \         (_)                /\                ")
        print(" | |__) |___  ___ _ _ __   ___     /  \   _ __  _ __  ")
        print(" |  _  // _ \/ __| | '_ \ / _ \   / /\ \ | '_ \| '_ \ ")
        print(" | | \ \  __/ (__| | |_) |  __/  / ____ \| |_) | |_) |")
        print(" |_|  \_\___|\___|_| .__/ \___| /_/    \_\ .__/| .__/ ")
        print("                   | |                   | |   | |    ")
        print("                   |_|                   |_|   |_|    ")
        print("======================================================")
        print("   What would you like to do? Pick a choice below!    ")
        print("======================================================\n")
        print("1. Create a new recipe")
        print("2. Search for recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe\n")
        print("Type 'quit' to exit the program\n")
        choice = input("Your choice: ").strip().lower()
        print()

        if choice in ['1', '2', '3', '4']:
            if choice == '1':
                create_recipe(conn, cursor)
            elif choice == '2':
                search_recipe(conn, cursor)
            elif choice == '3':
                update_recipe(conn, cursor)
            elif choice == '4':
                delete_recipe(conn, cursor)
        elif choice == 'quit':
            print('========================================')
            print('  Thank you for using the recipe app!   ')
            print('========================================')
            break
        else:
            print('--------------------------------------------------')
            print("Invalid choice! Please enter 1, 2, 3, 4 or 'quit'.")
            print('--------------------------------------------------\n')
            print('... returning to main menu ...\n')

    conn.close()

def create_recipe(conn, cursor):
    print()
    print('------------------------------------')
    print('  Creating a new recipe...')
    print('------------------------------------\n')
    print('Please follow the instructions below to create a new recipe.\n')

    while True:
        try:
            number_of_recipes = int(input('How many recipes would you like to create? '))
            if number_of_recipes < 1:
                print('Please enter a number greater than 0.')
            else:
                break
        except ValueError:
            print('Please enter a valid number.\n')

    for i in range(number_of_recipes):
        print(f'\nEnter recipe #{i+1}')
        print('-------------------')

        name = input('Enter the recipe name:')
        cooking_time = int(input('Enter the cooking time (in minutes):'))
        ingredients = input('Enter the ingredients (separated by commas):')
        ingredients = ingredients.split(',')

        difficulty = calculate_difficulty(cooking_time, ingredients)
        ingredients_str = ', '.join(ingredients)

        try:
            insert_query = 'INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)'
            cursor.execute(insert_query, (name, ingredients_str, cooking_time, difficulty))
            conn.commit()

            print('Recipe added successfully!\n')
        except mysql.connector.Error as err:
            print('Error adding recipe:', err)

    final_message = 'Recipe(s) added successfully!' if number_of_recipes == 1 else 'Recipe added successfully!'

    print()
    print('------------------------------------')
    print(f'  {final_message}')
    print('------------------------------------\n')
    print('... returning to main menu ...\n')

def calculate_difficulty(cooking_time, ingredients):
    num_ingredients = len(ingredients)
    if cooking_time < 10 and num_ingredients < 4:
        return 'Easy'
    elif cooking_time < 10 and num_ingredients >= 4:
        return 'Medium'
    elif cooking_time >= 10 and num_ingredients < 4:
        return 'Intermediate'
    elif cooking_time >= 10 and num_ingredients >= 4:
        return 'Hard'
    
def format_recipe_display(recipe):
    print(f'\nRecipe: {recipe[1].title()}')
    print(f'Time: {recipe[3]} minutes')
    print('Ingredients:')
    for ingredient in recipe[2].split(','):
        print(f' - {ingredient.title()}')
    print(f'Difficulty: {recipe[4]}')

def search_recipe(conn, cursor):
    cursor.execute('SELECT ingredients FROM Recipes')
    results = cursor.fetchall()

    if not results:
        print('No recipes found. Please create a recipe first.\n')
        print('... returning to main menu ...\n')
        return
    
    all_ingredients = set()

    print('-------------------------------------------')
    print('  Searching for recipes by Ingredients...')
    print('-------------------------------------------\n')
    print('Please enter a number to see all recipes that use that ingredient.\n')

    for result in results:
        ingretdients_list = result[0].split(',')
        for ingredient in ingretdients_list:
            all_ingredients.add(ingredient.strip())

    for i, ingredient in enumerate(sorted(all_ingredients)):
        print(f'{i+1}. {ingredient.title()}')

    print()
    while True:
        try:
            choice = int(input('Enter the number of ingredient:'))
            if 1 <= choice <= len(all_ingredients):
                break
            else:
                print()
                print('Please enter a number within the list range.\n')
        except ValueError:
            print()
            print('Invalid input. Please enter a valid number.\n')

    selected_ingredient = sorted(all_ingredients)[choice-1]

    search_query = 'SELECT * FROM Recipes WHERE ingredients LIKE %s'
    cursor.execute(search_query, ('%' + selected_ingredient + '%',))
    search_results = cursor.fetchall()

    if search_results:
        recipe_count = len(search_results)
        recipe_word = 'recipe' if recipe_count == 1 else 'recipes'
        print(f'\n{recipe_count} {recipe_word} found using {selected_ingredient.title()}:\n')
        for recipe in search_results:
            format_recipe_display(recipe)

        print()
        print('-------------------------------------------')
        print(' Recipe search completed successfully!')
        print('-------------------------------------------\n')
        print('... returning to main menu ...\n')
    else:
        print(f'\nNo recipes found using {selected_ingredient.title()}.\n')

    print('\n')

def update_recipe(conn, cursor):
    cursor.execute('SELECT * FROM Recipes')
    results = cursor.fetchall()

    if not results:
        print('------------------------------------------------')
        print(' There are no recipes in the database to update.')
        print('         Please create a recipe first.          ')
        print('------------------------------------------------\n')
        print('... returning to main menu ...\n')
        return
    
    print()
    print('------------------------------------')
    print(' Updating a Recipe By ID Number...')
    print('------------------------------------\n')
    print('Please enter an ID number to update that recipe.\n')


    print('----- Available Recipes -----')
    for result in results:
        ingredients_list = result[2].split(',')
        capitalized_ingredients = [ingredient.title() for ingredient in ingredients_list]
        capitalized_ingredients_str = ', '.join(capitalized_ingredients)

        print(f'ID: {result[0]} | Name: {result[1]}')
        print(f'Ingredients: {capitalized_ingredients_str} | Cooking Time: {result[3]} minutes | Difficulty: {result[4]}')

    while True:
        try:
            print()
            recipe_id = int(input('Enter the ID number of the recipe to update: '))
            print()

            cursor.execute('SELECT COUNT(*) FROM Recipes WHERE id = %s', (recipe_id,))
            if cursor.fetchone()[0] == 0:
                print('No recipe found with the entered ID. Please try again.\n')
            else:
                break
        except ValueError:
            print()
            print('Invalid input. Please enter a valid number.\n')

    selected_recipe = next((result for result in results if result[0] == recipe_id), None)
    if selected_recipe:
        print(f"Which field would you like to update for '{selected_recipe[1]}'?")
    else:
        print('Recipe not found.')
        return
    print('- Name')
    print('- Cooking Time')
    print('- Ingredients\n')

    update_field = input('Enter your choice: ').lower()
    print()

    if update_field == 'cooking time':
        update_field = 'cooking_time'

    if update_field not in ['name', 'cooking_time', 'ingredients']:
        print("Invalid field. Please enter 'name', 'cooking time', or 'ingredients'.\n")
        return
    
    if update_field == 'cooking_time' or update_field == 'cooking time':
        while True:
            try:
                new_value = int(input('Enter the new cooking time (in minutes): '))
                break
            except ValueError:
                print('Invalid input. Please enter a valid number.\n')
    else:
        new_value = input(f'Enter the new {update_field}: ')

    update_query = f'UPDATE Recipes SET {update_field} = %s WHERE id = %s'
    cursor.execute(update_query, (new_value, recipe_id))

    if update_field in ['cooking_time', 'ingredients']:
        cursor.execute('SELECT cooking_time, ingredients FROM Recipes WHERE id = %s', (recipe_id,))
        updated_recipe = cursor.fetchone()
        new_difficulty = calculate_difficulty(updated_recipe[0], updated_recipe[1].split(','))

        cursor.execute('UPDATE Recipes SET difficulty = %s WHERE id = %s', (new_difficulty, recipe_id))

    conn.commit()

    print()
    print('------------------------------------')
    print('  Recipe Updated Successfully!')
    print('------------------------------------\n')
    print('... returning to main menu ...\n')

def delete_recipe(conn, cursor):
    cursor.execute('SELECT * FROM Recipes')
    results = cursor.fetchall()

    if not results:
        print('------------------------------------------------')
        print(' There are no recipes in the database to delete.')
        print('         Please create a recipe first.          ')
        print('------------------------------------------------\n')
        print('... returning to main menu ...\n')
        return
    
    print()
    print('------------------------------------')
    print(' Deleting a Recipe By ID Number...')
    print('------------------------------------\n')
    print('Please enter an ID number of the recipe to remove.\n')
    print('*Warning: This action cannot be undone.\n')

    print('----- Available Recipes -----')
    for result in results:
        ingredients_list = result[2].split(',')
        capitalized_ingredients = [ingredient.title() for ingredient in ingredients_list]
        capitalized_ingredients_str = ', '.join(capitalized_ingredients)

        print(f'ID: {result[0]} | Name: {result[1]}')
        print(f'Ingredients: {capitalized_ingredients_str} | Cooking Time: {result[3]} minutes | Difficulty: {result[4]}')

    while True:
        try:
            recipe_id = int(input('Enter the ID of the recipe to delete: '))
            print()

            cursor.execute('SELECT COUNT(*) FROM Recipes WHERE id = %s', (recipe_id,))
            if cursor.fetchone()[0] == 0:
                print('No recipe found with the entered ID. Please try again.\n')
            else:
                
                cursor.execute('SELECT name FROM Recipes WHERE id = %s', (recipe_id,))
                recipe_name = cursor.fetchone()[0]
                confirm = input(f'Are you sure you want to delete the recipe "{recipe_name}"? (yes/no): ').lower()

                if confirm == 'yes':
                    break
                elif confirm == 'no':
                    print()
                    print('Deletion cancelled. Returning to main menu...\n')
                    return
                else:
                    print()
                    print("Invalid input. Please enter 'yes' or 'no'.\n")

        except ValueError:
            print()
            print('Invalid input. Please enter a valid number.\n')

    cursor.execute('DELETE FROM Recipes WHERE id = %s', (recipe_id,))

    conn.commit()

    print()
    print('------------------------------------')
    print('  Recipe Deleted Successfully!')
    print('------------------------------------\n')
    print('... returning to main menu ...\n')

# Start the main menu
main_menu(conn, cursor)
