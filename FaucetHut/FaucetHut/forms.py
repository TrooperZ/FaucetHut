from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class addressChecker(FlaskForm):
    baddr = StringField('Check if address is ready to claim', [DataRequired()])
    submit = SubmitField('Check')