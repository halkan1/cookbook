from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField, 
                     IntegerField, TextAreaField)
from wtforms.validators import (ValidationError, DataRequired, Email, EqualTo, 
                                Length)
from app.models import User, Recipe

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please us a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class RecipeForm(FlaskForm):
    recipe = StringField('Recipe Name', validators=[DataRequired()])
    description = StringField('Description')
    created_on = datetime.utcnow()
    # tags = 
    servings = IntegerField('Servings')
    comments = TextAreaField('Comments')
    source = StringField('Source/Creator')
    submit = SubmitField('Submit')

    def validate_recipe(self, recipe):
        recipe = Recipe.query.filter_by(name=recipe.data).first()
        if recipe is not None:
            raise ValidationError('Please use a different recipe name.')

class EditRecipeForm(FlaskForm):
    recipe = StringField('Recipe Name', validators=[DataRequired()])
    description = StringField('Description')
    # tags = 
    servings = IntegerField('Servings')
    comments = TextAreaField('Comments')
    source = StringField('Source/Creator')
    submit = SubmitField('Submit')

    def __init__(self, original_recipename, *args, **kwargs):
        super(EditRecipeForm, self).__init__(*args, **kwargs)
        self.original_recipename = original_recipename

    def validate_recipename(self, recipename):
        if recipe.data != self.original_recipename:
            recipe = User.query.filter_by(name=self.recipe.data).first()
            if recipe is not None:
                raise ValidationError('Please use a different recipename.')