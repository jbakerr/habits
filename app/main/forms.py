from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User
from flask_babel import lazy_gettext as _l

class NewHabbitForm(FlaskForm):
    habbit = TextAreaField('Habbit To Track', validators=[
        DataRequired(), Length(min=1, max=70)])
    submit = SubmitField('Submit')
