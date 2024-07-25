from django.test import TestCase
from .models import Recipe

class RecipeModelTest(TestCase):

    def setUp(self):
        # Set up some initial data for tests
        self.recipe_easy = Recipe.objects.create(
            name="Easy Recipe",
            ingredients="ingredient1,ingredient2",
            cooking_time=5
        )
        self.recipe_medium = Recipe.objects.create(
            name="Medium Recipe",
            ingredients="ingredient1,ingredient2,ingredient3,ingredient4",
            cooking_time=5
        )
        self.recipe_intermediate = Recipe.objects.create(
            name="Intermediate Recipe",
            ingredients="ingredient1,ingredient2",
            cooking_time=15
        )
        self.recipe_hard = Recipe.objects.create(
            name="Hard Recipe",
            ingredients="ingredient1,ingredient2,ingredient3,ingredient4",
            cooking_time=15
        )

    def test_easy_difficulty(self):
        self.recipe_easy.calc_difficulty()
        self.assertEqual(self.recipe_easy.difficulty, 'Easy')

    def test_medium_difficulty(self):
        self.recipe_medium.calc_difficulty()
        self.assertEqual(self.recipe_medium.difficulty, 'Medium')

    def test_intermediate_difficulty(self):
        self.recipe_intermediate.calc_difficulty()
        self.assertEqual(self.recipe_intermediate.difficulty, 'Intermediate')

    def test_hard_difficulty(self):
        self.recipe_hard.calc_difficulty()
        self.assertEqual(self.recipe_hard.difficulty, 'Hard')

    def test_string_representation(self):
        self.assertEqual(str(self.recipe_easy), "Easy Recipe")
