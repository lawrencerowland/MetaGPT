from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class ContractorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    specialty = StringField('Specialty', validators=[DataRequired()])
    rating = FloatField('Rating', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

class ReviewForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    rating = FloatField('Rating', validators=[DataRequired()])
