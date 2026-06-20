from flask import request
from flask_user import current_user
from model import db, Invite, Person, Role, Event, Category, Purpose, Ad, AnyPurpose, FunctionalPurpose, MarketingPurpose, AnalyticsPurpose, CorePurpose, RecommendEventsPurpose, TargetedMarketingPurpose, MassMarketingPurpose, InsightsPurpose, StatsPurpose
from dto import PersonDTO, EventDTO, CategoryDTO, RoleDTO, AdDTO, InviteDTO, RESTRICTED
import hashlib
import random
import sys

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

PRIVACY_INPUT = {
    AnyPurpose: {
        "data": [],
        "children": {
            MarketingPurpose: {
                "data": [("Person", "name")],
                "children": {
                    TargetedMarketingPurpose: {"data": [("Person", "gender")], "children": {}},
                    MassMarketingPurpose: {"data": [("Person", "email")], "children": {}}
                }
            },
            InsightsPurpose: {
                "data": [],
                "children": {
                    AnalyticsPurpose: {"data": [("Person", "gender")], "children": {}},
                    StatsPurpose: {
                        "data": [("Person", "name"), ("Person", "subscriptions"), ("Person", "attends")],
                        "children": {},
                        "constraintDesc": "you attended more than two events"
                    }
                }
            },
            FunctionalPurpose: {
                "data": [("Person", "attends")],
                "children": {
                    RecommendEventsPurpose: {
                        "data": [("Person", "subscriptions")],
                        "children": {},
                        "constraintDesc": "you are a regular user"
                    },
                    CorePurpose: {
                        "data": [("Person", "name"), ("Person", "surname"), ("Person", "role"), ("Person", "subscriptions"), ("Person", "gender"), ("Person", "email")],
                        "children": {}
                    }
                }
            }
        }
    }
}

class SecurityException(Exception):
    def __init__(self, msg = 'Not allowed', page = 'sec_error.html', params = {}):
        self.msg = msg
        self.page = page
        self.params = params

class PrivacyException(Exception):
    def __init__(self, msg = 'Not allowed', page = 'priv_error.html', params = {}):
        self.msg = msg
        self.page = page
        self.params = params

def _purposes_below(name, tree=PRIVACY_INPUT):
    """The purpose `name` plus every purpose nested under it, per the PRIVACY_INPUT
    hierarchy. Consent to a purpose also grants the purposes it contains."""
    for purpose, body in tree.items():
        if purpose == name:
            names = {purpose}
            stack = list(body["children"].items())
            while stack:
                child, child_body = stack.pop()
                names.add(child)
                stack.extend(child_body["children"].items())
            return names
        found = _purposes_below(name, body["children"])
        if found:
            return found
    return set()  # not found in this subtree

def get_consent_tuples(consents):
    # Per the privacy policy, consenting to a purpose also covers the actual purposes
    # it contains ("...or to purposes containing the actual purposes"). So expand each
    # consent down the hierarchy: e.g. consent to Functional grants Core/RecommendEvents.
    tuples = []
    for con in consents:
        below = _purposes_below(con.purpose.name) or {con.purpose.name}
        for p in below:
            tuples.append((con.classname, con.propertyname, p))
    return tuples

def on_identity_loaded(sender, identity):
    pass

def init():
    pass

def main():
    user=PersonDTO.copy(current_user) 
    if current_user.is_authenticated:
        consent_tuples = get_consent_tuples(current_user.consents)
        events = RESTRICTED
        if ('Person', 'subscriptions', 'RecommendEvents') in consent_tuples and current_user.role.name == 'REGULARUSER':
            events = recommend_events(current_user)
        if ('Person', 'name', 'Core') not in consent_tuples:
            user.name = RESTRICTED
        if ('Person', 'surname', 'Core') not in consent_tuples:
            user.surname = RESTRICTED
    else:
        events = []
    return {'user' : user, 'recommended_events': events}

