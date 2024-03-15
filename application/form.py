from wtforms import TextAreaField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length

from . import util

languages_choice = []
for key, value in util.languages.items():
    languages_choice.append((key, value))
    

class QRCodeData(FlaskForm):
    data_field = TextAreaField('Original Text',validators=[DataRequired(), Length(min=1, max=250)])
    language=""
    language_field = SelectField("Language to translate to", choices=languages_choice)
    translated_field=TextAreaField('Translated Text')
    submit = SubmitField('Translate') 