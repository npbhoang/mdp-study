import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from flask import Flask, render_template, redirect, url_for, request, jsonify, Response
from flask_user import UserManager, user_registered, login_required, current_user

from dtm import *
from instrumentation import secure, Restrict
from ptm import EventPlatformNAGPrivacyModel
import logging

from flask import Response

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

    db.init_app(app)

    with app.app_context():
        db.drop_all()
        db.create_all()

        roles = Role.query.all()
        if len(roles) == 0:
            db.session.add(Role(name=VISITOR))
            db.session.add(Role(name=REGULARUSER))
            db.session.add(Role(name=MODERATOR))
            db.session.add(Role(name=ADMIN))
            db.session.commit()

        purposes = Purpose.query.all()
        if len(purposes) == 0:
            db.session.commit()
            
        personaldata = PersonalData.query.all()
        if len(personaldata) == 0:
            db.session.commit()

        visitorrole = db.session.get(Role, 1)
        regularuserrole = db.session.get(Role, 2)
        moderatorrole = db.session.get(Role, 3)
        adminrole = db.session.get(Role, 4)

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
                testid='p0',
                name = 'p0', 
                surname = 'p0', 
                username = 'p0', 
                password = 'p0', 
                gender = 'male', 
                email = 'p0@gmail.com', 
            ), 
            Person(
                id=5,
                testid='p1',
                name = 'p1', 
                surname = 'p1', 
                username = 'p1', 
                password = 'p1', 
                gender = 'male', 
                email = 'p1@gmail.com', 
            ), 
            Event(
                id=6,
                testid='e1',
                title = 'e1', 
                description = 'e1', 
            ), 
            Event(
                id=7,
                testid='e2',
                title = 'e2', 
                description = 'e2', 
            ), 
            Event(
                id=8,
                testid='e3',
                title = 'e3', 
                description = 'e3', 
            ), 
            Event(
                id=9,
                testid='e4',
                title = 'e4', 
                description = 'e4', 
            ),
            Invite(
                id=10,
                testid='i1'
            ),
            Invite(
                id=11,
                testid='i2'
            ),
            Invite(
                id=12,
                testid='i3'
            ),
            Event(
                id=13,
                testid='e5',
                title = 'e5', 
                description = 'e5', 
            ),
            Event(
                id=14,
                testid='e6',
                title = 'e6', 
                description = 'e6', 
            ),
            Event(
                id=15,
                testid='e7',
                title = 'e7', 
                description = 'e7', 
            ),
            Event(
                id=16,
                testid='e8',
                title = 'e8', 
                description = 'e8', 
            ),
            Event(
                id=17,
                testid='e9',
                title = 'e9', 
                description = 'e9', 
            ),
            Invite(
                id=18,
                testid='i4'
            ),
            Category(
                id=19,
                name = 'c0'
            ),
            Invite(
                id=20,
                testid='i5'
            ),
            Person(
                id=21,
                testid='ADMIN1',
                name = 'ADMIN1', 
                surname = 'ADMIN1', 
                username = 'ADMIN1', 
                password = 'ADMIN1', 
                gender = 'male', 
                email = 'ADMIN1@gmail.com', 
            )
        ]
        db.session.bulk_save_objects(objects)
        
        
        FREEUSER0 = db.session.query(Person).filter(Person.testid == 'FREEUSER0').one()
        MODERATOR0 = db.session.query(Person).filter(Person.testid == 'MODERATOR0').one()
        ADMIN0 = db.session.query(Person).filter(Person.testid == 'ADMIN0').one()
        ADMIN1 = db.session.query(Person).filter(Person.testid == 'ADMIN1').one()
        p0 = db.session.query(Person).filter(Person.testid == 'p0').one()
        p1 = db.session.query(Person).filter(Person.testid == 'p1').one()
        e1 = db.session.query(Event).filter(Event.testid == 'e1').one()
        e2 = db.session.query(Event).filter(Event.testid == 'e2').one()
        e3 = db.session.query(Event).filter(Event.testid == 'e3').one()
        e4 = db.session.query(Event).filter(Event.testid == 'e4').one()
        e5 = db.session.query(Event).filter(Event.testid == 'e5').one()
        e6 = db.session.query(Event).filter(Event.testid == 'e6').one()
        e7 = db.session.query(Event).filter(Event.testid == 'e7').one()
        e8 = db.session.query(Event).filter(Event.testid == 'e8').one()
        e9 = db.session.query(Event).filter(Event.testid == 'e9').one()
        c0 = db.session.query(Category).filter(Category.id == 19).one()
        i1 = db.session.query(Invite).filter(Invite.testid == 'i1').one()
        i2 = db.session.query(Invite).filter(Invite.testid == 'i2').one()
        i3 = db.session.query(Invite).filter(Invite.testid == 'i3').one()
        i4 = db.session.query(Invite).filter(Invite.testid == 'i4').one()
        i5 = db.session.query(Invite).filter(Invite.testid == 'i5').one()
        i1.event = e4
        i2.event = e4
        i3.event = e4
        i4.event = e9
        i1.invitedBy = p1
        i2.invitedBy = p1
        i3.invitedBy = p1
        i4.invitedBy = p1
        i1.invitee = FREEUSER0
        i2.invitee = MODERATOR0
        i3.invitee = ADMIN0
        i4.invitee = p0
        i5.event = e6
        i5.invitedBy = p1
        i5.invitee = p0
        FREEUSER0.role = regularuserrole
        MODERATOR0.role = moderatorrole
        ADMIN0.role = adminrole
        ADMIN1.role = adminrole
        p0.role = regularuserrole
        p1.role = regularuserrole
        e1.owner = FREEUSER0
        e2.owner = MODERATOR0
        e3.owner = ADMIN0
        e4.owner = p1
        e5.owner = p1
        e6.owner = p1
        e7.owner = p1
        e8.owner = p1
        e9.owner = p1
        e1.attendants.append(FREEUSER0)
        e1.managedBy.append(FREEUSER0)
        e2.attendants.append(MODERATOR0)
        e2.managedBy.append(MODERATOR0)
        e3.attendants.append(ADMIN0)
        e3.managedBy.append(ADMIN0)
        e4.attendants.append(p1)
        e4.managedBy.append(p1)
        e5.attendants.append(p1)
        e5.managedBy.append(p1)
        e5.attendants.append(FREEUSER0)
        e5.managedBy.append(FREEUSER0)
        e5.attendants.append(MODERATOR0)
        e5.managedBy.append(MODERATOR0)
        e5.attendants.append(ADMIN0)
        e5.managedBy.append(ADMIN0)
        e6.attendants.append(p1)
        e6.managedBy.append(p1)
        e6.attendants.append(FREEUSER0)
        e6.attendants.append(MODERATOR0)
        e6.attendants.append(ADMIN0)
        e7.attendants.append(p1)
        e7.managedBy.append(p1)
        e7.requesters.append(FREEUSER0)
        e7.requesters.append(MODERATOR0)
        e7.requesters.append(ADMIN0)
        e8.attendants.append(p1)
        e8.managedBy.append(p1)
        e9.attendants.append(p1)
        e9.managedBy.append(p1)
        e9.attendants.append(FREEUSER0)
        e9.managedBy.append(FREEUSER0)
        e9.attendants.append(MODERATOR0)
        e9.managedBy.append(MODERATOR0)
        e9.attendants.append(ADMIN0)
        e9.managedBy.append(ADMIN0)
        e9.requesters.append(p0)
        c0.subscribers.append(FREEUSER0)
        c0.subscribers.append(MODERATOR0)
        c0.subscribers.append(ADMIN0)
        c0.subscribers.append(p0)

        db.session.commit()

    UserManager(app, db, Person, RoleClass=Role)

    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    return app

@pytest.fixture
def client(app_with_data):
    return app_with_data.test_client()

