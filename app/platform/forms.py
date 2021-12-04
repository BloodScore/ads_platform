from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired


class AdCreationForm(FlaskForm):
    text_description = TextField('Description', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    categories = SelectMultipleField('Categories', choices=[])
    submit = SubmitField('Create Ad')
