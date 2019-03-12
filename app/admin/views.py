# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from .. import db
from . import admin
from ..models import Title, Temp_aspect, Temp_imp, Affiliation, Accepted, Expert, Yes_no, Operator
from forms import TitleForm, Temp_aspectForm, Temp_impForm, AffiliationForm, AcceptedForm, ExpertAssignForm, Yes_noForm, OperatorForm


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


############################################################################
# Title Views
############################################################################


@admin.route('/titles', methods=['GET', 'POST'])
@login_required
def list_titles():
    """
    List all titles
    """
    check_admin()

    titles = Title.query.all()

    return render_template('admin/titles/titles.html',
                           titles=titles, title="titles")


@admin.route('/titles/add', methods=['GET', 'POST'])
@login_required
def add_title():
    """
    Add a title to the database
    """
    check_admin()

    add_title = True

    form = TitleForm()
    if form.validate_on_submit():
        title = Title(name=form.name.data)
        try:
            # add title to the database
            db.session.add(title)
            db.session.commit()
            flash('You have successfully added a new title.')
        except:
            # in case title name already exists
            flash('Error: title name already exists.')

        # redirect to titles page
        return redirect(url_for('admin.list_titles'))

    # load title template
    return render_template('admin/titles/title.html', action="Add",
                           add_title=add_title, form=form,
                           title="Add Title")


