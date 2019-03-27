# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Accepted, Yes_no


class page_textForm(FlaskForm):
    """
    Form for admin to add or edit a title
    """
    name = TextAreaField('Name', render_kw={"rows": 70, "cols": 11})
    submit = SubmitField('Submit')


class TitleForm(FlaskForm):
    """
    Form for admin to add or edit a title
    """
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SensitivityForm(FlaskForm):
    """
    Form for admin to add or edit a node Sensitivity
    """
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Con_strengthForm(FlaskForm):
    """
    Form for admin to add or edit a connection strength
    """
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')    


class Yes_noForm(FlaskForm):
    """
    Form for admin to add or edit a title
    """
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Temp_aspectForm(FlaskForm):
    """
    Form for admin to add or edit a temporal aspect
    """
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Spat_aspectForm(FlaskForm):
    """
    Form for admin to add or edit a temporal aspect
    """
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class OperatorForm(FlaskForm):
    """
    Form for admin to add or edit an operator
    """
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Temp_impForm(FlaskForm):
    """
    Form for admin to add or edit a temporal importance
    """
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AffiliationForm(FlaskForm):
    """
    Form for admin to add or edit a temporal importance
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AcceptedForm(FlaskForm):
    """
    Form for admin to add or edit a temporal importance
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ExpertAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    accepted = QuerySelectField(query_factory=lambda: Accepted.query.all(),
                                  get_label="name")
    core = QuerySelectField(query_factory=lambda: Yes_no.query.all(),
                                  get_label="name")
    submit = SubmitField('Submit')
