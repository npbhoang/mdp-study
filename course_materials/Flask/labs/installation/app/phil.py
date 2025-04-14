from flask import Flask, render_template, request, redirect, url_for
from enum import Enum, auto
from flask_sqlalchemy import SQLAlchemy
from flask_user import current_user, login_required, UserManager, UserMixin, \
    roles_required, user_registered

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['USER_APP_NAME'] = "Thoughts app"
app.config['USER_ENABLE_EMAIL'] = False      
app.config['USER_ENABLE_USERNAME'] = True    
app.config['USER_REQUIRE_RETYPE_PASSWORD'] = False
app.config['SECRET_KEY'] = '_5#yfasQ8sansaxec/][#1'
app.config['USER_UNAUTHORIZED_ENDPOINT'] = 'error'

@app.route('/error')
def error():
    msg = "You are not allowed to access this page: Not a User"
    return render_template('error.html', message = msg)

@user_registered.connect_via(app)
def after_user_registered_hook(sender, user, **extra):
    role = Role.query.filter_by(name=USER).one()
    user.roles.append(role)
    db.session.commit()

db = SQLAlchemy(app)

USER = "User"
SYSTEM = "System"

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    thought_id = db.Column(db.Integer, db.ForeignKey('thought.id'))

class Person(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    roles = db.relationship('Role', secondary='user_roles')
    created = db.relationship('Thought', backref='createdBy')
    voted = db.relationship('Vote', backref='voter')

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('person.id'), unique=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))

class Thought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    votedBy = db.relationship('Vote', backref='votee')

with app.app_context():
    db.create_all()
    roles = Role.query.all()
    if len(roles) == 0:
        db.session.add(Role(name=USER))
        db.session.add(Role(name=SYSTEM))
        db.session.commit()

user_manager = UserManager(app, db, Person)


@app.route('/')
@login_required
@roles_required(USER)
def index():
    thoughts=Thought.query.all()
    return render_template('index.html', table=thoughts)
        
        
@app.route('/add_thought', methods=['POST'])
@login_required
@roles_required(USER)
def add_thought():
    content = request.form["thought"]
    if content != "":
        t = Thought(content=content)
        t.createdBy = current_user
        db.session.add(t)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        thoughts = Thought.query.all()
        return render_template('index.html', table=thoughts, invalid_input=True)

class SecurityException(Exception):
    def __init__(self, msg):
        self.msg = msg

def check_delete(self,caller):
    if self.createdBy.id != caller.id:
        raise SecurityException("You are not allowed to delete this thought: Not own thought")    

@app.route('/delete_thought')
@login_required
@roles_required(USER)
def delete_thought():
    id = request.args["id"]
    try: 
        i = int(id)
        t = Thought.query.get(i)
        if t != None:
            try:
                check_delete(t,current_user)
                db.session.delete(t)
                db.session.commit()
            except SecurityException as se:
                thoughts = Thought.query.all()
                return render_template('index.html', table=thoughts, security_violation=True,message=se.msg)
        return redirect(url_for('index'))
    except:
        return redirect(url_for('index'))

def check_vote(self,caller):
    # cannot vote for their own thought
    if self.createdBy.id==caller.id:
        raise SecurityException("You are not allowed to vote for this thought: Own thought")
    # cannot vote for a thought more than 3 times
    if len([x for x in caller.voted if x.votee==self]) >= 3:
        raise SecurityException("You are not allowed to vote for this thought: Too many votes")


@app.route('/vote_thought')
@login_required
@roles_required(USER)
def vote_thought():
    id = request.args["id"]
    try: 
        i = int(id)
        t = Thought.query.get(i)
        c = current_user
        if t != None and c != None:
            try:
                check_vote(t,c)
                v = Vote(voter=c, votee=t)
                db.session.add(v)
                db.session.commit()
                return redirect(url_for('index'))
            except SecurityException as se:
                thoughts = Thought.query.all()
                return render_template('index.html', table=thoughts, security_violation=True,message=se.msg)
            
    except:
        return redirect(url_for('index'))





