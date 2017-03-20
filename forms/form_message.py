from flask import flash


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