def profile():
    if not current_user.is_authenticated:
        raise SecurityException(msg="No profile available for visitors")
    
    user=PersonDTO.copy(current_user) 
    if ('Person', 'attends', 'Core') not in get_consent_tuples(current_user.consents):
        user.attends = RESTRICTED
    for e in user.manages:
        e.owner = PersonDTO.copy(Event.query.get(e.id).owner)
        consent_tuples = get_consent_tuples(Person.query.get(e.owner.id).consents)
        if ('Person', 'name', 'Core') not in consent_tuples:
            e.owner.name = RESTRICTED
    for e in user.attends:
        e.owner = PersonDTO.copy(Event.query.get(e.id).owner)
        consent_tuples = get_consent_tuples(Person.query.get(e.owner.id).consents)
        if ('Person', 'name', 'Core') not in consent_tuples:
            e.owner.name = RESTRICTED

    if ('Person', 'subscriptions', 'Core') not in get_consent_tuples(current_user.consents):
        subs = RESTRICTED
    else:
        subs = CategoryDTO.copies(current_user.subscriptions)
    for s in subs:
        if current_user.id not in [m.id for m in s.moderators]:
            s.subscribers = RESTRICTED
        for e in s.events:
            e.owner = PersonDTO.copy(Event.query.get(e.id).owner)
            consent_tuples = get_consent_tuples(Person.query.get(e.owner.id).consents)
            if ('Person', 'name', 'Core') not in consent_tuples:
                e.owner.name = RESTRICTED
            if ('Person', 'surname', 'Core') not in consent_tuples:
                e.owner.surname = RESTRICTED

    consent_tuples = get_consent_tuples(current_user.consents)
    if ('Person', 'gender', 'TargetedMarketing') in consent_tuples and ('Person', 'name', 'Marketing') in consent_tuples:
        ad = get_personalize_ad(current_user)
    else:
        ad = RESTRICTED
    return {'user' : user, 'subs' : subs, 'ad': ad}
        
def events():   
    events = EventDTO.copies(Event.query.all())
    for event in events:
        consent_tuples = get_consent_tuples(Person.query.get(event.owner.id).consents)
        if not current_user.is_authenticated or ('Person', 'name', 'Core') not in consent_tuples:
            event.owner.name = RESTRICTED
    categories = CategoryDTO.copies(Category.query.all())
    return {'events' : events, 'categories' : categories}

def view_event(id):
    event = EventDTO.copy(Event.query.get(id))
    if not current_user.is_authenticated:
        event.attendants = RESTRICTED          
    else:
        for att in event.attendants:
            consent_tuples = get_consent_tuples(Person.query.get(att.id).consents)
            if not current_user.is_authenticated or ('Person', 'name', 'Core') not in consent_tuples:
                att.name = RESTRICTED
            if not current_user.is_authenticated or ('Person', 'surname', 'Core') not in consent_tuples:
                att.surname = RESTRICTED
    return {'event' : event}

def edit_event(id):
    event = EventDTO.copy(Event.query.get(id))
    categories = CategoryDTO.copies(Category.query.all())
    return {'event' : event, 'categories' : categories}

def update_event():
    event = Event.query.get(request.form["id"])
    is_manager = current_user.is_authenticated and current_user.id in [m.id for m in event.managedBy]
    new_ids = [int(c) for c in request.form.getlist("categories")]
    changed = set(c.id for c in event.categories) ^ set(new_ids)  
    moderates_changed = current_user.is_authenticated and all(
        current_user.id in [m.id for m in Category.query.get(cid).moderators] for cid in changed)
    if not is_manager and not (changed and moderates_changed):
        raise SecurityException(msg="Only event managers, or moderators of the changed categories, may edit")
    if is_manager:                     
        event.title = request.form["title"]
        event.description = request.form["description"]
    if set(c.id for c in event.categories) != set(new_ids):
        event.categories = [Category.query.get(c) for c in new_ids]
    db.session.commit()
    return request.form["id"]

def join(id):
    if not current_user.is_authenticated:
        raise SecurityException(msg="Visitors cannot join events")
    event = Event.query.get(id)
    if current_user.id in [i.invitee.id for i in event.invitations]:
        raise SecurityException(msg="You have been invited; you cannot request to join")
    if current_user.id not in [p.id for p in event.requesters]:
        event.requesters.append(current_user)
        db.session.commit()

def analyze(id):
    event = Event.query.get(id)
    gender_counts = {"male": 0, "female": 0, "unknown": 0}
    if current_user.is_authenticated and current_user.role.name == "ADMIN":
        for p in event.attendants:
            consent_tuples = get_consent_tuples(p.consents)
            if ('Person', 'gender', 'Analytics') in consent_tuples:
                g = p.gender if p.gender in gender_counts else "unknown"
                gender_counts[g] += 1
    return {'event': event, 'male': gender_counts['male'],
            'female': gender_counts['female'], 'unknown': gender_counts['unknown']}
    
