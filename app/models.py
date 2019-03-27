# app/models.py

import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class Expert(UserMixin, db.Model):
    """
    Create an expert table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'experts'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    username = db.Column(db.String(60), index=True, unique=True)
    email = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    title_id = db.Column(db.Integer, db.ForeignKey('titles.id'))
    affiliation_id = db.Column(db.Integer, db.ForeignKey('affiliations.id'))
    discipline = db.Column(db.String(60), index=True)
    uni_work = db.Column(db.String(60), index=True)
    country = db.Column(db.String(60), index=True)
    accepted_id = db.Column(db.Integer, db.ForeignKey('accepteds.id'))
    specialization = db.Column(db.String(200))
    personal_descr = db.Column(db.String(1000))
    permission_mention = db.Column(db.String(15), index=True)
    permission_add_question = db.Column(db.String(15), index=True)
    core_exp = db.Column(db.String(3), index=True)
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.username


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Expert.query.get(int(user_id))


class Title(db.Model):
    """
    Create a title table
    """

    __tablename__ = 'titles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    experts = db.relationship('Expert', backref='title',
                                lazy='dynamic')

    def __repr__(self):
        return self.name


class pageTexts(db.Model):
    """
    Create a title table
    """

    __tablename__ = 'pageTexts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    pageID = db.Column(db.String(60))
    htmlName = db.Column(db.String(60))

    def __repr__(self):
        return self.name


class Yes_no(db.Model):
    """
    Create a title table
    """

    __tablename__ = 'yes_no'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)

    def __repr__(self):
        return self.name


class Accepted(db.Model):
    """
    Create a accepted table
    """

    __tablename__ = 'accepteds'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    experts = db.relationship('Expert', backref='accepted',
                                lazy='dynamic')

    def __repr__(self):
        return self.name


class Affiliation(db.Model):
    """
    Create a affiliation with MD table
    """

    __tablename__ = 'affiliations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    experts = db.relationship('Expert', backref='affiliation',
                                lazy='dynamic')

    def __repr__(self):
        return self.name


class Factor(db.Model):
    """
    Create a factor table
    """

    __tablename__ = 'factors'

    id = db.Column(db.Integer, primary_key=True)
    expert_id = db.Column(db.Integer, db.ForeignKey('experts.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    factor_A = db.Column(db.String(60))
    factor_B = db.Column(db.String(60))
    value = db.Column(db.Integer)
    temp_aspect_id = db.Column(db.Integer, db.ForeignKey('temp_aspects.id'))
    temp_imp_id = db.Column(db.Integer, db.ForeignKey('temp_imps.id'))
    operator_id = db.Column(db.Integer, db.ForeignKey('operators.id'))
    factor_C = db.Column(db.String(60))
    factor_D = db.Column(db.String(60))
    notes_A = db.Column(db.String(500))
    notes_B = db.Column(db.String(500))
    notes_C = db.Column(db.String(500))
    notes_D = db.Column(db.String(500))
    notes_relation = db.Column(db.String(500))


class Node(db.Model):
    """
    Create a factor table
    """

    __tablename__ = 'nodes'

    id = db.Column(db.Integer, primary_key=True)
    expert_id = db.Column(db.Integer, db.ForeignKey('experts.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    factor = db.Column(db.String(60))
    sensitivity_id = db.Column(db.Integer, db.ForeignKey('sensitivities.id'), default=1)
    spat_aspect_id = db.Column(db.Integer, db.ForeignKey('spat_aspects.id'))
    temp_aspect_id = db.Column(db.Integer, db.ForeignKey('temp_aspects.id'))
    temp_imp_id = db.Column(db.Integer, db.ForeignKey('temp_imps.id'))
    notes = db.Column(db.String(500))
    node_type_id = db.Column(db.Integer, db.ForeignKey('node_types.id'))
    notes_factor = db.Column(db.String(500))


class Edge(db.Model):
    """
    Create a factor table
    """

    __tablename__ = 'edges'

    id = db.Column(db.Integer, primary_key=True)
    expert_id = db.Column(db.Integer, db.ForeignKey('experts.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    factor_A = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    factor_B = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    con_strength_id = db.Column(db.Integer, db.ForeignKey('con_strengths.id'), default=3)
    spat_aspect_id = db.Column(db.Integer, db.ForeignKey('spat_aspects.id'))
    temp_aspect_id = db.Column(db.Integer, db.ForeignKey('temp_aspects.id'))
    temp_imp_id = db.Column(db.Integer, db.ForeignKey('temp_imps.id'))
    operator_id = db.Column(db.Integer, db.ForeignKey('operators.id'))
    notes_relation = db.Column(db.String(500))
    edge_type = db.Column(db.String(10))
    sup_lit = db.Column(db.String(500))


class Node_type(db.Model):
    """
    Create a temporal aspect table
    [Stock, Cloud, Variable, Constant, Unknown]
    """

    __tablename__ = 'node_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), default="unknown")
    code = db.Column(db.String(60), default="\uf128")
    size = db.Column(db.Integer, default=40)
    color = db.Column(db.String(60), default="#aa00ff")    
    nodes = db.relationship('Node', backref='node_type',
                                lazy='dynamic')

    def __repr__(self):
        return self.name


class Sensitivity(db.Model):
    """
    Create a sensitivity table
    [Very Negative, Negative, Neutral, Positive, Very Positive]
    """

    __tablename__ = 'sensitivities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    factors_Sens = db.relationship('Node', backref='sensitivity',
                                lazy='dynamic')

    def __repr__(self):
        return self.name


class Con_strength(db.Model):
    """
    Create a connection-strength table
    [Seconds, Minutes, Hours, Days, Months, Years, Lifetime]
    """

    __tablename__ = 'con_strengths'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    factors_Constr = db.relationship('Edge', backref='con_strength',
                                lazy='dynamic')

    def __repr__(self):
        return self.name


class Temp_aspect(db.Model):
    """
    Create a temporal aspect table
    [Seconds, Minutes, Hours, Days, Months, Years, Lifetime]
    """

    __tablename__ = 'temp_aspects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    factors_TA = db.relationship('Node', backref='temp_aspect',
                                lazy='dynamic')

    def __repr__(self):
        return self.name


class Temp_imp(db.Model):
    """
    Create a temporal importance table
    [Onset, Maintenance, Relapse, Onset-Maintenance, Onset-Relapse, 
        Maintenance-Relapse, All of the above]
    """

    __tablename__ = 'temp_imps'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    factors_TI = db.relationship('Node', backref='temp_imp',
                                lazy='dynamic')

    def __repr__(self):
        return self.name


class Spat_aspect(db.Model):
    """
    Create a temporal aspect table
    [Seconds, Minutes, Hours, Days, Months, Years, Lifetime]
    """

    __tablename__ = 'spat_aspects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    factors_SA = db.relationship('Node', backref='spat_aspect',
                                lazy='dynamic')

    def __repr__(self):
        return self.name



class Operator(db.Model):
    """
    Create a operators table
    [if, or, xor, and]
    """

    __tablename__ = 'operators'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    factors_OP = db.relationship('Edge', backref='operator',
                                lazy='dynamic')

    def __repr__(self):
        return self.name


# class Literature_factor(db.Model):
#     """
#     Create a literature table for the factors
#     """

