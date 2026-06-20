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
                username = 'FREEUSER0', 
                password = 'FREEUSER0', 
            ), 
            Person(
                id=2,
                testid='MODERATOR0',
                username = 'MODERATOR0', 
                password = 'MODERATOR0', 
            ), 
            Person(
                id=99,
                testid='MODERATOR1',
                username = 'MODERATOR1', 
                password = 'MODERATOR1', 
            ), 
            Person(
                id=3,
                testid='ADMIN0',
                username = 'ADMIN0', 
                password = 'ADMIN0', 
            ), 
            Person(
                id=4,
                testid='FREEUSER44',
                name = 'FREEUSER44', 
                surname = 'FREEUSER44', 
                username = 'FREEUSER44', 
                password = 'FREEUSER44', 
                gender = 'male', 
                email = 'FREEUSER44@gmail.com', 
            ),
            Person(
                id=5,
                testid='MODERATOR44',
                name = 'MODERATOR44',
                surname = 'MODERATOR44',
                username = 'MODERATOR44',
                password = 'MODERATOR44',
                gender = 'male',
                email = 'MODERATOR44@gmail.com'
            ),
            Person(
                id=6,
                testid='ADMIN44',
                name = 'ADMIN44',
                surname = 'ADMIN44',
                username = 'ADMIN44',
                password = 'ADMIN44',
                gender = 'male',
                email = 'ADMIN44@gmail.com'
            ),
            Person(
                id=7,
                testid='FREEUSER45',
                name = 'FREEUSER45', 
                surname = 'FREEUSER45', 
                username = 'FREEUSER45', 
                password = 'FREEUSER45', 
                gender = 'male', 
                email = 'FREEUSER45@gmail.com', 
            ),
            Person(
                id=8,
                testid='MODERATOR45',
                name = 'MODERATOR45',
                surname = 'MODERATOR45',
                username = 'MODERATOR45',
                password = 'MODERATOR45',
                gender = 'male',
                email = 'MODERATOR45@gmail.com'
            ),
            Person(
                id=9,
                testid='ADMIN45',
                name = 'ADMIN45',
                surname = 'ADMIN45',
                username = 'ADMIN45',
                password = 'ADMIN45',
                gender = 'male',
                email = 'ADMIN45@gmail.com'
            ),
            Person(id=10, testid='FREEUSER46', name='FREEUSER46', surname='FREEUSER46', username='FREEUSER46', password='FREEUSER46', gender='male', email='FREEUSER46@gmail.com'),
            Person(id=11, testid='MODERATOR46', name='MODERATOR46', surname='MODERATOR46', username='MODERATOR46', password='MODERATOR46', gender='male', email='MODERATOR46@gmail.com'),
            Person(id=12, testid='ADMIN46', name='ADMIN46', surname='ADMIN46', username='ADMIN46', password='ADMIN46', gender='male', email='ADMIN46@gmail.com'),
            Person(id=13, testid='FREEUSER47', surname='FREEUSER47', username='FREEUSER47', password='FREEUSER47', gender='male', email='FREEUSER47@gmail.com'),
            Person(id=14, testid='MODERATOR47', surname='MODERATOR47', username='MODERATOR47', password='MODERATOR47', gender='male', email='MODERATOR47@gmail.com'),
            Person(id=15, testid='ADMIN47', surname='ADMIN47', username='ADMIN47', password='ADMIN47', gender='male', email='ADMIN47@gmail.com'),
            Person(id=16, testid='FREEUSER48', name='FREEUSER48', surname='FREEUSER48', username='FREEUSER48', password='FREEUSER48', gender='male', email='FREEUSER48@gmail.com'),
            Person(id=17, testid='MODERATOR48', name='MODERATOR48', surname='MODERATOR48', username='MODERATOR48', password='MODERATOR48', gender='male', email='MODERATOR48@gmail.com'),
            Person(id=18, testid='ADMIN48', name='ADMIN48', surname='ADMIN48', username='ADMIN48', password='ADMIN48', gender='male', email='ADMIN48@gmail.com'),
            Person(id=19, testid='FREEUSER49', name='FREEUSER49', username='FREEUSER49', password='FREEUSER49', gender='male', email='FREEUSER49@gmail.com'),
            Person(id=20, testid='MODERATOR49', name='MODERATOR49', username='MODERATOR49', password='MODERATOR49', gender='male', email='MODERATOR49@gmail.com'),
            Person(id=21, testid='ADMIN49', name='ADMIN49', username='ADMIN49', password='ADMIN49', gender='male', email='ADMIN49@gmail.com'),
            Person(id=22, testid='FREEUSER50', name='FREEUSER50', surname='FREEUSER50', username='FREEUSER50', password='FREEUSER50', gender='male', email='FREEUSER50@gmail.com'),
            Person(id=23, testid='MODERATOR50', name='MODERATOR50', surname='MODERATOR50', username='MODERATOR50', password='MODERATOR50', gender='male', email='MODERATOR50@gmail.com'),
            Person(id=24, testid='ADMIN50', name='ADMIN50', surname='ADMIN50', username='ADMIN50', password='ADMIN50', gender='male', email='ADMIN50@gmail.com'),
            Person(id=25, testid='FREEUSER51', name='FREEUSER51', surname='FREEUSER51', username='FREEUSER51', password='FREEUSER51', gender='male', email='FREEUSER51@gmail.com'),
            Person(id=26, testid='MODERATOR51', name='MODERATOR51', surname='MODERATOR51', username='MODERATOR51', password='MODERATOR51', gender='male', email='MODERATOR51@gmail.com'),
            Person(id=27, testid='ADMIN51', name='ADMIN51', surname='ADMIN51', username='ADMIN51', password='ADMIN51', gender='male', email='ADMIN51@gmail.com'),
            Person(id=28, testid='FREEUSER52', name='FREEUSER52', surname='FREEUSER52', username='FREEUSER52', password='FREEUSER52', gender='male', email='FREEUSER52@gmail.com'),
            Person(id=29, testid='MODERATOR52', name='MODERATOR52', surname='MODERATOR52', username='MODERATOR52', password='MODERATOR52', gender='male', email='MODERATOR52@gmail.com'),
            Person(id=30, testid='ADMIN52', name='ADMIN52', surname='ADMIN52', username='ADMIN52', password='ADMIN52', gender='male', email='ADMIN52@gmail.com'),
            Person(id=31, testid='FREEUSER53', name='FREEUSER53', surname='FREEUSER53', username='FREEUSER53', password='FREEUSER53', gender='male', email='FREEUSER53@gmail.com'),
            Person(id=32, testid='MODERATOR53', name='MODERATOR53', surname='MODERATOR53', username='MODERATOR53', password='MODERATOR53', gender='male', email='MODERATOR53@gmail.com'),
            Person(id=33, testid='ADMIN53', name='ADMIN53', surname='ADMIN53', username='ADMIN53', password='ADMIN53', gender='male', email='ADMIN53@gmail.com'),
            Person(id=34, testid='FREEUSER54', name='FREEUSER54', surname='FREEUSER54', username='FREEUSER54', password='FREEUSER54', gender='male', email='FREEUSER54@gmail.com'),
            Person(id=35, testid='MODERATOR54', name='MODERATOR54', surname='MODERATOR54', username='MODERATOR54', password='MODERATOR54', gender='male', email='MODERATOR54@gmail.com'),
            Person(id=36, testid='ADMIN54', name='ADMIN54', surname='ADMIN54', username='ADMIN54', password='ADMIN54', gender='male', email='ADMIN54@gmail.com'),
            Person(id=37, testid='FREEUSER55', name='FREEUSER55', surname='FREEUSER55', username='FREEUSER55', password='FREEUSER55', gender='male', email='FREEUSER55@gmail.com'),
            Person(id=38, testid='MODERATOR55', name='MODERATOR55', surname='MODERATOR55', username='MODERATOR55', password='MODERATOR55', gender='male', email='MODERATOR55@gmail.com'),
            Person(id=39, testid='ADMIN55', name='ADMIN55', surname='ADMIN55', username='ADMIN55', password='ADMIN55', gender='male', email='ADMIN55@gmail.com'),
            Person(id=40, testid='FREEUSER56', name='FREEUSER56', surname='FREEUSER56', username='FREEUSER56', password='FREEUSER56', gender='male', email='FREEUSER56@gmail.com'),
            Person(id=41, testid='MODERATOR56', name='MODERATOR56', surname='MODERATOR56', username='MODERATOR56', password='MODERATOR56', gender='male', email='MODERATOR56@gmail.com'),
            Person(id=42, testid='ADMIN56', name='ADMIN56', surname='ADMIN56', username='ADMIN56', password='ADMIN56', gender='male', email='ADMIN56@gmail.com'),
            Person(id=43, testid='FREEUSER57', name='FREEUSER57', surname='FREEUSER57', username='FREEUSER57', password='FREEUSER57', gender='male', email='FREEUSER57@gmail.com'),
            Person(id=46, testid='FREEUSER58', name='FREEUSER58', surname='FREEUSER58', username='FREEUSER58', password='FREEUSER58', gender='male', email='FREEUSER58@gmail.com'),
            Person(id=50, testid='MODERATOR59', name='MODERATOR59', surname='MODERATOR59', username='MODERATOR59', password='MODERATOR59', gender='male', email='MODERATOR59@gmail.com'),
            Person(id=53, testid='MODERATOR60', name='MODERATOR60', surname='MODERATOR60', username='MODERATOR60', password='MODERATOR60', gender='male', email='MODERATOR60@gmail.com'),
            Person(id=57, testid='ADMIN61', name='ADMIN61', surname='ADMIN61', username='ADMIN61', password='ADMIN61', gender='male', email='ADMIN61@gmail.com'),
            Person(id=60, testid='ADMIN62', name='ADMIN62', surname='ADMIN62', username='ADMIN62', password='ADMIN62', gender='male', email='ADMIN62@gmail.com'),
            Person(id=61, testid='FREEUSER63', name='FREEUSER63', surname='FREEUSER63', username='FREEUSER63', password='FREEUSER63', gender='male', email='FREEUSER63@gmail.com'),
            Person(id=62, testid='MODERATOR63', name='MODERATOR63', surname='MODERATOR63', username='MODERATOR63', password='MODERATOR63', gender='male', email='MODERATOR63@gmail.com'),
            Person(id=63, testid='ADMIN63', name='ADMIN63', surname='ADMIN63', username='ADMIN63', password='ADMIN63', gender='male', email='ADMIN63@gmail.com'),
            Person(id=64, testid='FREEUSER64', name='FREEUSER64', surname='FREEUSER64', username='FREEUSER64', password='FREEUSER64', gender='male', email='FREEUSER64@gmail.com'),
            Person(id=65, testid='MODERATOR64', name='MODERATOR64', surname='MODERATOR64', username='MODERATOR64', password='MODERATOR64', gender='male', email='MODERATOR64@gmail.com'),
            Person(id=66, testid='ADMIN64', name='ADMIN64', surname='ADMIN64', username='ADMIN64', password='ADMIN64', gender='male', email='ADMIN64@gmail.com'),
            Person(id=67, testid='FREEUSER65', name='FREEUSER65', surname='FREEUSER65', username='FREEUSER65', password='FREEUSER65', email='FREEUSER65@gmail.com'),
            Person(id=68, testid='MODERATOR65', name='MODERATOR65', surname='MODERATOR65', username='MODERATOR65', password='MODERATOR65', email='MODERATOR65@gmail.com'),
            Person(id=69, testid='ADMIN65', name='ADMIN65', surname='ADMIN65', username='ADMIN65', password='ADMIN65', email='ADMIN65@gmail.com'),
            Person(id=70, testid='FREEUSER66', name='FREEUSER66', surname='FREEUSER66', username='FREEUSER66', password='FREEUSER66', gender='male', email='FREEUSER66@gmail.com'),
            Person(id=71, testid='MODERATOR66', name='MODERATOR66', surname='MODERATOR66', username='MODERATOR66', password='MODERATOR66', gender='male', email='MODERATOR66@gmail.com'),
            Person(id=72, testid='ADMIN66', name='ADMIN66', surname='ADMIN66', username='ADMIN66', password='ADMIN66', gender='male', email='ADMIN66@gmail.com'),
            Person(id=73, testid='FREEUSER67', name='FREEUSER67', surname='FREEUSER67', username='FREEUSER67', password='FREEUSER67', gender='male', email='FREEUSER67@gmail.com'),
            Person(id=74, testid='MODERATOR67', name='MODERATOR67', surname='MODERATOR67', username='MODERATOR67', password='MODERATOR67', gender='male', email='MODERATOR67@gmail.com'),
            Person(id=75, testid='ADMIN67', name='ADMIN67', surname='ADMIN67', username='ADMIN67', password='ADMIN67', gender='male', email='ADMIN67@gmail.com'),
            Person(id=76, testid='FREEUSER68', name='FREEUSER68', surname='FREEUSER68', username='FREEUSER68', password='FREEUSER68', gender='male', email='FREEUSER68@gmail.com'),
            Person(id=77, testid='MODERATOR68', name='MODERATOR68', surname='MODERATOR68', username='MODERATOR68', password='MODERATOR68', gender='male', email='MODERATOR68@gmail.com'),
            Person(id=78, testid='ADMIN68', name='ADMIN68', surname='ADMIN68', username='ADMIN68', password='ADMIN68', gender='male', email='ADMIN68@gmail.com'),
            Person(id=79, testid='FREEUSER69', name='FREEUSER69', surname='FREEUSER69', username='FREEUSER69', password='FREEUSER69', gender='male'),
            Person(id=80, testid='MODERATOR69', name='MODERATOR69', surname='MODERATOR69', username='MODERATOR69', password='MODERATOR69', gender='male'),
            Person(id=81, testid='ADMIN69', name='ADMIN69', surname='ADMIN69', username='ADMIN69', password='ADMIN69', gender='male'),
            Person(id=82, testid='FREEUSER70', name='FREEUSER70', surname='FREEUSER70', username='FREEUSER70', password='FREEUSER70', gender='male', email='FREEUSER70@gmail.com'),
            Person(id=83, testid='MODERATOR70', name='MODERATOR70', surname='MODERATOR70', username='MODERATOR70', password='MODERATOR70', gender='male', email='MODERATOR70@gmail.com'),
            Person(id=84, testid='ADMIN70', name='ADMIN70', surname='ADMIN70', username='ADMIN70', password='ADMIN70', gender='male', email='ADMIN70@gmail.com'),
            Person(id=86, testid='MODERATOR71', name='MODERATOR71', surname='MODERATOR71', username='MODERATOR71', password='MODERATOR71', gender='male', email='MODERATOR71@gmail.com'),
            Event(
                id=87,
                testid='e1',
                title = 'e1', 
                description = 'e1', 
            ), 
            Event(
                id=88,
                testid='e2',
                title = 'e2', 
                description = 'e2', 
            ),
            Event(
                id=89,
                testid='e3',
                title = 'e3', 
                description = 'e3', 
            ),
            Event(
                id=90,
                testid='e4',
                title = 'e4', 
                description = 'e4', 
            ),
            Event(
                id=91,
                testid='e5',
                title = 'e5', 
                description = 'e5', 
            ),
            Event(
                id=92,
                testid='e6',
                title = 'e6', 
                description = 'e6', 
            ),
            Event(
                id=93,
                testid='e7',
                title = 'e7', 
                description = 'e7', 
            ), 
            Category(
                id=94,
                testid='c1',
                name = 'c1'
            ), 
            Category(
                id=95,
                testid='c2',
                name = 'c2'
            ),
            Category(
                id=97,
                testid='c3',
                name = 'c3'
            ), 
            Category(
                id=98,
                testid='c4',
                name = 'c4'
            ),
            Person(
                id=96,
                testid='p0',
                name = 'p0',
                surname = 'p0',
                username = 'p0',
                password = 'p0',
                gender = 'male',
                email = 'p0@gmail.com'
            ),
        ]
        db.session.bulk_save_objects(objects)
        
        
        FREEUSER0 = db.session.query(Person).filter(Person.testid == 'FREEUSER0').one()
        MODERATOR0 = db.session.query(Person).filter(Person.testid == 'MODERATOR0').one()
        MODERATOR1 = db.session.query(Person).filter(Person.testid == 'MODERATOR1').one()
        p0 = db.session.query(Person).filter(Person.testid == 'p0').one()
        ADMIN0 = db.session.query(Person).filter(Person.testid == 'ADMIN0').one()
        FREEUSER0.role = regularuserrole
        MODERATOR0.role = moderatorrole
        ADMIN0.role = adminrole
        FREEUSER44 = db.session.query(Person).filter(Person.testid == 'FREEUSER44').one()
        MODERATOR44 = db.session.query(Person).filter(Person.testid == 'MODERATOR44').one()
        ADMIN44 = db.session.query(Person).filter(Person.testid == 'ADMIN44').one()
        FREEUSER44.role = regularuserrole
        MODERATOR44.role = moderatorrole
        ADMIN44.role = adminrole
        FREEUSER45 = db.session.query(Person).filter(Person.testid == 'FREEUSER45').one()
        MODERATOR45 = db.session.query(Person).filter(Person.testid == 'MODERATOR45').one()
        ADMIN45 = db.session.query(Person).filter(Person.testid == 'ADMIN45').one()
        FREEUSER45.role = regularuserrole
        MODERATOR45.role = moderatorrole
        ADMIN45.role = adminrole
        FREEUSER46 = db.session.query(Person).filter(Person.testid == 'FREEUSER46').one()
        MODERATOR46 = db.session.query(Person).filter(Person.testid == 'MODERATOR46').one()
        ADMIN46 = db.session.query(Person).filter(Person.testid == 'ADMIN46').one()
        FREEUSER46.role = regularuserrole
        MODERATOR46.role = moderatorrole
        ADMIN46.role = adminrole
        FREEUSER47 = db.session.query(Person).filter(Person.testid == 'FREEUSER47').one()
        MODERATOR47 = db.session.query(Person).filter(Person.testid == 'MODERATOR47').one()
        ADMIN47 = db.session.query(Person).filter(Person.testid == 'ADMIN47').one()
        FREEUSER47.role = regularuserrole
        MODERATOR47.role = moderatorrole
        ADMIN47.role = adminrole
        FREEUSER48 = db.session.query(Person).filter(Person.testid == 'FREEUSER48').one()
        MODERATOR48 = db.session.query(Person).filter(Person.testid == 'MODERATOR48').one()
        ADMIN48 = db.session.query(Person).filter(Person.testid == 'ADMIN48').one()
        FREEUSER48.role = regularuserrole
        MODERATOR48.role = moderatorrole
        ADMIN48.role = adminrole
        FREEUSER49 = db.session.query(Person).filter(Person.testid == 'FREEUSER49').one()
        MODERATOR49 = db.session.query(Person).filter(Person.testid == 'MODERATOR49').one()
        ADMIN49 = db.session.query(Person).filter(Person.testid == 'ADMIN49').one()
        FREEUSER49.role = regularuserrole
        MODERATOR49.role = moderatorrole
        ADMIN49.role = adminrole
        FREEUSER50 = db.session.query(Person).filter(Person.testid == 'FREEUSER50').one()
        MODERATOR50 = db.session.query(Person).filter(Person.testid == 'MODERATOR50').one()
        ADMIN50 = db.session.query(Person).filter(Person.testid == 'ADMIN50').one()
        FREEUSER50.role = regularuserrole
        MODERATOR50.role = moderatorrole
        ADMIN50.role = adminrole
        FREEUSER51 = db.session.query(Person).filter(Person.testid == 'FREEUSER51').one()
        MODERATOR51 = db.session.query(Person).filter(Person.testid == 'MODERATOR51').one()
        ADMIN51 = db.session.query(Person).filter(Person.testid == 'ADMIN51').one()
        FREEUSER51.role = regularuserrole
        MODERATOR51.role = moderatorrole
        ADMIN51.role = adminrole
        FREEUSER52 = db.session.query(Person).filter(Person.testid == 'FREEUSER52').one()
        MODERATOR52 = db.session.query(Person).filter(Person.testid == 'MODERATOR52').one()
        ADMIN52 = db.session.query(Person).filter(Person.testid == 'ADMIN52').one()
        FREEUSER52.role = regularuserrole
        MODERATOR52.role = moderatorrole
        ADMIN52.role = adminrole
        FREEUSER53 = db.session.query(Person).filter(Person.testid == 'FREEUSER53').one()
        MODERATOR53 = db.session.query(Person).filter(Person.testid == 'MODERATOR53').one()
        ADMIN53 = db.session.query(Person).filter(Person.testid == 'ADMIN53').one()
        FREEUSER53.role = regularuserrole
        MODERATOR53.role = moderatorrole
        ADMIN53.role = adminrole
        FREEUSER54 = db.session.query(Person).filter(Person.testid == 'FREEUSER54').one()
        MODERATOR54 = db.session.query(Person).filter(Person.testid == 'MODERATOR54').one()
        ADMIN54 = db.session.query(Person).filter(Person.testid == 'ADMIN54').one()
        FREEUSER54.role = regularuserrole
        MODERATOR54.role = moderatorrole
        ADMIN54.role = adminrole
        FREEUSER55 = db.session.query(Person).filter(Person.testid == 'FREEUSER55').one()
        MODERATOR55 = db.session.query(Person).filter(Person.testid == 'MODERATOR55').one()
        ADMIN55 = db.session.query(Person).filter(Person.testid == 'ADMIN55').one()
        FREEUSER55.role = regularuserrole
        MODERATOR55.role = moderatorrole
        ADMIN55.role = adminrole
        FREEUSER56 = db.session.query(Person).filter(Person.testid == 'FREEUSER56').one()
        MODERATOR56 = db.session.query(Person).filter(Person.testid == 'MODERATOR56').one()
        ADMIN56 = db.session.query(Person).filter(Person.testid == 'ADMIN56').one()
        FREEUSER56.role = regularuserrole
        MODERATOR56.role = moderatorrole
        ADMIN56.role = adminrole
        FREEUSER57 = db.session.query(Person).filter(Person.testid == 'FREEUSER57').one()
        FREEUSER57.role = regularuserrole
        FREEUSER58 = db.session.query(Person).filter(Person.testid == 'FREEUSER58').one()
        FREEUSER58.role = regularuserrole
        MODERATOR59 = db.session.query(Person).filter(Person.testid == 'MODERATOR59').one()
        MODERATOR59.role = moderatorrole
        MODERATOR60 = db.session.query(Person).filter(Person.testid == 'MODERATOR60').one()
        MODERATOR60.role = moderatorrole
        ADMIN61 = db.session.query(Person).filter(Person.testid == 'ADMIN61').one()
        ADMIN61.role = adminrole
        ADMIN62 = db.session.query(Person).filter(Person.testid == 'ADMIN62').one()
        ADMIN62.role = adminrole
        FREEUSER63 = db.session.query(Person).filter(Person.testid == 'FREEUSER63').one()
        MODERATOR63 = db.session.query(Person).filter(Person.testid == 'MODERATOR63').one()
        ADMIN63 = db.session.query(Person).filter(Person.testid == 'ADMIN63').one()
        FREEUSER63.role = regularuserrole
        MODERATOR63.role = moderatorrole
        ADMIN63.role = adminrole
        FREEUSER64 = db.session.query(Person).filter(Person.testid == 'FREEUSER64').one()
        MODERATOR64 = db.session.query(Person).filter(Person.testid == 'MODERATOR64').one()
        ADMIN64 = db.session.query(Person).filter(Person.testid == 'ADMIN64').one()
        FREEUSER64.role = regularuserrole
        MODERATOR64.role = moderatorrole
        ADMIN64.role = adminrole
        FREEUSER65 = db.session.query(Person).filter(Person.testid == 'FREEUSER65').one()
        MODERATOR65 = db.session.query(Person).filter(Person.testid == 'MODERATOR65').one()
        ADMIN65 = db.session.query(Person).filter(Person.testid == 'ADMIN65').one()
        FREEUSER65.role = regularuserrole
        MODERATOR65.role = moderatorrole
        ADMIN65.role = adminrole
        FREEUSER66 = db.session.query(Person).filter(Person.testid == 'FREEUSER66').one()
        MODERATOR66 = db.session.query(Person).filter(Person.testid == 'MODERATOR66').one()
        ADMIN66 = db.session.query(Person).filter(Person.testid == 'ADMIN66').one()
        FREEUSER66.role = regularuserrole
        MODERATOR66.role = moderatorrole
        ADMIN66.role = adminrole
        FREEUSER67 = db.session.query(Person).filter(Person.testid == 'FREEUSER67').one()
        MODERATOR67 = db.session.query(Person).filter(Person.testid == 'MODERATOR67').one()
        ADMIN67 = db.session.query(Person).filter(Person.testid == 'ADMIN67').one()
        FREEUSER67.role = regularuserrole
        MODERATOR67.role = moderatorrole
        ADMIN67.role = adminrole
        FREEUSER68 = db.session.query(Person).filter(Person.testid == 'FREEUSER68').one()
        MODERATOR68 = db.session.query(Person).filter(Person.testid == 'MODERATOR68').one()
        ADMIN68 = db.session.query(Person).filter(Person.testid == 'ADMIN68').one()
        FREEUSER68.role = regularuserrole
        MODERATOR68.role = moderatorrole
        ADMIN68.role = adminrole
        FREEUSER69 = db.session.query(Person).filter(Person.testid == 'FREEUSER69').one()
        MODERATOR69 = db.session.query(Person).filter(Person.testid == 'MODERATOR69').one()
        ADMIN69 = db.session.query(Person).filter(Person.testid == 'ADMIN69').one()
        FREEUSER69.role = regularuserrole
        MODERATOR69.role = moderatorrole
        ADMIN69.role = adminrole
        FREEUSER70 = db.session.query(Person).filter(Person.testid == 'FREEUSER70').one()
        MODERATOR70 = db.session.query(Person).filter(Person.testid == 'MODERATOR70').one()
        ADMIN70 = db.session.query(Person).filter(Person.testid == 'ADMIN70').one()
        FREEUSER70.role = regularuserrole
        MODERATOR70.role = moderatorrole
        ADMIN70.role = adminrole
        MODERATOR71 = db.session.query(Person).filter(Person.testid == 'MODERATOR71').one()
        MODERATOR71.role = moderatorrole
        MODERATOR1.role = moderatorrole
        p0.role = regularuserrole
        e1 = db.session.query(Event).filter(Event.testid == 'e1').one()
        e2 = db.session.query(Event).filter(Event.testid == 'e2').one()
        e3 = db.session.query(Event).filter(Event.testid == 'e3').one()
        e4 = db.session.query(Event).filter(Event.testid == 'e4').one()
        e5 = db.session.query(Event).filter(Event.testid == 'e5').one()
        e6 = db.session.query(Event).filter(Event.testid == 'e6').one()
        e7 = db.session.query(Event).filter(Event.testid == 'e7').one()
        c1 = db.session.query(Category).filter(Category.testid == 'c1').one()
        c2 = db.session.query(Category).filter(Category.testid == 'c2').one()
        c3 = db.session.query(Category).filter(Category.testid == 'c3').one()
        c4 = db.session.query(Category).filter(Category.testid == 'c4').one()
        e1.categories.append(c1)
        e2.categories.append(c1)
        e3.categories.append(c1)
        e4.categories.append(c1)
        e5.categories.append(c1)
        e6.categories.append(c1)
        e7.categories.append(c1)
        e1.categories.append(c2)
        e2.categories.append(c2)
        e3.categories.append(c2)
        e4.categories.append(c2)
        e5.categories.append(c2)
        e6.categories.append(c2)
        e7.categories.append(c2)
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
        c1.moderators.append(MODERATOR0)
        c2.moderators.append(MODERATOR1)
        c3.moderators.append(MODERATOR0)
        c4.moderators.append(MODERATOR1)

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

