import pickle

#Function to display the recipes
def display_recipe(recipe):
  print('')
  print('Recipe name:', recipe['name'])
  print('Cooking time:', recipe['cooking_time'])
  print('Ingredients:')
  for element in recipe['ingredients']:
    print('--   ', element)
  print('Difficulty:', recipe['difficulty'])
  print('')

#Function to search ingredients
def search_ingredients(data):
    #Adds number to each element in the list
    available_ingredients = enumerate(data['all_ingredients'])
    #Put enumerated data into the list
    numbered_list = list(available_ingredients)
    print('Ingredients List:')

    for element in numbered_list:
      print(element[0], element[1])
    try:
      num = int(input('Enter the number of the ingredient you want to search: '))
      ingredient_searched = numbered_list[num][1]
      print('Searching for recipes with', ingredient_searched, '.....')
    except ValueError:
      print('Only numbers are allowed')
    except IndexError:
      print('Your input does not match any ingredient. Make sure you enter the number of the ingredient')
    else:
      for element in data['recipes_list']:
        if ingredient_searched in element['ingredients']:
          print(element)

filename = input('Enter the name of the file you want to save to: ')

try:
  file = open(filename, 'rb')
  data = pickle.load(file)
  print('File loaded successfully')
except FileNotFoundError:
  print('No files match that name - please try again')
except:
  print('An error occurred while trying to open the file')
else:
  file.close()
  search_ingredients(data)
