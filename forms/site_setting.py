from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class SiteSettingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])

    def send_placeholder(self, setting, *args, **kwargs):
        self.setting = setting
        kwargs['obj'] = self.setting
        super(SiteSettingForm, self).__init__(*args, **kwargs)
