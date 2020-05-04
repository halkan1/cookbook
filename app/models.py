from app import db, login
from datetime import datetime
from flask_login import UserMixin
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash

# Many to Many relationships
recipe_tags = db.Table('recipe_tags',
    db.Column('recipes', db.Integer, db.ForeignKey('recipe.id')),
    db.Column('tags', db.Integer, db.ForeignKey('tag.id')),
    db.UniqueConstraint('recipes', 'tags')
)

recipe_ingredients = db.Table('recipe_ingredients',
    db.Column('recipes', db.Integer, db.ForeignKey('recipe.id')),
    db.Column('ingredients', db.Integer, db.ForeignKey('ingredient_set.id')),
    db.UniqueConstraint('recipes', 'ingredients')
)

# Database models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    recipes = db.relationship('Recipe', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return f'<User {self.username}>'

class Recipe(db.Model):
    '''Needs nullable=False some columns when production ready.'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    description = db.Column(db.String(128))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.relationship('Tag', secondary=recipe_tags, backref=db.backref(
        'recipes', lazy='dynamic'), lazy='dynamic')
    servings = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ingredients = db.relationship('IngredientSet', secondary=recipe_ingredients, 
        backref=db.backref('recipes', lazy='dynamic'), lazy='dynamic')
    steps = db.relationship('RecipeStep', backref='recipe', lazy='dynamic', 
        order_by='RecipeStep.step_number')
    comments = db.Column(db.String(512))
    source = db.Column(db.String(128))
    
    def add_ingredient(self, ingredient_set):
        if not self.has_ingredient(ingredient_set):
            self.ingredients.append(ingredient_set)

    def remove_ingredient(self, ingredient_set):
        if self.has_ingredient(ingredient_set):
            self.ingredients.remove(ingredient_set)

    def has_ingredient(self, ingredient_set):
        return self.ingredients.filter(
            recipe_ingredients.c.ingredients == ingredient_set.id).count() > 0

    def __repr__(self):
        return f'{self.name}'

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.name}'

class RecipeStep(db.Model):
    '''Needs nullable=False on all foreign keys when production ready'''
    id = db.Column(db.Integer, primary_key=True)
    step_number = db.Column(db.Integer, nullable=False)
    step_text = db.Column(db.String(64), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    __table_args__ = (db.UniqueConstraint(step_number, recipe_id),)

    def __repr__(self):
        return f'{self.step_number}. {self.step_text}'

class IngredientSet(db.Model):
    """Table to create ingredient combinations for the recipe"""
    id = db.Column(db.Integer, primary_key=True)
    measurement_qty_id = db.Column(db.Integer, db.ForeignKey(
        'measurement_qty.id'), nullable=False)
    measurement_unit_id = db.Column(db.Integer, db.ForeignKey(
        'measurement_unit.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey(
        'ingredient.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint(
        measurement_qty_id, measurement_unit_id, ingredient_id),)

    @staticmethod
    def add_set(quantity, unit, ingredient):
        ingredient_set = IngredientSet.get_set(quantity, unit, ingredient)
        if ingredient_set is None:
            quantity = MeasurementQty.query.filter_by(quantity=quantity).first()
            unit = MeasurementUnit.query.filter_by(shortform=unit).first()
            ingredient = Ingredient.query.filter_by(name=ingredient).first()
            db.session.add(IngredientSet(
                quantity=quantity, unit=unit, ingredient=ingredient))
            # should move commit to route instead
            db.session.commit()

    @staticmethod
    def remove_set(quantity, unit, ingredient):
        ingredient_set = IngredientSet.get_set(quantity, unit, ingredient)
        if ingredient_set:
            db.session.delete(ingredient_set)
            # should move commit to route instead
            db.session.commit()

    @staticmethod
    def get_set(quantity, unit, ingredient):
        query = IngredientSet.query.join(
            MeasurementQty, MeasurementUnit, Ingredient).filter(
                MeasurementQty.quantity==quantity, 
                MeasurementUnit.shortform==unit, 
                Ingredient.name==ingredient).first()
        if query is not None:
            return query
        return None

    def __repr__(self):
        return f'{self.quantity} {self.unit} {self.ingredient}'

class MeasurementQty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, unique=True, nullable=False)
    ingredient_set_id = db.relationship(
        'IngredientSet', backref='quantity', lazy='dynamic')

    def __repr__(self):
        return f'{self.quantity}'

class MeasurementUnit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shortform = db.Column(db.String(8), unique=True, nullable=False)
    fullform = db.Column(db.String(16), unique=True, nullable=False)
    ingredient_set_id = db.relationship(
        'IngredientSet', backref='unit', lazy='dynamic')

    def __repr__(self):
        return f'{self.shortform}'

class Ingredient(db.Model):
    '''Needs nullable=False on all foreign keys when production ready'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    ingredient_type_id = db.Column(db.Integer, db.ForeignKey('ingredient_type.id'))
    ingredient_set_id = db.relationship(
        'IngredientSet', backref='ingredient', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}'

class IngredientType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    ingredient_id = db.relationship('Ingredient', backref='type', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))