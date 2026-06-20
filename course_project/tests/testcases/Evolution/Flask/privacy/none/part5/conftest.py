import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from flask import Flask, render_template, redirect, url_for
from flask_user import UserManager
from model import *
from app import SecurityException
from flask import Response
from flask_principal import Principal, identity_loaded
from project import PRIVACY_INPUT

@pytest.fixture(scope='function')
def app_with_data():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testingapp.db'
    app.config['USER_APP_NAME'] = "Event Platform Testing"
    app.config['USER_ENABLE_EMAIL'] = False      
    app.config['USER_ENABLE_USERNAME'] = True    
    app.config['USER_REQUIRE_RETYPE_PASSWORD'] = False
    app.config['SECRET_KEY'] = '_5#yfasQ8sansaxec/][#1'
    app.config['USER_UNAUTHORIZED_ENDPOINT'] = 'error'
    app.config['SERVER_NAME'] = 'localhost'
    app.config['TESTING']=True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    principals = Principal(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        from project import on_identity_loaded
        return on_identity_loaded(sender, identity)

    def secure(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except SecurityException as se:
                db.session.rollback()
                return render_template(se.page, security_violation = True, msg = se.msg, **se.params)
        wrapper.__name__ = func.__name__
        return wrapper

    @app.route('/error')
    def error():
        msg = "The message does not matter!"
        return render_template('error.html', message = msg)

    @app.route('/')
    @secure
    def main():
        from project import main 
        result=main()
        if type(result) == Response:
            return result
        else: 
            return render_template('main.html', **result)
        

    @app.route('/profile')
    @secure
    def profile():
        from project import profile 
        result=profile()
        if type(result) == Response:
            return result
        else: 
            return render_template('profile.html', **result)
        

    @app.route('/events')
    @secure
    def events():
        from project import events 
        result=events()
        if type(result) == Response:
            return result
        else: 
            return render_template('events.html', **result)


    @app.route('/view_event/<int:id>')
    @secure
    def view_event(id):
        from project import view_event 
        result=view_event(id)
        if type(result) == Response:
            return result
        else: 
            return render_template('view_event.html', **result)


    @app.route('/edit_event/<int:id>')
    @secure
    def edit_event(id):
        from project import edit_event 
        result=edit_event(id)
        if type(result) == Response:
            return result
        else: 
            return render_template('edit_event.html', **result)


    @app.post('/update_event')
    @secure
    def update_event():
        from project import update_event 
        result=update_event()
        if type(result) == Response:
            return result
        else: 
            return redirect(url_for('edit_event',id=result))



    @app.route('/join/<int:id>')
    @secure
    def join(id):
        from project import join 
        result=join(id)
        if type(result) == Response:
            return result
        else: 
            return redirect(url_for('events'))


    @app.route('/leave/<int:id>')
    @secure
    def leave(id):
        from project import leave 
        result=leave(id)
        if type(result) == Response:
            return result
        else: 
            return redirect(url_for('profile'))


    @app.post('/create_event')
    @secure
    def create_event():
        from project import create_event 
        result=create_event()
        if type(result) == Response:
            return result
        else: 
            return redirect(url_for('events'))


    @app.route('/manage_event/<int:id>')
    @secure
    def manage_event(id):
        from project import manage_event 
        result=manage_event(id)
        if type(result) == Response:
            return result
        else: 
            return render_template('manage_event.html', **result)


    @app.route('/categories')
    @secure
    def categories():
        from project import categories 
        result=categories()
        if type(result) == Response:
            return result
        else: 
            return render_template('categories.html', **result)


    @app.route('/view_category/<int:id>')
    @secure
    def view_category(id):
        from project import view_category 
        result=view_category(id)
        if type(result) == Response:
            return result
        else: 
            return render_template('view_category.html', **result)


    @app.route('/remove_category/<int:id>/<int:c>')
    @secure
    def remove_category(id,c):
        from project import remove_category 
        result=remove_category(id,c)
        if type(result) == Response:
            return result
        else: 
            return redirect(url_for('view_category',id=c))


    @app.route('/edit_category/<int:id>')
    @secure
    def edit_category(id):
        from project import edit_category 
        result=edit_category(id)
        if type(result) == Response:
            return result
        else: 
            return render_template('edit_category.html', **result)


    @app.route('/add_moderator/<int:id>/<int:c>')
    @secure
    def add_moderator(id,c):
        from project import add_moderator 
        result=add_moderator(id,c)
        if type(result) == Response:
            return result
        else: 
            return redirect(url_for('edit_category',id=c))


    @app.route('/remove_moderator/<int:id>/<int:c>')
    @secure
    def remove_moderator(id,c):
        from project import remove_moderator 
        result=remove_moderator(id,c)
        if type(result) == Response:
            return result
        else: 
            return redirect(url_for('edit_category',id=c))


    @app.post('/update_category')
    @secure
    def update_category():
        from project import update_category 
        result=update_category()
        if type(result) == Response:
            return result
        else: 
            return redirect(url_for('edit_category',id=result))
    

    @app.route('/subscribe/<int:id>')
    @secure
    def subscribe(id):
        from project import subscribe 
        result=subscribe(id)
        if type(result) == Response:
            return result
        else: 
            return redirect(url_for('categories'))


    @app.route('/unsubscribe/<int:id>')
    @secure
    def unsubscribe(id):
        from project import unsubscribe 
        result=unsubscribe(id)
        if type(result) == Response:
            return result
        else: 
            return redirect(url_for('profile'))


    @app.post('/create_category')
    @secure
    def create_category():
        from project import create_category 
        result=create_category()
        if type(result) == Response:
            return result
        else: 
            return redirect(url_for('categories'))


    @app.route('/users')
    @secure
    def users():
        from project import users
        result=users()
        if type(result) == Response:
            return result
        else: 
            return render_template('users.html', **result) 
        

    @app.route('/user/<int:id>')
    @secure
    def user(id):
        from project import user 
        result=user(id)
        if type(result) == Response:
            return result
        else: 
            return render_template('user.html', **result) 
        

    @app.post('/update_user')
    @secure
    def update_user():
        from project import update_user 
        result=update_user()
        if type(result) == Response:
            return result
        else: 
            return redirect(url_for('user',id=result))


    @app.route('/promote_manager/<int:id>/<int:e>')
    @secure
    def promote_manager(id,e):
        from project import promote_manager 
        result=promote_manager(id,e)
        if type(result) == Response:
            return result
        else: 
            return redirect(url_for('manage_event',id=e))


    @app.route('/demote_manager/<int:id>/<int:e>')
    @secure
    def demote_manager(id,e):
        from project import demote_manager 
        result=demote_manager(id,e)
        if type(result) == Response:
            return result
        else: 
            return redirect(url_for('manage_event',id=e))


    @app.route('/remove_attendee/<int:id>/<int:e>')
    @secure
    def remove_attendee(id,e):
        from project import remove_attendee 
        result=remove_attendee(id,e)
        if type(result) == Response:
            return result
        else: 
            return redirect(url_for('manage_event',id=e))


    @app.route('/accept_request/<int:id>/<int:e>')
    @secure
    def accept_request(id,e):
        from project import accept_request 
        result=accept_request(id,e)
        if type(result) == Response:
            return result
        else: 
            return redirect(url_for('manage_event',id=e))


    @app.route('/reject_request/<int:id>/<int:e>')
    @secure
    def reject_request(id,e):
        from project import reject_request 
        result=reject_request(id,e)
        if type(result) == Response:
            return result
        else: 
            return redirect(url_for('manage_event',id=e))

    @app.route('/personalized_stats/<int:id>')
    @secure
    def personalized_stats(id):
        from project import personalized_stats 
        result=personalized_stats(id)
        if type(result) == Response:
            return result
        else: 
            return render_template('personalized_stats.html', **result)

    @app.route('/send_invite/<int:id>/<int:e>')
    @secure
    def send_invite(id,e):
        from project import send_invite 
        result=send_invite(id,e)
        if type(result) == Response:
            return result
        else: 
            return redirect(url_for('manage_event',id=e))


    @app.route('/accept_invitation/<int:id>')
    @secure
    def accept_invitation(id):
        from project import accept_invitation 
        result=accept_invitation(id)
        if type(result) == Response:
            return result
        else: 
            return redirect(url_for('profile'))


    @app.route('/decline_invitation/<int:id>')
    @secure
    def decline_invitation(id):
        from project import decline_invitation 
        result=decline_invitation(id)
        if type(result) == Response:
            return result
        else: 
            return redirect(url_for('profile'))

    db.init_app(app)

    with app.app_context():
        db.drop_all()
        db.create_all()

        def add_all_consent(user):
            def process_purpose(purpose_name, purpose_data, user):
                # Add consents for the current purpose's data
                for class_name, property_name in purpose_data.get("data", []):
                    my_purpose = Purpose.query.filter_by(name=purpose_name).first()
                    if my_purpose:
                        consent = Consent(
                            classname=class_name,
                            propertyname=property_name,
                            user=user,
                            purpose=my_purpose
                        )
                        db.session.add(consent)

                # Recursively process child purposes
                for child_purpose_name, child_purpose_data in purpose_data.get("children", {}).items():
                    process_purpose(child_purpose_name, child_purpose_data, user)

            # Start processing from the root purpose
            for root_purpose_name, root_purpose_data in PRIVACY_INPUT.items():
                process_purpose(root_purpose_name, root_purpose_data, user)

            # Commit all changes to the database
            db.session.commit()

        roles = [
            Role(id=1, name="REGULARUSER"),
            Role(id=2, name="MODERATOR"),
            Role(id=3, name="ADMIN"),
        ]
        db.session.bulk_save_objects(roles)

        PURPOSES = [
            AnyPurpose,
            FunctionalPurpose,
            MarketingPurpose,
            AnalyticsPurpose,
            CorePurpose,
            RecommendEventsPurpose,
            TargetedMarketingPurpose,
            MassMarketingPurpose,
            InsightsPurpose,
            StatsPurpose
        ]

        purposes = Purpose.query.all()
        if len(purposes) == 0:
            for iPurpose, name in enumerate(PURPOSES):
                db.session.add(Purpose(id=iPurpose+1, name=name))
            db.session.commit()
        
        regularuserrole = db.session.get(Role, 1)
        moderatorrole = db.session.get(Role, 2)
        adminrole = db.session.get(Role, 3)

        objects = [
            Person(
                id=1,
                testid='FREEUSER0',
                name = 'FREEUSER0', 
                surname = 'FREEUSER0', 
                username = 'FREEUSER0', 
                password = 'FREEUSER0', 
                gender = 'male', 
                email = 'FREEUSER0@gmail.com', 
            ), 
            Person(
                id=2,
                testid='MODERATOR0',
                name = 'MODERATOR0', 
                surname = 'MODERATOR0', 
                username = 'MODERATOR0', 
                password = 'MODERATOR0', 
                gender = 'male', 
                email = 'MODERATOR0@gmail.com', 
            ), 
            Person(
                id=3,
                testid='ADMIN0',
                name = 'ADMIN0', 
                surname = 'ADMIN0', 
                username = 'ADMIN0', 
                password = 'ADMIN0', 
                gender = 'male', 
                email = 'ADMIN0@gmail.com', 
            ), 
            Person(
                id=4,
                testid='p1',
                name = 'p1', 
                surname = 'p1', 
                username = 'p1', 
                password = 'p1', 
                gender = 'male', 
                email = 'p1@gmail.com', 
            ), 
            Person(
                id=5,
                testid='p2',
                name = 'p2', 
                surname = 'p2', 
                username = 'p2', 
                password = 'p2', 
                gender = 'male', 
                email = 'p2@gmail.com', 
            ), 
            Person(
                id=6,
                testid='p3',
                name = 'p3', 
                surname = 'p3', 
                username = 'p3', 
                password = 'p3', 
                gender = 'male', 
                email = 'p3@gmail.com', 
            ), 
            Event(
                id=7,
                testid='e1',
                title = 'e1', 
                description = 'e1', 
            ), 
            Event(
                id=8,
                testid='e2',
                title = 'e2', 
                description = 'e2', 
            ), 
            Event(
                id=9,
                testid='e3',
                title = 'e3', 
                description = 'e3', 
            ), 
            Event(
                id=10,
                testid='e4',
                title = 'e4', 
                description = 'e4', 
            ), 
            Event(
                id=11,
                testid='e5',
                title = 'e5', 
                description = 'e5', 
            ), 
            Event(
                id=12,
                testid='e6',
                title = 'e6', 
                description = 'e6', 
            ),
            Event(
                id=13,
                testid='e7',
                title = 'e7', 
                description = 'e7', 
            ),
            Person(
                id=14,
                testid='p0',
                name = 'p0', 
                surname = 'p0', 
                username = 'p0', 
                password = 'p0', 
                gender = 'male', 
                email = 'p0@gmail.com', 
            ), 
        ]
        db.session.bulk_save_objects(objects)
        
        
        FREEUSER0 = db.session.query(Person).filter(Person.testid == 'FREEUSER0').one()
        MODERATOR0 = db.session.query(Person).filter(Person.testid == 'MODERATOR0').one()
        ADMIN0 = db.session.query(Person).filter(Person.testid == 'ADMIN0').one()
        p0 = db.session.query(Person).filter(Person.testid == 'p0').one()
        p1 = db.session.query(Person).filter(Person.testid == 'p1').one()
        p2 = db.session.query(Person).filter(Person.testid == 'p2').one()
        p3 = db.session.query(Person).filter(Person.testid == 'p3').one()
        e1 = db.session.query(Event).filter(Event.testid == 'e1').one()
        e2 = db.session.query(Event).filter(Event.testid == 'e2').one()
        e3 = db.session.query(Event).filter(Event.testid == 'e3').one()
        e4 = db.session.query(Event).filter(Event.testid == 'e4').one()
        e5 = db.session.query(Event).filter(Event.testid == 'e5').one()
        e6 = db.session.query(Event).filter(Event.testid == 'e6').one()
        e7 = db.session.query(Event).filter(Event.testid == 'e7').one()
        FREEUSER0.role = regularuserrole
        MODERATOR0.role = moderatorrole
        ADMIN0.role = adminrole
        p0.role = regularuserrole
        p1.role = regularuserrole
        p2.role = regularuserrole
        p3.role = regularuserrole
        e1.owner = FREEUSER0
        e2.owner = MODERATOR0
        e3.owner = ADMIN0
        e4.owner = p0
        e5.owner = p0
        e6.owner = p0
        e7.owner = p0
        e1.attendants.append(FREEUSER0)
        e1.managedBy.append(FREEUSER0)
        e2.attendants.append(MODERATOR0)
        e2.managedBy.append(MODERATOR0)
        e3.attendants.append(ADMIN0)
        e3.managedBy.append(ADMIN0)
        e4.attendants.append(p0)
        e4.managedBy.append(p0)
        e4.attendants.append(FREEUSER0)
        e4.managedBy.append(FREEUSER0)
        e4.attendants.append(MODERATOR0)
        e4.managedBy.append(MODERATOR0)
        e4.attendants.append(ADMIN0)
        e4.managedBy.append(ADMIN0)
        e5.attendants.append(p0)
        e5.managedBy.append(p0)
        e5.attendants.append(FREEUSER0)
        e5.attendants.append(MODERATOR0)
        e5.attendants.append(ADMIN0)
        e6.attendants.append(p0)
        e6.managedBy.append(p0)
        e6.requesters.append(FREEUSER0)
        e6.requesters.append(MODERATOR0)
        e6.requesters.append(ADMIN0)
        e7.attendants.append(p0)
        e7.managedBy.append(p0)
        e1.requesters.append(p1)
        e2.requesters.append(p1)
        e3.requesters.append(p1)
        e4.requesters.append(p1)
        e5.requesters.append(p1)
        e6.requesters.append(p1)
        e7.requesters.append(p1)
        e6.attendants.append(p2)
        e7.attendants.append(p3)

        db.session.commit()



    UserManager(app, db, Person, RoleClass=Role)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    return app

@pytest.fixture
def client(app_with_data):
    return app_with_data.test_client()

