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
            Person(
                id=6,
                testid='p2',
                name = 'p2', 
                surname = 'p2', 
                username = 'p2', 
                password = 'p2', 
                gender = 'male', 
                email = 'p2@gmail.com', 
            ), 
            Person(
                id=7,
                testid='p3',
                name = 'p3', 
                surname = 'p3', 
                username = 'p3', 
                password = 'p3', 
                gender = 'male', 
                email = 'p3@gmail.com', 
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
            Event(
                id=11,
                testid='e4',
                title = 'e4', 
                description = 'e4', 
            ), 
            Event(
                id=12,
                testid='e5',
                title = 'e5', 
                description = 'e5', 
            ), 
            Event(
                id=13,
                testid='e7',
                title = 'e7', 
                description = 'e7', 
            ), 
            Event(
                id=14,
                testid='e8',
                title = 'e8', 
                description = 'e8', 
            ), 
            Event(
                id=15,
                testid='e9',
                title = 'e9', 
                description = 'e9', 
            ), 
            Event(
                id=16,
                testid='e10',
                title = 'e10', 
                description = 'e10', 
            ), 
            Event(
                id=17,
                testid='e11',
                title = 'e11', 
                description = 'e11', 
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
            Category(
                id=20,
                testid='c3',
                name = 'c3'
            ), 
            Category(
                id=21,
                testid='c4',
                name = 'c4'
            ), 
            Category(
                id=22,
                testid='c5',
                name = 'c5'
            ), 
            Category(
                id=23,
                testid='c6',
                name = 'c6'
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
        p2 = db.session.query(Person).filter(Person.testid == 'p2').one()
        p3 = db.session.query(Person).filter(Person.testid == 'p3').one()
        e1 = db.session.query(Event).filter(Event.testid == 'e1').one()
        e2 = db.session.query(Event).filter(Event.testid == 'e2').one()
        e3 = db.session.query(Event).filter(Event.testid == 'e3').one()
        e4 = db.session.query(Event).filter(Event.testid == 'e4').one()
        e5 = db.session.query(Event).filter(Event.testid == 'e5').one()
        e7 = db.session.query(Event).filter(Event.testid == 'e7').one()
        e8 = db.session.query(Event).filter(Event.testid == 'e8').one()
        e9 = db.session.query(Event).filter(Event.testid == 'e9').one()
        e10 = db.session.query(Event).filter(Event.testid == 'e10').one()
        e11 = db.session.query(Event).filter(Event.testid == 'e11').one()
        c1 = db.session.query(Category).filter(Category.testid == 'c1').one()
        c2 = db.session.query(Category).filter(Category.testid == 'c2').one()
        c3 = db.session.query(Category).filter(Category.testid == 'c3').one()
        c4 = db.session.query(Category).filter(Category.testid == 'c4').one()
        c5 = db.session.query(Category).filter(Category.testid == 'c5').one()
        c6 = db.session.query(Category).filter(Category.testid == 'c6').one()
        a1 = db.session.query(Ad).filter(Ad.testid == 'a1').one()
        FREEUSER0.role = regularuserrole
        MODERATOR0.role = moderatorrole
        MODERATOR1.role = moderatorrole
        ADMIN0.role = adminrole
        p1.role = regularuserrole
        p2.role = moderatorrole
        p3.role = adminrole
        e1.owner = p1
        e2.owner = p1
        e3.owner = p1
        e4.owner = p1
        e5.owner = p1
        e7.owner = FREEUSER0
        e8.owner = MODERATOR0
        e9.owner = ADMIN0
        e10.owner = p1
        e11.owner = p1
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
        e4.attendants.append(p1)
        e4.managedBy.append(p1)
        e5.attendants.append(p1)
        e5.attendants.append(FREEUSER0)
        e5.attendants.append(MODERATOR0)
        e5.attendants.append(ADMIN0)
        e5.managedBy.append(p1)
        e7.attendants.append(FREEUSER0)
        e7.managedBy.append(FREEUSER0)
        e8.attendants.append(MODERATOR0)
        e8.managedBy.append(MODERATOR0)
        e9.attendants.append(ADMIN0)
        e9.managedBy.append(ADMIN0)
        e10.requesters.append(FREEUSER0)
        e10.requesters.append(MODERATOR0)
        e10.requesters.append(ADMIN0)
        e10.attendants.append(p1)
        e10.managedBy.append(p1)
        e11.attendants.append(p1)
        e11.managedBy.append(p1)
        c1.subscribers.append(FREEUSER0)
        c1.subscribers.append(MODERATOR0)
        c1.subscribers.append(ADMIN0)
        c1.subscribers.append(p1)
        c1.events.append(e1)
        c2.subscribers.append(FREEUSER0)
        c2.subscribers.append(MODERATOR0)
        c2.subscribers.append(ADMIN0)
        c2.subscribers.append(p1)
        c2.moderators.append(MODERATOR1)
        c2.events.append(e1)
        c4.moderators.append(p2)
        c5.moderators.append(MODERATOR0)
        c6.subscribers.append(FREEUSER0)
        c6.subscribers.append(MODERATOR0)
        c6.subscribers.append(ADMIN0)

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