#     __tablename__ = 'literature_factors'

#     id = db.Column(db.Integer, primary_key=True)
#     factor_id = db.Column(db.Integer, db.ForeignKey('factors.id'))
#     name = db.Column(db.String(60))
#     description = db.Column(db.String(500))


# class Treatment_factor(db.Model):
#     """
#     Create a factor table
#     """

#     __tablename__ = 'treatment_factors'

#     id = db.Column(db.Integer, primary_key=True)
#     expert_id = db.Column(db.Integer, db.ForeignKey('experts.id'))
#     created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
#     treat_factor = db.Column(db.String(60))
#     effect_on_factor = db.Column(db.String(60))
#     treatment_weight = db.Column(db.Integer)
#     relation_temp = db.Column(db.Integer, db.ForeignKey('temp_aspects.id'))
#     notes = db.Column(db.String(500))
#     temp_imp_data = db.Column(db.Integer, db.ForeignKey('temp_imps.id'))


# class Literature_treat_factor(db.Model):
#     """
#     Create a literature table for the factors
#     """

#     __tablename__ = 'literature_treat_factors'

#     id = db.Column(db.Integer, primary_key=True)
    
#     factor_id = db.Column(db.Integer, db.ForeignKey('treatment_factors.id'))
#     name = db.Column(db.String(60))
#     description = db.Column(db.String(500))
#     