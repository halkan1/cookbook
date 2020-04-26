from app import app, db
from app.models import (User, Recipe, RecipeStep, RecipeSection, 
                       RecipeIngredient, MeasurementQty, MeasurementUnit, 
                       Ingredient, IngredientType)

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Recipe': Recipe,
        'RecipeStep': RecipeStep,
        'RecipeSection': RecipeSection,
        'RecipeIngredient': RecipeIngredient,
        'MeasurementQty': MeasurementQty,
        'MeasurementUnit': MeasurementUnit, 
        'Ingredient': Ingredient,
        'IngredientType': IngredientType
    }