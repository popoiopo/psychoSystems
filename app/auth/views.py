# app/auth/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user, current_user

from . import auth
from forms import LoginForm, RegistrationForm, FactorForm
from .. import db
from ..models import Expert, Factor


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        expert_data = Expert(first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            username=form.username.data,
                            title_id=form.title_id.data.id,
                            affiliation_id=form.affiliation_id.data.id,
                            discipline=form.discipline.data,
                            uni_work=form.uni_work.data,
                            country=form.country.data,
                            specialization=form.specialization.data,
                            personal_descr=form.personal_descr.data,
                            permission_mention=form.permission_mention.data.name,
                            permission_add_question=form.permission_add_question.data.name,
                            email=form.email.data,
                            password=form.password.data)

        # add employee to the database
        db.session.add(expert_data)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        expert_data = Expert.query.filter_by(email=form.email.data).first()
        if expert_data is not None and expert_data.verify_password(
                form.password.data):
            # log employee in
            login_user(expert_data)

             # redirect to the appropriate dashboard page
            if expert_data.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))


###########################################################################
# Factor Views
###########################################################################


@auth.route('/factors')
@login_required
def list_factors():
    """
    List all factors
    """

    factors = Factor.query.all()
    return render_template('auth/factors/factors.html',
                           factors=factors, title='Factor')


@auth.route('/factors/add', methods=['GET', 'POST'])
@login_required
def add_factor():
    """
    Add a factor to the database
    """

    add_factor = True

    form = FactorForm()
    if form.validate_on_submit():
        factor = Factor(expert_id=current_user.get_id(),
                        factor_A=form.factor_A.data,
                        factor_B=form.factor_B.data,
                        relation_weight=form.relation_weight.data,
                        temp_aspect_id=form.temp_aspect_id.data.id,
                        temp_imp_id=form.temp_imp_id.data.id,
                        operator_id=form.operator_id.data.id,
                        factor_C=form.factor_C.data,
                        factor_D=form.factor_D.data,
                        notes_A=form.notes_A.data,
                        notes_B=form.notes_B.data,
                        notes_C=form.notes_A.data,
                        notes_D=form.notes_B.data,
                        notes_relation=form.notes_relation.data,
                        )

        try:
            # add factor to the database
            db.session.add(factor)
            db.session.commit()
            flash('You have successfully added a new factor.')
        except: 
            # in case factor name already exists
            flash('Error: Something went wrong with sending your request to the database! Please email iasdepressionresearch@gmail.com about this behaviour.')

        # redirect to the factors page
        return redirect(url_for('auth.list_factors'))

    # load factor template
    return render_template('auth/factors/factor.html', add_factor=add_factor,
                           form=form, title='Add Factor')


@auth.route('/factors/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_factor(id):
    """
    Edit a factor
    """

    add_factor = False

    factor = Factor.query.get_or_404(id)
    form = FactorForm(obj=factor)
    if form.validate_on_submit():
        factor.factor_A = form.factor_A.data
        factor.factor_B = form.factor_B.data
        factor.relation_weight = form.relation_weight.data
        factor.temp_aspect_id = form.temp_aspect_id.data.id
        factor.temp_imp_id = form.temp_imp_id.data.id
        factor.operator_id = form.operator_id.data.id
        factor.factor_C = form.factor_C.data
        factor.factor_D = form.factor_D.data
        factor.notes_A = form.notes_A.data
        factor.notes_B = form.notes_B.data
        factor.notes_C = form.notes_C.data
        factor.notes_D = form.notes_D.data
        factor.notes_relation = form.notes_relation.data
        
        db.session.add(factor)
        db.session.commit()
        flash('You have successfully edited the new factor.')

        # redirect to the factors page
        return redirect(url_for('auth.list_factors'))

    form.factor_A.data = factor.factor_A
    form.factor_B.data = factor.factor_B
    form.relation_weight.data = factor.relation_weight
    form.temp_aspect_id.data = factor.temp_aspect_id
    form.temp_imp_id.data = factor.temp_imp_id
    form.operator_id.data = factor.operator_id
    form.factor_C.data = factor.factor_C
    form.factor_D.data = factor.factor_D
    form.notes_A.data = factor.notes_A
    form.notes_B.data = factor.notes_B
    form.notes_C.data = factor.notes_C
    form.notes_D.data = factor.notes_D
    form.notes_relation.data = factor.notes_relation
    return render_template('auth/factors/factor.html', add_factor=add_factor,
                           form=form, title="Edit Factor")


@auth.route('/factors/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_factor(id):
    """
    Delete a factor from the database
    """

    factor = Factor.query.get_or_404(id)
    db.session.delete(factor)
    db.session.commit()
    flash('You have successfully deleted the factor.')

    # redirect to the factors page
    return redirect(url_for('auth.list_factors'))

    return render_template(title="Delete factor")