def leave(id):
    if not current_user.is_authenticated:
        raise SecurityException(msg="Visitors cannot leave an event")
    event = Event.query.get(id)
    if current_user.id in [event_manager.id for event_manager in event.managedBy]:
        raise SecurityException(msg="The managers of the event cannot leave it")
    if ('Person', 'attends', 'Core') not in get_consent_tuples(current_user.consents):
        raise PrivacyException(msg="No consent to update attendance for the Core purpose")
    for a in event.attendants:
        if a.id == current_user.id:
            event.attendants.remove(a)
            db.session.commit()
            break
    
def create_event():
    if not current_user.is_authenticated:
        raise SecurityException(msg="Only registered users can create events")
    title = request.form["title"]
    description = request.form["description"]
    owner = current_user
    categories = request.form.getlist("categories")
    categories = [Category.query.get(c) for c in categories]
    event = Event(title=title,
                  description=description,
                  owner=owner,
                  categories=categories)
    event.managedBy.append(owner)
    event.attendants.append(owner)
    db.session.add(event)
    db.session.commit()
    
def manage_event(id):
    event = EventDTO.copy(Event.query.get(id))
    if not current_user.is_authenticated:
        event.attendants = RESTRICTED
        event.managedBy = RESTRICTED
        event.requesters = RESTRICTED
    else:
        is_manager = current_user.id in [m.id for m in event.managedBy]
        for u in event.attendants + event.managedBy + event.requesters:
            consent_tuples = get_consent_tuples(Person.query.get(u.id).consents)
            if ('Person', 'name', 'Core') not in consent_tuples:
                u.name = RESTRICTED
            if ('Person', 'surname', 'Core') not in consent_tuples:
                u.surname = RESTRICTED
        if not is_manager:
            event.requesters = RESTRICTED
    return {'event' : event}

def categories():
    categories = CategoryDTO.copies(Category.query.all())
    return {'categories' : categories}

def view_category(id):
    category = CategoryDTO.copy(Category.query.get(id))
    for event in category.events:
        event.owner = PersonDTO.copy(Event.query.get(event.id).owner)
        consent_tuples = get_consent_tuples(Person.query.get(event.owner.id).consents)
        if not current_user.is_authenticated or (('Person', 'name', 'Core') not in consent_tuples):
            event.owner.name = RESTRICTED
        if not current_user.is_authenticated or (('Person', 'surname', 'Core') not in consent_tuples):
            event.owner.surname = RESTRICTED

    if not current_user.is_authenticated or current_user.id not in [mod.id for mod in category.moderators]:
        category.subscribers = RESTRICTED
    else:
        for sub in category.subscribers:
            consent_tuples = get_consent_tuples(Person.query.get(sub.id).consents)
            if ('Person', 'name', 'Core') not in consent_tuples:
                sub.name = RESTRICTED
            if ('Person', 'surname', 'Core') not in consent_tuples:
                sub.surname = RESTRICTED
    return {'category' : category}

def remove_category(id,c):
    event = Event.query.get(id)
    category = Category.query.get(c)
    if not current_user.is_authenticated or (
        current_user.id not in [m.id for m in event.managedBy]
        and current_user.id not in [mod.id for mod in category.moderators]):
        raise SecurityException(msg="Only the event's managers or the category's moderators can remove it")
    if event in category.events:
        category.events.remove(event)
        db.session.commit()
    
def edit_category(id):
    cat = Category.query.get(id)
    category = CategoryDTO.copy(cat)
    for mod in category.moderators:                       
        consent_tuples = get_consent_tuples(Person.query.get(mod.id).consents)
        if not current_user.is_authenticated or ('Person', 'name', 'Core') not in consent_tuples:
            mod.name = RESTRICTED
        if not current_user.is_authenticated or ('Person', 'surname', 'Core') not in consent_tuples:
            mod.surname = RESTRICTED
    if not current_user.is_authenticated:          
        candidates = RESTRICTED
    else:
        candidates = []                       
        for cand in PersonDTO.copies(cat.candidates):
            consent_tuples = get_consent_tuples(Person.query.get(cand.id).consents)
            if ('Person', 'role', 'Core') not in consent_tuples:
                continue
            if ('Person', 'name', 'Core') not in consent_tuples:
                cand.name = RESTRICTED
            if ('Person', 'surname', 'Core') not in consent_tuples:
                cand.surname = RESTRICTED
            candidates.append(cand)
    return {'category' : category, 'candidates' : candidates}

