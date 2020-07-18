from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired

class AddMaterialForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    cost = FloatField('Total Cost', default=0.0)
    quantity = IntegerField('Quantity', default=0)

class LoginForm(FlaskForm):
    player = StringField('Player', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    player = StringField('Player Name', validators=[DataRequired()])
    submit = SubmitField('Register')