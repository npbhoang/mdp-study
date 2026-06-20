# Copyright (c) 2023 All Rights Reserved

from flask import render_template, redirect, url_for
from flask_user import current_user
from dtm import db, Event, Category, Person, Role, Ad, Purpose, Consent, PersonalData
from auxiliary import recommend_events, get_personalize_ad, send_advertisement_to_user, get_candidates

from instrumentation import SecurityException, secure, Restrict

def P(ls):
    def lazy():
        return list(map(lambda x: Purpose.query.filter_by(name=x).first(),ls))
    return lazy

@secure(db,P(['CORE']))
def main():
    name = current_user.name
    surname = current_user.surname
    rec_events = recommend_events({'user': current_user}) if current_user.is_authenticated else []
    rec_event_titles = [e.title for e in rec_events]
    rec_event_descs = [e.description for e in rec_events]
    return {
        'name': name, 
        'surname': surname, 
        'recommended_events': rec_events,
        'rec_event_titles': rec_event_titles,
        'rec_event_descs': rec_event_descs
        }

@secure(db,P(['CORE']))
def users():
    users = Person.query.all()
    cu = None
    p1 = None
    for u in users:
        if u.id == current_user.id:
            cu = u
        if u.testid == 'p1':
            p1 = u
    current_user_name = cu.name if cu else None
    current_user_surname = cu.surname if cu else None   
    other_user_name = p1.name if p1 else None
    other_user_surname = p1.surname if p1 else None
    return {
        'users': users, 
        'current_user_name': current_user_name, 
        'current_user_surname': current_user_surname, 
        'other_user_name': other_user_name, 
        'other_user_surname': other_user_surname
        }

@secure(db,P(['CORE']))
def user(id):
    user = Person.query.get(id)
    user_name = user.name
    user_surname = user.surname
    user_role = user.role.name if user.role else Restrict()
    user_gender = user.gender
    user_email = user.email
    user_subscriptions = [c for c in user.subscriptions]
    user_subscription_category_names = [c.name for c in user.subscriptions]
    return {
        'user_name': user_name, 
        'user_surname': user_surname, 
        'user_role': user_role, 
        'user_gender': user_gender, 
        'user_email': user_email,
        'user_subscriptions': user_subscriptions,
        'user_subscription_category_names': user_subscription_category_names
        }

@secure(db,P(['CORE']))
def profile():
    ad = get_personalize_ad({'user': current_user})
    ad_content = ad.content if ad else None
    manage_events = [e for e in current_user.manages]
    manage_event_titles = [e.title for e in current_user.manages]
    manage_event_owners = [e.owner for e in current_user.manages]
    manage_event_owner_names = [o.name for o in manage_event_owners]
    attend_events = [e for e in current_user.attends]
    attend_event_titles = [e.title for e in current_user.attends]
    attend_event_owners = [e.owner for e in current_user.attends]
    attend_event_owner_names = [o.name for o in attend_event_owners]
    subscriptions = [c for c in current_user.subscriptions]
    subscribed_category_names = [c.name for c in current_user.subscriptions]
    subscribed_category_events = []
    subscribed_category_event_titles = []
    subscribed_category_event_owners = []
    subscribed_category_event_owner_names = []
    subscribed_category_event_owner_surnames = []
    subscribed_category_subscribers = []
    for c in subscriptions:
        for e in c.events:
            subscribed_category_events.append(e)
            subscribed_category_event_titles.append(e.title)
            subscribed_category_event_owners.append(e.owner)
            subscribed_category_event_owner_names.append(e.owner.name)
            subscribed_category_event_owner_surnames.append(e.owner.surname)
        if c.id == 18 and current_user.id != 3:
            subscribed_category_subscribers = c.subscribers
        elif c.id == 19 and current_user.id == 3:
            subscribed_category_subscribers = c.subscribers
    return {
        'ad_content': ad_content,
        'manage_events': manage_events,
        'manage_event_titles': manage_event_titles,
        'manage_event_owners': manage_event_owners,
        'manage_event_owner_names': manage_event_owner_names,
        'attend_events': attend_events,
        'attend_event_titles': attend_event_titles,
        'attend_event_owners': attend_event_owners,
        'attend_event_owner_names': attend_event_owner_names,
        'subscriptions': subscriptions,
        'subscribed_category_names': subscribed_category_names,
        'subscribed_category_events': subscribed_category_events,
        'subscribed_category_event_titles': subscribed_category_event_titles,
        'subscribed_category_event_owners': subscribed_category_event_owners,
        'subscribed_category_event_owner_names': subscribed_category_event_owner_names,
        'subscribed_category_event_owner_surnames': subscribed_category_event_owner_surnames,
        'subscribed_category_subscribers': subscribed_category_subscribers
    }