def add_moderator(id,c):
    if not current_user.is_authenticated or current_user.role.name != "ADMIN":
        raise SecurityException(msg="Only administrators can add moderators")
    user = Person.query.get(id)
    category = Category.query.get(c)
    if user.role.name != "MODERATOR":                    
        raise SecurityException(msg="Only users with the MODERATOR role can be added")
    if user not in category.moderators:
        category.moderators.append(user)
        db.session.commit()

def remove_moderator(id,c):
    if not current_user.is_authenticated or (current_user.id != id and current_user.role.name != "ADMIN"):
        raise SecurityException(msg="Only administrators can remove other moderators")
    user = Person.query.get(id)
    category = Category.query.get(c)
    if user in category.moderators:
        category.moderators.remove(user)
        db.session.commit()

def update_category():
    if not current_user.is_authenticated or current_user.role.name != "ADMIN":
        raise SecurityException(msg="Only administrators can update categories")
    category = Category.query.get(request.form["id"])
    if category.name != request.form["name"]:
        category.name = request.form["name"]
    db.session.commit()
    return request.form["id"]

def subscribe(id):
    if not current_user.is_authenticated:
        raise SecurityException(msg="Only registered users can subscribe categories")
    category = Category.query.get(id)
    if category not in current_user.subscriptions:
         current_user.subscriptions.append(category)
         db.session.commit()
    
def unsubscribe(id):
    if not current_user.is_authenticated:
        raise SecurityException(msg="Only registered users can unsubscribe categories")
    category = Category.query.get(id)
    if category in current_user.subscriptions:
         current_user.subscriptions.remove(category)
         db.session.commit()
    
def send_mass_advertisement(id):
    category = Category.query.get(id)
    if not current_user.is_authenticated or current_user.id not in [mod.id for mod in category.moderators]:
        raise SecurityException(msg="Only the category's moderators can send advertisements")
    for subscriber in category.subscribers:
        consent_tuples = get_consent_tuples(subscriber.consents)
        if ('Person', 'email', 'MassMarketing') in consent_tuples and ('Person', 'name', 'Marketing') in consent_tuples:
            send_advertisement_to_user(subscriber)

def create_category():
    if not current_user.is_authenticated or current_user.role.name != "ADMIN":
        raise SecurityException(msg="Only administrators can create categories")
    name = request.form["name"]
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()

def users():
    users = PersonDTO.copies(Person.query.all())
    for user in users:
        consent_tuples = get_consent_tuples(Person.query.get(user.id).consents)
        if not current_user.is_authenticated or ('Person', 'name', 'Core') not in consent_tuples:
            user.name = RESTRICTED
        if not current_user.is_authenticated or ('Person', 'surname', 'Core') not in consent_tuples:
            user.surname = RESTRICTED
        if not current_user.is_authenticated or ('Person', 'role', 'Core') not in consent_tuples:
            user.role = RESTRICTED
    return {'users' : users}

def user(id):
    user = PersonDTO.copy(Person.query.get(id))
    if not current_user.is_authenticated:
        user.name = RESTRICTED
        user.surname = RESTRICTED
        user.email = RESTRICTED
        user.gender = RESTRICTED
        user.role = RESTRICTED
        user.subscriptions = RESTRICTED
    else:
        consent_tuples = get_consent_tuples(Person.query.get(user.id).consents)
        # security check
        if current_user.id != id:
            if current_user.role.name != "ADMIN":
                user.gender = RESTRICTED
            user_subscriptions = [CategoryDTO.copy(Category.query.get(cat.id)) for cat in user.subscriptions]
            sub_moderators = [cat.moderators for cat in user_subscriptions]
            if current_user.id not in [moderator.id for moderator_list in sub_moderators for moderator in moderator_list]:
                user.email = RESTRICTED
            user.subscriptions = RESTRICTED
        # privacy check
        if ('Person', 'name', 'Core') not in consent_tuples:
            user.name = RESTRICTED
        if ('Person', 'surname', 'Core') not in consent_tuples:
            user.surname = RESTRICTED
        if ('Person', 'email', 'Core') not in consent_tuples:
            user.email = RESTRICTED
        if ('Person', 'gender', 'Core') not in consent_tuples:
            user.gender = RESTRICTED
        if ('Person', 'role', 'Core') not in consent_tuples:
            user.role = RESTRICTED
        if ('Person', 'subscriptions', 'Core') not in consent_tuples:
            user.subscriptions = RESTRICTED
    roles = RoleDTO.copies(Role.query.all())
    return {'user' : user, 'roles' : roles}

