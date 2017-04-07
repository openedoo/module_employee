from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import (DataRequired, Email, Length, EqualTo,
                                ValidationError)
from sqlalchemy import and_, not_
from modules.module_employee.models import User


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

    def validate_username(self, field):
        """Username must unique"""
        isUsernameExist = User.query.filter_by(username=field.data).first()
        if isUsernameExist:
            raise ValidationError('This username is already taken. \
            Please choose another username.')


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

    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs['obj'] = self.user
        super(EditEmployeeForm, self).__init__(*args, **kwargs)

    def validate_username(self, field):
        """Username must unique, check username that is not current User.id"""
        isUsernameExist = User.query.filter(and_(
                                            User.username.like(field.data),
                                            not_((User.id == self.user.id))
                                            )).first()
        if isUsernameExist:
            raise ValidationError('This username is already taken. \
            Please choose another username.')


class AssignAsTeacherForm(FlaskForm):
    subject = SelectField('Subject',
                          coerce=int,
                          validators=[DataRequired()])