@secure(db,P(['CORE']))
def update_user(id,name,surname,email,gender,rolename):
    user = Person.query.get(id)
    if user.name != name:
        user.name = name
    if user.surname != surname:
        user.surname = surname
    if user.email != email:
        user.email = email
    if user.gender != gender:
        user.gender = gender
    if user.role.name != rolename:
        user.role = Role.query.filter_by(name=rolename).first()
    db.session.commit()

@secure(db,P([]))
def join(id):
    event = Event.query.get(id)
    if current_user.id not in [p.id for p in event.requesters]:
        p = Person.query.get(current_user.id)
        event.requesters.append(p)
        db.session.commit()

@secure(db,P([]))
def leave(id):
    event = Event.query.get(id)
    if current_user.id in [p.id for p in event.attendants]:
        p = Person.query.get(current_user.id)
        p.attends.remove(event)
        db.session.commit()

@secure(db,P([]))
def add_moderator(id,c):
    user = Person.query.get(id)
    category = Category.query.get(c)
    if user not in category.moderators:
        category.moderators.append(user)
        db.session.commit()

@secure(db,P([]))
def remove_moderator(id,c):
    user = Person.query.get(id)
    category = Category.query.get(c)
    if user in category.moderators:
        category.moderators.remove(user)
        db.session.commit()

@secure(db,P(['CORE']))
def subscribe(id):
    category = Category.query.get(id)
    if category not in current_user.subscriptions:
         current_user.subscriptions.append(category)
         db.session.commit()

@secure(db,P(['CORE']))
def unsubscribe(id):
    category = Category.query.get(id)
    if category in current_user.subscriptions:
         current_user.subscriptions.remove(category)
         db.session.commit()

@secure(db,P(['CORE']))
def events():
    events = Event.query.all()
    categories = Category.query.all()
    category_names = [c.name for c in categories]
    admin_own_events = None
    admin_own_event_titles = None
    admin_own_event_owners = None
    admin_own_event_owner_names = None
    moderator_own_events = None
    moderator_own_event_titles = None
    moderator_own_event_owners = None
    moderator_own_event_owner_names = None
    regularuser_own_events = None
    regularuser_own_event_titles = None
    regularuser_own_event_owners = None
    regularuser_own_event_owner_names = None
    manage_events = None
    manage_event_titles = None
    manage_event_owners = None
    manage_event_owner_names = None
    attend_events = None
    attend_event_titles = None
    attend_event_owners = None
    attend_event_owner_names = None
    request_events = None
    request_event_titles = None
    request_event_owners = None
    request_event_owner_names = None
    stranger_events = None
    stranger_event_titles = None
    stranger_event_owners = None
    stranger_event_owner_names = None
    for e in events:
        if e.id == 15:
            admin_own_events = e
            admin_own_event_titles = e.title
            admin_own_event_owners = e.owner
            admin_own_event_owner_names = e.owner.name
        elif e.id == 14:
            moderator_own_events = e
            moderator_own_event_titles = e.title
            moderator_own_event_owners = e.owner
            moderator_own_event_owner_names = e.owner.name
        elif e.id == 13:
            regularuser_own_events = e
            regularuser_own_event_titles = e.title
            regularuser_own_event_owners = e.owner
            regularuser_own_event_owner_names = e.owner.name
        elif e.id == 9:
            manage_events = e
            manage_event_titles = e.title
            manage_event_owners = e.owner
            manage_event_owner_names = e.owner.name
        elif e.id == 10:
            attend_events = e
            attend_event_titles = e.title
            attend_event_owners = e.owner
            attend_event_owner_names = e.owner.name
        elif e.id == 16:
            request_events = e
            request_event_titles = e.title
            request_event_owners = e.owner
            request_event_owner_names = e.owner.name
        elif e.id == 17:
            stranger_events = e
            stranger_event_titles = e.title
            stranger_event_owners = e.owner
            stranger_event_owner_names = e.owner.name

    return {
        'category_names': category_names,
        'admin_own_events': admin_own_events,
        'admin_own_event_titles': admin_own_event_titles,
        'admin_own_event_owners': admin_own_event_owners,
        'admin_own_event_owner_names': admin_own_event_owner_names,
        'moderator_own_events': moderator_own_events,
        'moderator_own_event_titles': moderator_own_event_titles,
        'moderator_own_event_owners': moderator_own_event_owners,
        'moderator_own_event_owner_names': moderator_own_event_owner_names,
        'regularuser_own_events': regularuser_own_events,
        'regularuser_own_event_titles': regularuser_own_event_titles,
        'regularuser_own_event_owners': regularuser_own_event_owners,
        'regularuser_own_event_owner_names': regularuser_own_event_owner_names,
        'manage_events': manage_events,
        'manage_event_titles': manage_event_titles,
        'manage_event_owners': manage_event_owners,
        'manage_event_owner_names': manage_event_owner_names,
        'attend_events': attend_events,
        'attend_event_titles': attend_event_titles,
        'attend_event_owners': attend_event_owners,
        'attend_event_owner_names': attend_event_owner_names,
        'request_events': request_events,
        'request_event_titles': request_event_titles,
        'request_event_owners': request_event_owners,
        'request_event_owner_names': request_event_owner_names,
        'stranger_events': stranger_events,
        'stranger_event_titles': stranger_event_titles,
        'stranger_event_owners': stranger_event_owners,
        'stranger_event_owner_names': stranger_event_owner_names
    }
    # return {'events': Event.query.all(), 'categories': Category.query.all()}