def update_user():
    if not current_user.is_authenticated:
        raise SecurityException(msg="Only registered users can update their data")
    user = Person.query.get(request.form["id"])
    # Writing personal data requires the data owner's consent for the Core purpose
    # (update_user runs under the Core actual purpose).
    owner_consents = get_consent_tuples(user.consents)
    if user.name != request.form["name"]:
        if current_user.id != user.id:
            raise SecurityException(msg="Users can only edit their own name")
        if ('Person', 'name', 'Core') not in owner_consents:
            raise PrivacyException(msg="No consent to update name for the Core purpose")
        user.name = request.form["name"]
    if user.surname != request.form["surname"]:
        if current_user.id != user.id:
            raise SecurityException(msg="Users can only edit their own surname")
        if ('Person', 'surname', 'Core') not in owner_consents:
            raise PrivacyException(msg="No consent to update surname for the Core purpose")
        user.surname = request.form["surname"]
    if user.role.name != request.form["role"]:
        if current_user.role.name != "ADMIN":
            raise SecurityException(msg="Only administrators can edit roles")
        if ('Person', 'role', 'Core') not in owner_consents:
            raise PrivacyException(msg="No consent to update role for the Core purpose")
        user.role = Role.query.filter_by(name=request.form["role"]).first()
    if user.email != request.form["email"] and request.form["email"] not in ('RESTRICTED', 'None'):
        raise SecurityException(msg="Editing email is not allowed")
    db.session.commit()
    return request.form["id"]
        
