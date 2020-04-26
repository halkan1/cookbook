from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    recipies = db.relationship('Recipe', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    steps = db.relationship('RecipeStep', backref='recipe', lazy='dynamic')
    ingredients = db.relationship('RecipeIngredient', backref='recipe', lazy='dynamic')

    def __repr__(self):
        return f'<Recipe {self.name}, {self.description}>'

class RecipeStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step_no = db.Column(db.Integer)
    step_text = db.Column(db.String(64))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    def __repr__(self):
        return f'<{self.step_no}: {self.step_text}>'

class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measurement_qty_id = db.relationship('MeasurementQty', backref='quantity', lazy='dynamic')
    measurement_unit_id = db.relationship('MeasurementUnit', backref='unit', lazy='dynamic')
    ingredient_id = db.relationship('Ingredient', backref='ingredient', lazy='dynamic')
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    def __repr__(self):
        return f'<{self.measurement_qty_id} {self.measurement_unit_id} {self.ingredient_id}>'

class MeasurementQty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    m_quantity = db.Column(db.Integer, unique=True)
    recipe_ingredients_id = db.Column(db.Integer, db.ForeignKey('recipe_ingredient.id'))

    def __repr__(self):
        return f'<{self.m_quantity}>'

class MeasurementUnit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit_short = db.Column(db.String(8), unique=True)
    unit_long = db.Column(db.String(16), unique=True)
    recipe_ingredients_id = db.Column(db.Integer, db.ForeignKey('recipe_ingredient.id'))

    def __repr__(self):
        return f'<Short form: {self.unit_short}, Long form: {self.unit_long}>'

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    ingredient_type_id = db.relationship('IngredientType', backref='type', lazy='dynamic')
    recipe_ingredients_id = db.Column(db.Integer, db.ForeignKey('recipe_ingredient.id'))

    def __repr__(self):
        return f'<Ingredient: {self.name}, Type: {self.ingredient_type_id}>'

class IngredientType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ing_type = db.Column(db.String(32), unique=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'))

    def __repr__(self):
        return f'<Type: {self.ing_type}>'