@secure(db,P([]))
def create_event(title,description,categories):
    event = Event()
    current_user.events.append(event)
    current_user.manages.append(event)
    current_user.attends.append(event)
    event.title = title
    event.description = description
    for cid in categories:
        c = Category.query.get(cid)
        event.categories.append(c)
    db.session.add(event)
    db.session.commit()

@secure(db,P(['CORE']))
def view_event(id):
    event=Event.query.get(id)
    event_title = event.title
    event_description = event.description
    event_categories = event.categories
    event_category_names = [c.name for c in event.categories]
    event_attendants = [a for a in event.attendants]
    event_attendant_names = [a.name for a in event.attendants]
    event_attendant_surames = [a.surname for a in event.attendants]
    return {
        'event': Event.query.get(id),
        'event_title': event_title,
        'event_description': event_description,
        'event_categories': event_categories,
        'event_category_names': event_category_names,
        'event_attendants': event_attendants,
        'event_attendant_names': event_attendant_names,
        'event_attendant_surames': event_attendant_surames
    }

@secure(db,P([]))
def edit_event(id):
    event=Event.query.get(id)
    event_title = event.title
    event_description = event.description
    event_categories = [c for c in event.categories]
    event_category_names = [c.name for c in event.categories]
    return {
        'event': Event.query.get(id),
        'event_title': event_title,
        'event_description': event_description,
        'event_categories': event_categories,
        'event_category_names': event_category_names
    }

@secure(db,P([]))
def update_event(id,title,description,categories):
    event = Event.query.get(id)
    if event.title != title:
        event.title = title
    if event.description != description:
        event.description = description
    new_categories = [int(id) for id in categories] 
    current_categories = [c.id for c in event.categories]
    if set(current_categories) != set(new_categories):
        ids_to_remove = set(current_categories) - set(new_categories)
        ids_to_add = set(new_categories) - set(current_categories)
        for cid in ids_to_remove:
            c = Category.query.get(cid)
            event.categories.remove(c)
        for cid in ids_to_add:
            c = Category.query.get(cid)
            event.categories.append(c)
    db.session.commit()

@secure(db,P(['CORE']))
def manage_event(id):
    event = Event.query.get(id)
    event_attendants = [a for a in event.attendants]
    event_attendant_names = [a.name for a in event.attendants]
    event_attendant_surnames = [a.surname for a in event.attendants]
    event_managers = [m for m in event.managedBy]
    event_manager_names = [m.name for m in event.managedBy]
    event_manager_surnames = [m.surname for m in event.managedBy]
    event_requesters = [r for r in event.requesters]
    event_requester_names = [r.name for r in event.requesters]
    event_requester_surnames = [r.surname for r in event.requesters]
    return {
        'event': Event.query.get(id),
        'event_attendants': event_attendants,
        'event_attendant_names': event_attendant_names,
        'event_attendant_surnames': event_attendant_surnames,
        'event_managers': event_managers,
        'event_manager_names': event_manager_names,
        'event_manager_surnames': event_manager_surnames,
        'event_requesters': event_requesters,
        'event_requester_names': event_requester_names,
        'event_requester_surnames': event_requester_surnames
    }

