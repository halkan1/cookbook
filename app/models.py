from app import db

# Many to Many relationships
recipe_tags = db.Table('recipe_tags',
    db.Column('recipes', db.Integer, db.ForeignKey('recipe.id')),
    db.Column('tags', db.Integer, db.ForeignKey('tag.id')),
    db.UniqueConstraint('recipes', 'tags')
)

recipe_ingredients = db.Table('recipe_ingredients',
    db.Column('recipes', db.Integer, db.ForeignKey('recipe.id')),
    db.Column('ingredients', db.Integer, db.ForeignKey('recipe_ingredient.id')),
    db.UniqueConstraint('recipes', 'ingredients')
)

# Database models
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
    when production ready.'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    description = db.Column(db.String(128))
    #tags = db.relationship('Tag', backref='recipe', lazy='dynamic')
    tags = db.relationship('Tag', secondary=recipe_tags, backref=db.backref('recipes', lazy='dynamic'), lazy='dynamic')
    # timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    servings = db.Column(db.Integer)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #ingredients = db.relationship('RecipeIngredient', backref='recipe', lazy='dynamic')
    ingredients = db.relationship('RecipeIngredient', secondary=recipe_ingredients, backref=db.backref('recipes', lazy='dynamic'), lazy='dynamic')
    steps = db.relationship('RecipeStep', backref='recipe', lazy='dynamic')
    comments = db.Column(db.String(512))
    source = db.Column(db.String(128))
    '''
    def add_ingredient_set(self, quantity, unit, ingredient):
        if not self.get_ingredient_set(quantity, unit, ingredient):
            db.session.add(RecipeIngredient(
                quantity=quantity, 
                unit=unit, 
                ingredient=ingredient))
            db.session.commit()
    '''
    def add_ingredient_set(self, quantity, unit, ingredient):
        '''This should probably be under REcipeIngredient as a static method instead '''
        quantity = MeasurementQty.query.filter_by(quantity=quantity).first()
        unit = MeasurementUnit.query.filter_by(shortform=unit).first()
        ingredient = Ingredient.query.filter_by(name=ingredient).first()
        db.session.add(RecipeIngredient(quantity=quantity, unit=unit, ingredient=ingredient))
        db.session.commit()
    
    def remove_ingredient_set(self, quantity, unit, ingredient):
        if self.get_ingredient_set(quantity, unit, ingredient):
            db.session.remove(RecipeIngredient(
                quantity=quantity, 
                unit=unit, 
                ingredient=ingredient))
            db.session.commit()

    def get_ingredient_set(self, quantity, unit, ingredient):
        query = RecipeIngredient.query.join(
            MeasurementQty, MeasurementUnit, Ingredient).filter(
                MeasurementQty.quantity==quantity, 
                MeasurementUnit.shortform==unit, 
                Ingredient.name==ingredient).first()
        if query is not None:
            return query
        return False

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

class RecipeIngredient(db.Model):
    """Table to create ingredient combinations for the recipe"""
    id = db.Column(db.Integer, primary_key=True)
    measurement_qty_id = db.Column(db.Integer, db.ForeignKey('measurement_qty.id'), nullable=False)
    measurement_unit_id = db.Column(db.Integer, db.ForeignKey('measurement_unit.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint(measurement_qty_id, measurement_unit_id, ingredient_id),)

    @staticmethod
    def add_ingredient_set(quantity, unit, ingredient):
        ingredient_set = RecipeIngredient.ingredient_set_exists(quantity, unit, ingredient)
        if ingredient_set is None:
            quantity = MeasurementQty.query.filter_by(quantity=quantity).first()
            unit = MeasurementUnit.query.filter_by(shortform=unit).first()
            ingredient = Ingredient.query.filter_by(name=ingredient).first()
            db.session.add(RecipeIngredient(
                quantity=quantity, unit=unit, ingredient=ingredient))
            db.session.commit()

    @staticmethod
    def remove_ingredient_set(quantity, unit, ingredient):
        ingredient_set = RecipeIngredient.ingredient_set_exists(quantity, unit, ingredient)
        if ingredient_set:
            db.session.delete(ingredient_set)
            db.session.commit()

    @staticmethod
    def ingredient_set_exists(quantity, unit, ingredient):
        query = RecipeIngredient.query.join(
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