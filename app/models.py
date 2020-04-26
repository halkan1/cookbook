from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #recipies = db.relationship('Recipe', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(128))
    servings = db.Column(db.Integer)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sections = db.relationship('RecipeSection', backref='sections', lazy='dynamic')
    steps = db.relationship('RecipeStep', backref='steps', lazy='dynamic')
    comments = db.Column(db.String(512))
    source = db.Column(db.String(128))

    def __repr__(self):
        return f'{self.name}'

class RecipeStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step_number = db.Column(db.Integer)
    step_text = db.Column(db.String(64))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    def __repr__(self):
        return f'{self.step_number}. {self.step_text}'

class RecipeSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), default='Default')
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    ingredients = db.relationship('RecipeIngredient', backref='ingredients', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}'

class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measurement_qty_id = db.Column(db.Integer, db.ForeignKey('measurement_qty.id'))
    measurement_unit_id = db.Column(db.Integer, db.ForeignKey('measurement_unit.id'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'))
    recipe_section_id = db.Column(db.Integer, db.ForeignKey('recipe_section.id'))

    def __repr__(self):
        return f'{self.quantity} {self.unit} {self.ingredient}'

class MeasurementQty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, unique=True)
    recipe_ingredient_id = db.relationship('RecipeIngredient', backref='quantity', lazy='dynamic')

    def __repr__(self):
        return f'{self.quantity}'

class MeasurementUnit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shortform = db.Column(db.String(8), unique=True)
    fullform = db.Column(db.String(16), unique=True)
    recipe_ingredient_id = db.relationship('RecipeIngredient', backref='unit', lazy='dynamic')

    def __repr__(self):
        return f'{self.shortform}'

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    ingredient_type_id = db.Column(db.Integer, db.ForeignKey('ingredient_type.id'))
    recipe_ingredient_id = db.relationship('RecipeIngredient', backref='ingredient', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}'

class IngredientType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    ingredient_id = db.relationship('Ingredient', backref='type', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}'