@secure(db,P([]))
def remove_category(id,c):
    event = Event.query.get(id)
    category = Category.query.get(c)
    if event in category.events:
        category.events.remove(event)
        db.session.commit()

@secure(db,P([]))
def promote_manager(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    if user not in event.managedBy:
        user.manages.append(event)
        db.session.commit()  

@secure(db,P([]))
def demote_manager(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    if user in event.managedBy:
        user.manages.remove(event)
        db.session.commit()

@secure(db,P([]))
def remove_attendee(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    if user in event.attendants:
        user.attends.remove(event)
        db.session.commit()

@secure(db,P([]))
def accept_request(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    if user not in event.attendants:
        user.attends.append(event)
    event.requesters.remove(user)
    db.session.commit()

@secure(db,P([]))
def reject_request(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    event.requesters.remove(user)
    db.session.commit()

@secure(db,P([]))
def categories():
    categories = Category.query.all()
    c0 = None
    for c in categories:
        if c.id == 13:
            c0 = c
    category_c0_events = c0.events
    category_c0_name = c0.name
    return {
        'categories': categories,
        'category_c0_events': category_c0_events,
        'category_c0_name': category_c0_name
    }

@secure(db,P([]))
def create_category(name):    
    category = Category()
    category.name = name
    db.session.add(category)
    db.session.commit()

@secure(db,P(['CORE']))
def view_category(id):
    category = Category.query.get(id)
    category_subscribers = [s for s in category.subscribers]
    category_subscriber_names = [s.name for s in category.subscribers]
    category_subscriber_surnames = [s.surname for s in category.subscribers]
    category_events = [e for e in category.events]
    category_event_titles = [e.title for e in category.events]
    category_event_owners = [e.owner for e in category.events]
    category_event_owner_names = [o.name for o in category_event_owners]
    category_event_owner_surnames = [o.surname for o in category_event_owners]
    category_name = category.name
    # return {'category': Category.query.get(id)}
    return {
        'category': category,
        'category_subscribers': category_subscribers,
        'category_subscriber_names': category_subscriber_names,
        'category_subscriber_surnames': category_subscriber_surnames,
        'category_events': category_events,
        'category_event_titles': category_event_titles,
        'category_event_owners': category_event_owners,
        'category_event_owner_names': category_event_owner_names,
        'category_event_owner_surnames': category_event_owner_surnames,
        'category_name': category_name
    }

@secure(db,P(['CORE']))
def edit_category(id):
    category = Category.query.get(id)
    category_moderators = [m for m in category.moderators]
    category_moderator_names = [m.name for m in category.moderators]
    category_moderator_surnames = [m.surname for m in category.moderators]
    candidates = get_candidates({'cat': category})
    candidate_names = [c.name for c in candidates]
    candidate_surnames = [c.surname for c in candidates]
    return {
        'category': category,
        'category_moderators': category_moderators,
        'category_moderator_names': category_moderator_names,
        'category_moderator_surnames': category_moderator_surnames,
        'candidates': candidates,
        'candidate_names': candidate_names,
        'candidate_surnames': candidate_surnames
    }
    # return {'category': category, 'candidates': candidates}

@secure(db,P([]))
def update_category(id, name):
    category = Category.query.get(id)
    if category.name != name:
        category.name = name
    db.session.commit()

@secure(db,P([]))
def ads():  
    ads = Ad.query.all()
    ad_contents = [a.content for a in ads]
    # return {'ads': Ad.query.all()}
    return {
        'ads': ads,
        'ad_contents': ad_contents
    }

@secure(db,P([]))
def remove_ad(id):
    ad = Ad.query.get(id)
    ad.__delete__(db)
    db.session.commit()

@secure(db,P([]))
def create_ad(content):
    ad = Ad()
    ad.content = content
    db.session.add(ad)
    db.session.commit()

@secure(db,P(['MASSMARKETING']))
def send_mass_advertisement(id):
    category = Category.query.get(id)
    for p in category.subscribers:
        send_advertisement_to_user({'user': p})

@secure(db,P(['ANALYTICS']))
def analyze(id):
    event = Event.query.get(id)
    gender_counts = {"male": 0, "female": 0, "unknown": 0}
    for p in event.attendants:
        gender = p.gender if str(p.gender) in gender_counts else "unknown"
        gender_counts[gender] += 1    
    return {'event': event, 'male': gender_counts['male'], 'female': gender_counts['female'], 'unknown': gender_counts['unknown']}