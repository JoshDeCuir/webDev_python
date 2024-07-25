from django.db import models

# Create your models here.
class Recipe(models.Model):
    # class attributes
    name = models.CharField(max_length=35)
    ingredients = models.CharField(
        max_length=255,
        help_text='Enter the ingredients separated by commas'
    )
    cooking_time = models.FloatField(help_text='Enter the cooking time in minutes')
    difficulty = models.CharField(max_length=15, blank=True, null=True)

    # Determines recipe difficulty based on cooking time
    def calc_difficulty(self):
        ingredients = self.ingredients.split(',')

        if self.cooking_time < 10 and len(ingredients) < 4:
            self.difficulty = 'Easy'
        elif self.cooking_time < 10 and len(ingredients) >= 4:
            self.difficulty = 'Medium'
        elif self.cooking_time >= 10 and len(ingredients) < 4:
            self.difficulty = 'Intermediate'
        else:
            self.difficulty = 'Hard'

    # String representation
    def __str__(self):
        return self.name
