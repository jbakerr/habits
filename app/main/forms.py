from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, NumberRange
from app.models import User
from flask_babel import lazy_gettext as _l

class NewHabbitForm(FlaskForm):
    habbit = TextAreaField('Habbit To Track', validators=[
        DataRequired(), Length(min=1, max=70)])
    weekly_goal = IntegerField('Weekly Goal', validators=[
        DataRequired(), NumberRange(min=1, max=7)])
    submit = SubmitField('Submit')


class HabbitSettings(FlaskForm):
    habbit = TextAreaField('Habbit Title', validators=[
        DataRequired(), Length(min=1, max=70)])
    weekly_goal = IntegerField('Weekly Goal', validators=[
        DataRequired(), NumberRange(min=1, max=7)])
    submit = SubmitField('Submit')

    def __init__(self, original_habbit, *args, **kwargs):
        super(HabbitSettings, self).__init__(*args, **kwargs)
        self.original_habbit = original_habbit


