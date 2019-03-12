# app/home/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Expert, Title, Affiliation, Yes_no, Temp_aspect, Temp_imp, Operator

class NodeForm(FlaskForm):
	factor = StringField('Factor label', validators=[DataRequired()])
	temp_imp_id = QuerySelectField('At what stage is this factor important?', query_factory=lambda: Temp_imp.query.all(), get_label="name")
	temp_aspect_id = QuerySelectField('How fast are changes concerning this factor?', query_factory=lambda: Temp_aspect.query.all(), get_label="name")
	notes_factor = StringField('Could you shortly elaborate on this factor?')
	notes = StringField('Any general notes?')
	sup_lit = StringField('Supporting literature (seperate by / )')
	submit = SubmitField('Submit')