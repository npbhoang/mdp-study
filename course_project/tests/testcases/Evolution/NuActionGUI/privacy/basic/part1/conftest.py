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
                testid='MODERATOR1',
                name = 'MODERATOR1', 
                surname = 'MODERATOR1', 
                username = 'MODERATOR1', 
                password = 'MODERATOR1', 
                gender = 'male', 
                email = 'MODERATOR1@gmail.com', 
            ), 
            Person(
                id=4,
                testid='ADMIN0',
                name = 'ADMIN0', 
                surname = 'ADMIN0', 
                username = 'ADMIN0', 
                password = 'ADMIN0', 
                gender = 'male', 
                email = 'ADMIN0@gmail.com', 
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
                id=8,
                testid='e1',
                title = 'e1', 
                description = 'e1', 
            ), 
            Event(
                id=9,
                testid='e2',
                title = 'e2', 
                description = 'e2', 
            ), 
            Event(
                id=10,
                testid='e3',
                title = 'e3', 
                description = 'e3', 
            ), 
            Category(
                id=18,
                testid='c1',
                name = 'c1'
            ), 
            Category(
                id=19,
                testid='c2',
                name = 'c2'
            ), 
            Ad(
                id=24,
                testid='a1',
                content = 'a1'
            )
        ]
        db.session.bulk_save_objects(objects)
        
        
        FREEUSER0 = db.session.query(Person).filter(Person.testid == 'FREEUSER0').one()
        MODERATOR0 = db.session.query(Person).filter(Person.testid == 'MODERATOR0').one()
        MODERATOR1 = db.session.query(Person).filter(Person.testid == 'MODERATOR1').one()
        ADMIN0 = db.session.query(Person).filter(Person.testid == 'ADMIN0').one()
        p1 = db.session.query(Person).filter(Person.testid == 'p1').one()
        e1 = db.session.query(Event).filter(Event.testid == 'e1').one()
        e2 = db.session.query(Event).filter(Event.testid == 'e2').one()
        e3 = db.session.query(Event).filter(Event.testid == 'e3').one()
        c1 = db.session.query(Category).filter(Category.testid == 'c1').one()
        c2 = db.session.query(Category).filter(Category.testid == 'c2').one()
        a1 = db.session.query(Ad).filter(Ad.testid == 'a1').one()
        FREEUSER0.role = regularuserrole
        MODERATOR0.role = moderatorrole
        MODERATOR1.role = moderatorrole
        ADMIN0.role = adminrole
        p1.role = regularuserrole
        e1.owner = p1
        e2.owner = p1
        e3.owner = p1
        e1.attendants.append(p1)
        e1.managedBy.append(p1)
        e2.attendants.append(p1)
        e2.attendants.append(FREEUSER0)
        e2.attendants.append(MODERATOR0)
        e2.attendants.append(ADMIN0)
        e2.managedBy.append(p1)
        e2.managedBy.append(FREEUSER0)
        e2.managedBy.append(MODERATOR0)
        e2.managedBy.append(ADMIN0)
        e3.attendants.append(p1)
        e3.attendants.append(FREEUSER0)
        e3.attendants.append(MODERATOR0)
        e3.attendants.append(ADMIN0)
        e3.managedBy.append(p1)
        c1.subscribers.append(FREEUSER0)
        c1.subscribers.append(MODERATOR0)
        c1.subscribers.append(ADMIN0)
        c1.subscribers.append(p1)
        c1.events.append(e1)
        c2.subscribers.append(FREEUSER0)
        c2.subscribers.append(MODERATOR0)
        c2.subscribers.append(ADMIN0)
        c2.subscribers.append(p1)
        c2.subscribers.append(MODERATOR1)
        c2.moderators.append(MODERATOR1)
        c2.events.append(e1)

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