@admin.route('/titles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_title(id):
    """
    Edit a title
    """
    check_admin()

    add_title = False

    title = Title.query.get_or_404(id)
    form = TitleForm(obj=title)
    if form.validate_on_submit():
        title.name = form.name.data
        db.session.commit()
        flash('You have successfully edited the title.')

        # redirect to the titles page
        return redirect(url_for('admin.list_titles'))

    form.name.data = title.name
    return render_template('admin/titles/title.html', action="Edit",
                           add_title=add_title, form=form,
                           title_edit=title, title="Edit Title")


@admin.route('/titles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_title(id):
    """
    Delete a title from the database
    """
    check_admin()

    title = Title.query.get_or_404(id)
    db.session.delete(title)
    db.session.commit()
    flash('You have successfully deleted the title.')

    # redirect to the titles page
    return redirect(url_for('admin.list_titles'))

    return render_template(title="Delete Title")


############################################################################
# Operator Views
############################################################################


@admin.route('/operators')
@login_required
def list_operators():
    check_admin()
    """
    List all operators
    """
    operators = Operator.query.all()
    return render_template('admin/operators/operators.html',
                           operators=operators, title='Operator')


@admin.route('/operators/add', methods=['GET', 'POST'])
@login_required
def add_operator():
    """
    Add a operator to the database
    """
    check_admin()

    add_operator = True

    form = OperatorForm()
    if form.validate_on_submit():
        operator = Operator(name=form.name.data)

        try:
            # add temp_aspect to the database
            db.session.add(operator)
            db.session.commit()
            flash('You have successfully added a new operator.')
        except:
            # in case operator name already exists
            flash('Error: operator name already exists.')

        # redirect to the operator page
        return redirect(url_for('admin.list_operators'))

    # load temp_aspect template
    return render_template('admin/operators/operator.html', add_operator=add_operator,
                           form=form, title='Add Operator')


@admin.route('/operators/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_operator(id):
    """
    Edit a Operator
    """
    check_admin()

    add_operator = False

    operator = Operator.query.get_or_404(id)
    form = OperatorForm(obj=temp_aspect)
    if form.validate_on_submit():
        temp_aspect.name = form.name.data
        db.session.add(operator)
        db.session.commit()
        flash('You have successfully edited the operator.')

        # redirect to the operators page
        return redirect(url_for('admin.list_operators'))

    form.name.data = operator.name
    return render_template('admin/operators/operator.html', add_operator=add_operator,
                           form=form, title="Edit Operator")


@admin.route('/operators/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_operator(id):
    """
    Delete a operator from the database
    """
    check_admin()

    operator = Operator.query.get_or_404(id)
    db.session.delete(operator)
    db.session.commit()
    flash('You have successfully deleted the operator.')

    # redirect to the operators page
    return redirect(url_for('admin.list_operators'))

    return render_template(title="Delete Operator")


############################################################################
# Temp_aspect Views
############################################################################


@admin.route('/temp_aspects')
@login_required
def list_temp_aspects():
    check_admin()
    """
    List all temp_aspects
    """
    temp_aspects = Temp_aspect.query.all()
    return render_template('admin/temp_aspects/temp_aspects.html',
                           temp_aspects=temp_aspects, title='Temp_aspects')


@admin.route('/temp_aspects/add', methods=['GET', 'POST'])
@login_required
def add_temp_aspect():
    """
    Add a temp_aspect to the database
    """
    check_admin()

    add_temp_aspect = True

    form = Temp_aspectForm()
    if form.validate_on_submit():
        temp_aspect = Temp_aspect(name=form.name.data)

        try:
            # add temp_aspect to the database
            db.session.add(temp_aspect)
            db.session.commit()
            flash('You have successfully added a new temporal aspect.')
        except:
            # in case temp_aspect name already exists
            flash('Error: temp_aspect name already exists.')

        # redirect to the temp_aspects page
        return redirect(url_for('admin.list_temp_aspects'))

    # load temp_aspect template
    return render_template('admin/temp_aspects/temp_aspect.html', add_temp_aspect=add_temp_aspect,
                           form=form, title='Add Temporal aspect')


@admin.route('/temp_aspects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_temp_aspect(id):
    """
    Edit a Temporal aspect
    """
    check_admin()

    add_temp_aspect = False

    temp_aspect = Temp_aspect.query.get_or_404(id)
    form = Temp_aspectForm(obj=temp_aspect)
    if form.validate_on_submit():
        temp_aspect.name = form.name.data
        db.session.add(temp_aspect)
        db.session.commit()
        flash('You have successfully edited the temporal aspect.')

        # redirect to the temp_aspects page
        return redirect(url_for('admin.list_temp_aspects'))

    form.name.data = temp_aspect.name
    return render_template('admin/temp_aspects/temp_aspect.html', add_temp_aspect=add_temp_aspect,
                           form=form, title="Edit Temporal aspect")


@admin.route('/temp_aspects/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_temp_aspect(id):
    """
    Delete a temp_aspect from the database
    """
    check_admin()

    temp_aspect = Temp_aspect.query.get_or_404(id)
    db.session.delete(temp_aspect)
    db.session.commit()
    flash('You have successfully deleted the temp_aspect.')

    # redirect to the temp_aspects page
    return redirect(url_for('admin.list_temp_aspects'))

    return render_template(title="Delete Temporal aspect")



############################################################################
# Temp_imp Views
############################################################################


@admin.route('/temp_imps')
@login_required
def list_temp_imps():
    check_admin()
    """
    List all temp_imps
    """
    temp_imps = Temp_imp.query.all()
    return render_template('admin/temp_imps/temp_imps.html',
                           temp_imps=temp_imps, title='Temp_imps')


@admin.route('/temp_imps/add', methods=['GET', 'POST'])
@login_required
def add_temp_imp():
    """
    Add a temp_imp to the database
    """
    check_admin()

    add_temp_imp = True

    form = Temp_impForm()
    if form.validate_on_submit():
        temp_imp = Temp_imp(name=form.name.data)

        try:
            # add temp_imp to the database
            db.session.add(temp_imp)
            db.session.commit()
            flash('You have successfully added a new temp_imp.')
        except:
            # in case temp_imp name already exists
            flash('Error: temp_imp name already exists.')

        # redirect to the temp_imps page
        return redirect(url_for('admin.list_temp_imps'))

    # load temp_imp template
    return render_template('admin/temp_imps/temp_imp.html', add_temp_imp=add_temp_imp,
                           form=form, title='Add Temporal importance')


@admin.route('/temp_imps/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_temp_imp(id):
    """
    Edit a temp_imp
    """
    check_admin()

    add_temp_imp = False

    temp_imp = Temp_imp.query.get_or_404(id)
    form = Temp_impForm(obj=temp_imp)
    if form.validate_on_submit():
        temp_imp.name = form.name.data
        db.session.add(temp_imp)
        db.session.commit()
        flash('You have successfully edited the temp_imp.')

        # redirect to the temp_imps page
        return redirect(url_for('admin.list_temp_imps'))

    form.name.data = temp_imp.name
    return render_template('admin/temp_imps/temp_imp.html', add_temp_imp=add_temp_imp,
                           form=form, title="Edit Temporal importance")


@admin.route('/temp_imps/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_temp_imp(id):
    """
    Delete a temp_imp from the database
    """
    check_admin()

    temp_imp = Temp_imp.query.get_or_404(id)
    db.session.delete(temp_imp)
    db.session.commit()
    flash('You have successfully deleted the temp_imp.')

    # redirect to the temp_imps page
    return redirect(url_for('admin.list_temp_imps'))

    return render_template(title="Delete temp_imp")


############################################################################
# Affiliations Views
############################################################################


@admin.route('/affiliations')
@login_required
def list_affiliations():
    check_admin()
    """
    List all affiliations
    """
    affiliations = Affiliation.query.all()
    return render_template('admin/affiliations/affiliations.html',
                           affiliations=affiliations, title='Affiliations')


@admin.route('/affiliations/add', methods=['GET', 'POST'])
@login_required
def add_affiliation():
    """
    Add a affiliation to the database
    """
    check_admin()

    add_affiliation = True

    form = AffiliationForm()
    if form.validate_on_submit():
        affiliation = Affiliation(name=form.name.data,
                    description=form.description.data)

        try:
            # add affiliation to the database
            db.session.add(affiliation)
            db.session.commit()
            flash('You have successfully added a new affiliation.')
        except:
            # in case affiliation name already exists
            flash('Error: affiliation name already exists.')

        # redirect to the affiliations page
        return redirect(url_for('admin.list_affiliations'))

    # load affiliation template
    return render_template('admin/affiliations/affiliation.html', add_affiliation=add_affiliation,
                           form=form, title='Add Affiliation')


@admin.route('/affiliations/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_affiliation(id):
    """
    Edit a affiliation
    """
    check_admin()

    add_affiliation = False

    affiliation = Affiliation.query.get_or_404(id)
    form = AffiliationForm(obj=affiliation)
    if form.validate_on_submit():
        affiliation.name = form.name.data
        affiliation.description = form.description.data
        db.session.add(affiliation)
        db.session.commit()
        flash('You have successfully edited the affiliation.')

        # redirect to the affiliations page
        return redirect(url_for('admin.list_affiliations'))

    form.description.data = affiliation.description
    form.name.data = affiliation.name
    return render_template('admin/affiliations/affiliation.html', add_affiliation=add_affiliation,
                           form=form, title="Edit Affiliation")


@admin.route('/affiliations/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_affiliation(id):
    """
    Delete a affiliation from the database
    """
    check_admin()

    affiliation = Affiliation.query.get_or_404(id)
    db.session.delete(affiliation)
    db.session.commit()
    flash('You have successfully deleted the affiliation.')

    # redirect to the affiliations page
    return redirect(url_for('admin.list_affiliations'))

    return render_template(title="Delete Affiliation")


############################################################################
# Accepted Views
############################################################################


@admin.route('/accepteds')
@login_required
def list_accepteds():
    check_admin()
    """
    List all accepteds
    """
    accepteds = Accepted.query.all()
    return render_template('admin/accepteds/accepteds.html',
                           accepteds=accepteds, title='Accepted')


@admin.route('/accepteds/add', methods=['GET', 'POST'])
@login_required
def add_accepted():
    """
    Add a accepted to the database
    """
    check_admin()

    add_accepted = True

    form = AcceptedForm()
    if form.validate_on_submit():
        accepted = Accepted(name=form.name.data,
                    description=form.description.data)

        try:
            # add accepted to the database
            db.session.add(accepted)
            db.session.commit()
            flash('You have successfully added a new accepted.')
        except:
            # in case accepted name already exists
            flash('Error: accepted name already exists.')

        # redirect to the accepteds page
        return redirect(url_for('admin.list_accepteds'))

    # load accepted template
    return render_template('admin/accepteds/accepted.html', add_accepted=add_accepted,
                           form=form, title='Add Accepted')


@admin.route('/accepteds/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_accepted(id):
    """
    Edit a accepted
    """
    check_admin()

    add_accepted = False

    accepted = Accepted.query.get_or_404(id)
    form = AcceptedForm(obj=accepted)
    if form.validate_on_submit():
        accepted.name = form.name.data
        accepted.description = form.description.data
        db.session.add(accepted)
        db.session.commit()
        flash('You have successfully edited the accepted.')

        # redirect to the accepteds page
        return redirect(url_for('admin.list_accepteds'))

    form.description.data = accepted.description
    form.name.data = accepted.name
    return render_template('admin/accepteds/accepted.html', add_accepted=add_accepted,
                           form=form, title="Edit Accepted")


@admin.route('/accepteds/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_accepted(id):
    """
    Delete a accepted from the database
    """
    check_admin()

    accepted = Accepted.query.get_or_404(id)
    db.session.delete(accepted)
    db.session.commit()
    flash('You have successfully deleted the accepted.')

    # redirect to the accepteds page
    return redirect(url_for('admin.list_accepteds'))

    return render_template(title="Delete Accepted")


############################################################################
# Expert Views
############################################################################


@admin.route('/experts')
@login_required
def list_experts():
    """
    List all experts
    """
    check_admin()

    experts = Expert.query.all()
    return render_template('admin/experts/experts.html',
                           experts=experts, title='experts')


@admin.route('/experts/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_expert(id):
    """
    Assign a yes_no and a role to an expert
    """
    check_admin()

    expert = Expert.query.get_or_404(id)

    # prevent admin from being assigned a yes_no or role
    if expert.is_admin:
        abort(403)

    form = ExpertAssignForm(obj=expert)
    if form.validate_on_submit():
        expert.accepted = form.accepted.data
        expert.core_exp = form.core.data
        db.session.add(expert)
        db.session.commit()
        flash('You have successfully assigned an expert.')

        # redirect to the roles page
        return redirect(url_for('admin.list_experts'))

    return render_template('admin/experts/expert.html',
                           expert=expert, form=form,
                           title='Assign Expert')


############################################################################
# Yes_No Views
############################################################################


@admin.route('/yes_nos', methods=['GET', 'POST'])
@login_required
def list_yes_nos():
    """
    List all yes_nos
    """
    check_admin()

    yes_nos = Yes_no.query.all()

    return render_template('admin/yes_nos/yes_nos.html',
                           yes_nos=yes_nos, title="Yes_nos")


@admin.route('/yes_nos/add', methods=['GET', 'POST'])
@login_required
def add_yes_no():
    """
    Add a yes_no to the database
    """
    check_admin()

    add_yes_no = True

    form = Yes_noForm()
    if form.validate_on_submit():
        yes_no = Yes_no(name=form.name.data)
        try:
            # add yes_no to the database
            db.session.add(yes_no)
            db.session.commit()
            flash('You have successfully added a new yes_no.')
        except:
            # in case yes_no name already exists
            flash('Error: yes_no name already exists.')

        # redirect to yes_nos page
        return redirect(url_for('admin.list_yes_nos'))

    # load yes_no template
    return render_template('admin/yes_nos/yes_no.html', action="Add",
                           add_yes_no=add_yes_no, form=form,
                           title="Add Yes_no")


@admin.route('/yes_nos/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_yes_no(id):
    """
    Edit a yes_no
    """
    check_admin()

    add_yes_no = False

    yes_no = Yes_no.query.get_or_404(id)
    form = Yes_noForm(obj=yes_no)
    if form.validate_on_submit():
        yes_no.name = form.name.data
        db.session.commit()
        flash('You have successfully edited the yes_no.')

        # redirect to the yes_nos page
        return redirect(url_for('admin.list_yes_nos'))

    form.name.data = yes_no.name
    return render_template('admin/yes_nos/yes_no.html', action="Edit",
                           add_yes_no=add_yes_no, form=form,
                           yes_no=yes_no, title="Edit Yes_no")


@admin.route('/yes_nos/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_yes_no(id):
    """
    Delete a yes_no from the database
    """
    check_admin()

    yes_no = Yes_no.query.get_or_404(id)
    db.session.delete(yes_no)
    db.session.commit()
    flash('You have successfully deleted the yes_no.')

    # redirect to the yes_nos page
    return redirect(url_for('admin.list_yes_nos'))

    return render_template(title="Delete Yes_no")