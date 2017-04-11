from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class AddSubjectForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    major = StringField('Major')
    grade = StringField('Grade')
    weight = StringField('Weight')
    category = StringField('Category')
    curriculum = StringField('Curriculum')
    alias = StringField('Alias')
