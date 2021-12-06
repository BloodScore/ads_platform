from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SelectMultipleField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length


class AdCreationForm(FlaskForm):
    text_description = TextField('Description', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    categories = SelectMultipleField('Categories', choices=[], validators=[DataRequired()])
    submit = SubmitField('Create Ad')


class SearchForm(FlaskForm):
    text_description = TextField('Description')
    location = StringField('Location')
    price_from = StringField('Price from')
    price_to = StringField('Price to')
    categories = SelectMultipleField('Categories', choices=[])
    submit = SubmitField('Search')


class PaymentForm(FlaskForm):
    card_number = StringField('Card Number')
    exp_date = StringField('Expiration Date')
    cvv = IntegerField('CVV-code')
    submit = SubmitField('Make payment')


class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('Send message')
