from flask import flash, url_for
from openedoo.core.libs import render_template, request, redirect
from openedoo_project import db
from ..views.decorators import login_required, site_setting
from ..models import Setting
from ..forms import SiteSettingForm, flash_errors
from .base_controller import BaseController


class SiteSetting(BaseController):

    methods = ['GET', 'POST']
    decorators = [login_required, site_setting]

    def dispatch_request(self):
        setting = Setting()
        existingSetting = setting.get_existing_name()
        siteSettingForm = SiteSettingForm()
        isFormValid = self.is_form_valid(siteSettingForm)
        if setting and isFormValid:
            updateSetting = setting.update(request.form)
            flash(u'Succesfully updated.', 'success')
            return redirect(url_for('module_employee.dashboard'))
        elif not setting and isFormValid:
            setSetting = setting.add(request.form)
            flash(u'Succesfully set.', 'success')
            return redirect(url_for('module_employee.dashboard'))
        else:
            flash_errors(siteSettingForm)
        return render_template('admin/site-setting.html',
                        school=self.get_site_data(),
                        data=setting,
                        form=siteSettingForm)
