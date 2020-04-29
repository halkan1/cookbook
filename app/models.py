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
    '''Needs nullable=False on all foreign keys and other columns 
    when production ready.
    Needs add & remove step functions'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    description = db.Column(db.String(128))
    # timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    servings = db.Column(db.Integer)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ingredients = db.relationship('RecipeIngredient', backref='recipe', lazy='dynamic')
    steps = db.relationship('RecipeStep', backref='recipe', lazy='dynamic')
    comments = db.Column(db.String(512))
    source = db.Column(db.String(128))

    def add_ingredient(self, quantity, unit, ingredient):
        quantity = MeasurementQty.query.filter_by(quantity=quantity).first()
        unit = MeasurementUnit.query.filter_by(shortform=unit).first()
        ingredient = Ingredient.query.filter_by(name=ingredient).first()
        if quantity is not None and unit is not None and ingredient is not None:
            db.session.add(RecipeIngredient(quantity=quantity, unit=unit, ingredient=ingredient, recipe=self))
            db.session.commit()
        else:
            return None

    def delete_ingredient(self, ingredient):
        recipe_ingredient = RecipeIngredient.query.join(
            Recipe).join(Ingredient).filter(
                Recipe.name == self.name).filter(
                    Ingredient.name == ingredient).first()
        #recipe_ingredient = RecipeIngredient.query.join(Ingredient).filter(Ingredient.name == ingredient).first()
        #self.ingredients.remove(recipe_ingredient)
        if recipe_ingredient is not None:
            db.session.delete(recipe_ingredient)
            db.session.commit()
        else:
            return None

    def __repr__(self):
        return f'{self.name}'

class RecipeStep(db.Model):
    '''Needs nullable=False on all foreign keys when production ready'''
    id = db.Column(db.Integer, primary_key=True)
    step_number = db.Column(db.Integer, nullable=False)
    step_text = db.Column(db.String(64), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    def __repr__(self):
        return f'{self.step_number}. {self.step_text}'

class RecipeIngredient(db.Model):
    """Association Table to create ingredient combinations for the recipe
    Needs nullable=False on all foreign keys when production ready"""
    id = db.Column(db.Integer, primary_key=True)
    measurement_qty_id = db.Column(db.Integer, db.ForeignKey('measurement_qty.id'))
    measurement_unit_id = db.Column(db.Integer, db.ForeignKey('measurement_unit.id'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    def __repr__(self):
        return f'{self.quantity} {self.unit} {self.ingredient}'

class MeasurementQty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, unique=True, nullable=False)
    recipe_ingredient_id = db.relationship('RecipeIngredient', backref='quantity', lazy='dynamic')

    def __repr__(self):
        return f'{self.quantity}'

class MeasurementUnit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shortform = db.Column(db.String(8), unique=True, nullable=False)
    fullform = db.Column(db.String(16), unique=True, nullable=False)
    recipe_ingredient_id = db.relationship('RecipeIngredient', backref='unit', lazy='dynamic')

    def __repr__(self):
        return f'{self.shortform}'

class Ingredient(db.Model):
    '''Needs nullable=False on all foreign keys when production ready'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    ingredient_type_id = db.Column(db.Integer, db.ForeignKey('ingredient_type.id'))
    recipe_ingredient_id = db.relationship('RecipeIngredient', backref='ingredient', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}'

class IngredientType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    ingredient_id = db.relationship('Ingredient', backref='type', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}'