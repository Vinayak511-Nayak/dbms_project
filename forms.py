from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed
from wtforms import ValidationError


class LoginForm(FlaskForm):
    username = StringField('username',validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):

    username = StringField('username',validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('confirm_password',message='please verify email')])
    confirm_password = PasswordField('confirm password',validators=[DataRequired()])
    address=StringField('address')
    submit = SubmitField('Register')

class RiceForm(FlaskForm):
    IT_NO=IntegerField('IT_NO')
    Quantity=IntegerField('Quantity')

class PaneerForm(FlaskForm):
    IT_NO=IntegerField('IT_NO')
    Quantity=IntegerField('Quantity')