def promote_manager(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    if not current_user.is_authenticated or current_user.id != event.owner.id:
        raise SecurityException(msg="Only event's owner can promote attendants to managers")
    if user not in event.managedBy:
        event.managedBy.append(user)
        db.session.commit()  

def demote_manager(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    if not current_user.is_authenticated or current_user.id != event.owner.id:
        raise SecurityException(msg="Only event's owner can demote managers to attendants")
    if id == event.owner.id:
        raise SecurityException(msg="Cannot demote the event's owner")
    if user in event.managedBy:
        event.managedBy.remove(user)
        db.session.commit()

def remove_attendee(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    manager_list = [event_manager.id for event_manager in event.managedBy]
    if not current_user.is_authenticated or (current_user.id != id and current_user.id not in manager_list):
        raise SecurityException(msg="Only managers can remove other attendees")
    if id in manager_list:
        raise SecurityException(msg="Cannot remove the event manager from event attendees")
    if ('Person', 'attends', 'Core') not in get_consent_tuples(user.consents):
        raise PrivacyException(msg="No consent to update attendance for the Core purpose")
    if user in event.attendants:
        event.attendants.remove(user)
        db.session.commit()

def accept_request(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    if not current_user.is_authenticated or current_user.id not in [event_manager.id for event_manager in event.managedBy]:
        raise SecurityException(msg="Only managers can accept request")
    if ('Person', 'attends', 'Core') not in get_consent_tuples(user.consents):
        raise PrivacyException(msg="No consent to update attendance for the Core purpose")
    if user not in event.attendants:
        event.attendants.append(user)
    event.requesters.remove(user)
    db.session.commit()

def reject_request(id,e):
    user = Person.query.get(id)
    event = Event.query.get(e)
    if not current_user.is_authenticated or (current_user.id != id and current_user.id not in [event_manager.id for event_manager in event.managedBy]):
        raise SecurityException(msg="Only managers can deny request")
    event.requesters.remove(user)
    db.session.commit()

def ads():  
    ads = AdDTO.copies(Ad.query.all())
    return {'ads' : ads}    

def remove_ad(id):
    if not current_user.is_authenticated or current_user.role.name != "ADMIN":
        raise SecurityException(msg="Only administrators can remove advertisement")    
    ad = Ad.query.get(id)
    db.session.delete(ad)
    db.session.commit()

def create_ad():
    if not current_user.is_authenticated or current_user.role.name != "ADMIN":
        raise SecurityException(msg="Only administrators can add advertisement") 
    content = request.form["content"]
    ad = Ad(content=content)
    db.session.add(ad)
    db.session.commit()

def recommend_events(user):
    subscriptions = user.subscriptions
    attending = user.attends
    events = [event for category in subscriptions for event in category.events]
    return list(set(events) - set(attending)) 
    
def get_personalize_ad(user):
    seed_string = f"{user.id}{user.name}{user.gender}"
    seed_value = int(hashlib.sha256(seed_string.encode()).hexdigest(), 16)
    random.seed(seed_value)
    ads = AdDTO.copies(Ad.query.all())
    if len(ads) == 0:
        return None
    else:
        return ads[random.randint(1, len(ads)) - 1]

def send_advertisement_to_user(user):
    if user.email:
        print(f'A generic advertisement was sent to {user.name} at email: {user.email}.', file=sys.stderr)


# ---------------------------------------------------------------------------
# Evolution endpoints (invitations + personalized stats)
# ---------------------------------------------------------------------------
def personalized_stats(id):
    user = Person.query.get(id)
    user_dto = PersonDTO.copy(user)
    # Security: a user only sees their own personalized statistics.
    if not current_user.is_authenticated or current_user.id != user.id:
        user_dto.manages = RESTRICTED
        user_dto.attends = RESTRICTED
        user_dto.subscriptions = RESTRICTED
        user_dto.invitations = RESTRICTED
    else:
        # Privacy: name/subscriptions/attends are used for the Stats purpose only if
        # the user attended more than two events and consented for Stats.
        consent_tuples = get_consent_tuples(current_user.consents)
        attended_gt2 = len(list(user.attends)) > 2
        if not (attended_gt2 and ('Person', 'attends', 'Stats') in consent_tuples):
            user_dto.attends = RESTRICTED
        if not (attended_gt2 and ('Person', 'subscriptions', 'Stats') in consent_tuples):
            user_dto.subscriptions = RESTRICTED
    return {'user' : user_dto}

def send_invite(id, e):
    if not current_user.is_authenticated:
        raise SecurityException(msg="Only authenticated users can create invitations")
    event = Event.query.get(e)
    if current_user.id not in [m.id for m in event.managedBy]:
        raise SecurityException(msg="Only event managers can invite users to the event")
    user = Person.query.get(id)
    if user.id in [r.id for r in event.requesters] or user.id in [a.id for a in event.attendants]:
        raise SecurityException(msg="Cannot invite a user who already requested or attends the event")
    invite = Invite(event=event, invitedBy=current_user, invitee=user)
    db.session.add(invite)
    db.session.commit()

def accept_invitation(id):
    invite = Invite.query.get(id)
    if not current_user.is_authenticated or current_user.id != invite.invitee.id:
        raise SecurityException(msg="Only the invitee can accept the invitation")
    event = invite.event
    user = invite.invitee
    if ('Person', 'attends', 'Core') not in get_consent_tuples(user.consents):
        raise PrivacyException(msg="No consent to update attendance for the Core purpose")
    event.attendants.append(user)
    db.session.delete(invite)
    db.session.commit()

def decline_invitation(id):
    invite = Invite.query.get(id)
    event = invite.event
    if not current_user.is_authenticated or (
        current_user.id != invite.invitee.id
        and current_user.id != invite.invitedBy.id
        and current_user.id not in [m.id for m in event.managedBy]):
        raise SecurityException(msg="Not allowed to cancel this invitation")
    db.session.delete(invite)
    db.session.commit()

def get_invite_candidates(event):
    all_users = Person.query.all()
    invitees = [i.invitee.id for i in event.invitations]
    attendants = [a.id for a in event.attendants]
    requesters = [r.id for r in event.requesters]
    users = [u for u in all_users if u.id not in invitees and u.id not in attendants and u.id not in requesters]
    return PersonDTO.copies(users)
