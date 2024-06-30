import pickle

def take_recipe():
    # Taking input from the user
    recipe_name = input("Enter the recipe name: ")
    cooking_time = int(input("Enter the cooking time in minutes: "))
    ingredients = input("Enter the ingredients (comma-separated): ").split(',')

    # Calculating the difficulty
    difficulty = calc_difficulty(cooking_time, ingredients)

    # Gathering all attributes into a dictionary
    recipe = {
        'name': recipe_name,
        'cooking_time': cooking_time,
        'ingredients': ingredients,
        'difficulty': difficulty
    }
    
    return recipe

def calc_difficulty(cooking_time, ingredients):
    num_ingredients = len(ingredients)

    if cooking_time < 10 and num_ingredients < 4:
        difficulty = 'Easy'
    elif cooking_time < 10 and num_ingredients >= 4:
        difficulty = 'Medium'
    elif cooking_time >= 10 and num_ingredients < 4:
        difficulty = 'Intermediate'
    else:
        difficulty = 'Hard'
    
    return difficulty

# Have the user enter the name of the file
filename = input("Enter the name of the file: ")

#Try to open the file, if it doesn't exist, create it
try:
    file = open(filename, 'rb')
    data = pickle.load(file)
    print('File loaded successfully')
#This is the error that will be raised if the file doesn't exist
except FileNotFoundError:
    print('File not found, creating a new one')
    data = {'recipes_list': [], 'all_ingredients': []}
#This is a general error that will be raised if something else goes wrong
except:
    print('An error occurred while trying to open the file')
    data = {'recipes_list': [], 'all_ingredients': []}
#This will close the file
else:
    file.close()
#Extracts the data into two variables
finally:
    recipes_list = data['recipes_list']
    all_ingredients = data['all_ingredients']

#Asks the user how many recipes they want to add
n = int(input('How many recipes do you want to add? '))

#For each recipe, it will add the ingredients to the all_ingredients list
for i in range(0, n):
    recipe = take_recipe()
    for element in recipe['ingredients']:
        if element not in all_ingredients:
            all_ingredients.append(element)
    recipes_list.append(recipe)
    print('Recipe added successfully')

#Creates a new dictionary with the updated data
data = {'recipes_list': recipes_list, 'all_ingredients': all_ingredients}

#Opens the file and writes the data to it
updated_file = open(filename, 'wb')
pickle.dump(data, updated_file)

#Closes the file
updated_file.close()
print('Data saved successfully')
