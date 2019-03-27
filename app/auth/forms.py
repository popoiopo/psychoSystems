# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Expert, Title, Affiliation, Yes_no, Temp_aspect, Temp_imp, Operator


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    title_id = QuerySelectField('Title / Adressing', query_factory=lambda: Title.query.all(),
                                  get_label="name")
    affiliation_id = QuerySelectField('What is your affiliation with depression?', query_factory=lambda: Affiliation.query.all(),
                                  get_label="name")
    discipline = StringField('In which discipline do you work? (e.g. Biology, Public Health, etc.)', validators=[DataRequired()])
    uni_work = StringField('Name of University or place of work', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    specialization = StringField('Specialization (If multiple, seperate with comma and a space ", ")', validators=[DataRequired()])
    personal_descr = StringField('Personal Description', validators=[DataRequired()])
    permission_mention = QuerySelectField('Would you like to be mentioned as contributor?', query_factory=lambda: Yes_no.query.all(),
                                  get_label="name", validators=[DataRequired()])
    permission_add_question = QuerySelectField('Could we contact you with further questions regarding your contribution?', query_factory=lambda: Yes_no.query.all(),
                                  get_label="name", validators=[DataRequired()])

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Expert.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if Expert.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class FactorForm(FlaskForm):
    """
    Form for users to add factors
    """

    factor_A = StringField('Factor A which has effect on B', validators=[DataRequired()])
    factor_B = StringField('Factor B')
    relation_weight = IntegerField('Relation weight (integer between 1 and 10)')
    temp_aspect_id = QuerySelectField('At what stage is this relation important?', query_factory=lambda: Temp_imp.query.all(),
                                  get_label="name")
    temp_imp_id = QuerySelectField('How long would it take to see effect on Factor B?', query_factory=lambda: Temp_aspect.query.all(),
                                  get_label="name")
    operator_id = QuerySelectField('Under what condition does this relation hold? Choose an operator and give the factor under which the A-B relation holds.', query_factory=lambda: Operator.query.all(),
                                  get_label="name")
    factor_C = StringField('Factor C which is a condition for A-B')
    factor_D = StringField('Factor D, might also be a condition')
    notes_A = StringField('Could you shortly elaborate on factor A?', validators=[DataRequired()])
    notes_B = StringField('Could you shortly elaborate on factor B?')
    notes_C = StringField('Could you shortly elaborate on factor C?')
    notes_D = StringField('Could you shortly elaborate on factor D?')
    notes_relation = StringField('Could you shortly elaborate on the relationship?')
    submit = SubmitField('Submit')


