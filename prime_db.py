from app import app, db
from app.models import (Ingredient, MeasurementUnit, MeasurementQty, Tag, User,
                        Recipe, IngredientSet, RecipeStep)

user = User(username='jonas', email='jonas.example.com')
user.set_password('supersecret')
db.session.add(user)

for i in range(1, 1001):
    db.session.add(MeasurementQty(quantity=i))

setup_ingredients = [
    'vitlöksklyftor',
    'gul lök',
    'färsk rosmarin',
    'bacon',
    'olivolja',
    'köttfärs',
    'rött vin',
    'krossade tomater',
    'parmesan'
]

for i in setup_ingredients:
    db.session.add(Ingredient(name=i))

uom = [
    ['ml', 'milliliter', 'volume', 1],
    ['cl', 'centiliter', 'volume', 10],
    ['dl', 'deciliter', 'volume', 100],
    ['l', 'liter', 'volume', 1000],
    ['krm', 'kryddmått', 'volume', 1],
    ['tsk', 'tesked', 'volume', 5],
    ['msk', 'matsked', 'volume', 15],
    ['g', 'gram', 'weight', 1],
    ['hg', 'hektogram', 'weight', 100],
    ['kg', 'kilogram', 'weight', 1000],
    ['st', 'stycken', 'other', 1],
]

for entry in uom:
    db.session.add(
        MeasurementUnit(
            shortform=entry[0],
            fullform=entry[1],
            dimension=entry[2],
            factor=entry[3]
        )
    )

tags = [
    'nötkött',
    'fisk',
    'lamm',
    'vegetariskt',
    'indiskt',
    'italienskt'
]

for i in tags:
    db.session.add(Tag(name=i))

db.session.add(Recipe(
    name='pasta bolognese', 
    description='a great and simple family meal', 
    servings=4, 
    source='https://www.jamieoliver.com/recipes/beef-recipes/spaghetti-bolognese/')
)

bolognese_set = [
    (2,'st','vitlöksklyftor'),
    (1,'st','gul lök'),
    (1,'st','färsk rosmarin'),
    (6,'st','bacon'),
    (6,'ml','olivolja'),
    (500,'g','köttfärs'),
    (2,'dl','rött vin'),
    (400,'g','krossade tomater')
]

for i in bolognese_set:
    IngredientSet.add_set(quantity=float(i[0]), unit=i[1], ingredient=i[2])

recipe = Recipe.query.filter_by(name='pasta bolognese').first()

for i in IngredientSet.query.all():
    recipe.add_ingredient(i)

db.session.add(recipe)

db.session.add(RecipeStep(
    step_number=1,
    step_text="Preheat the oven to 180ºC/350ºF/gas 4."))
db.session.add(RecipeStep(
    step_number=2,
    step_text="Peel and finely chop the garlic and onions, pick and finely chop the rosemary, then finely slice the bacon."))
db.session.add(RecipeStep(
    step_number=3,
    step_text="Heat a splash of oil in a casserole pan on a medium heat, add the bacon, rosemary, garlic and onion and cook for 5 minutes, or until softened, stirring occasionally."))
db.session.add(RecipeStep(
    step_number=4,
    step_text="Add the minced beef, breaking it apart with the back of a spoon, then cook for 2 to 3 minutes, or until starting to brown, then pour in the wine. Leave to bubble and cook away."))
db.session.add(RecipeStep(
    step_number=5,
    step_text="Meanwhile, drain and tip the sun-dried tomatoes into a food processor, blitz to a paste, then add to the pan with the tomatoes. Stir well, break the plum tomatoes apart a little."))
db.session.add(RecipeStep(
    step_number=6,
    step_text="Cover with a lid then place in the oven for 1 hour, removing the lid and giving it a stir after 30 minutes – if it looks a little dry at this stage, add a splash of water to help it along."))
db.session.add(RecipeStep(
    step_number=7,
    step_text="About 10 minutes before the time is up, cook the spaghetti in boiling salted water according to the packet instructions."))
db.session.add(RecipeStep(
    step_number=8,
    step_text="Once the spaghetti is cooked, drain, reserving a mugful of cooking water, then return to the pan with a few spoons of Bolognese, a good grating of Parmesan and a drizzle of extra virgin olive oil."))
db.session.add(RecipeStep(
    step_number=9,
    step_text="Toss to coat the spaghetti, loosening with a splash of cooking water, if needed."))
db.session.add(RecipeStep(
    step_number=10,
    step_text="Divide the spaghetti between plates or bowls, add a good spoonful of Bolognese to each, then serve with a fine grating of Parmesan."))

for i in RecipeStep.query.all():
    recipe.steps.append(i)

db.session.commit()