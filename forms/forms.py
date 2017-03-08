from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


def flash_errors(form):
    """ Universal interface to handle form error.
    Handles form error with the help of flash message
    """
    for field, errors in form.errors.items():
        for error in errors:
            flash(u'Error in the %s field - %s' % (
                getattr(form, field).label.text,
                error
            ))


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(max=16)])
    password = PasswordField('Password',
                             validators=[DataRequired()])


class AddEmployeeForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(max=16)
        ]
    )
    fullname = StringField(
        'Full name',
        validators=[DataRequired()]
    )
    nip = StringField(
        'Nip',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'password',
        validators=[
            DataRequired(),
            EqualTo('verifyPassword', message='Password must match.')
        ]
    )
    verifyPassword = PasswordField('Verify password')


class EditEmployeeForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(max=16)
        ]
    )
    fullname = StringField(
        'Full name',
        validators=[DataRequired()]
    )
    nip = StringField(
        'Nip',
        validators=[DataRequired()]
    )
