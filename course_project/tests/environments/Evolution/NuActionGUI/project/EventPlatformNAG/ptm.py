from model import Action, Constraint
from enum import auto, Enum
from privacy_model import PrivacyModel
import dtm

class EventPlatformNAGPrivacyModel(PrivacyModel):

    # Extensible model (default: nothing declared)

    class Purpose(Enum):
        
        ANY = auto()
        MARKETING = auto()
        TARGETEDMARKETING = auto()
        MASSMARKETING = auto()
        INSIGHTS = auto()
        ANALYTICS = auto()
        STATS = auto()
        FUNCTIONAL = auto()
        RECOMMENDEVENTS = auto()
        CORE = auto()
        
        

        def get_subpurposes_names(self):
            ret = []
            for sp in purpose_hierarchy[self]:
                ret.append(sp.name)
                ret.extend(sp.get_subpurposes_names())
            return ret

    personaldata = [
        {'resource': 'Person', 'subresource': 'name'},
        {'resource': 'Person', 'subresource': 'surname'},
        {'resource': 'Person', 'subresource': 'role'},
        {'resource': 'Person', 'subresource': 'gender'},
        {'resource': 'Person', 'subresource': 'email'},
        {'resource': 'Person', 'subresource': 'subscriptions'},
        {'resource': 'Person', 'subresource': 'attends'}
        ]
        
    model = [(Purpose.MARKETING, [{'resource': 'Person', 'subresource': 'name'}], Constraint.fullAccess, 'true'), (Purpose.CORE, [{'resource': 'Person', 'subresource': 'name'}], Constraint.fullAccess, 'true'), (Purpose.CORE, [{'resource': 'Person', 'subresource': 'surname'}], Constraint.fullAccess, 'true'), (Purpose.CORE, [{'resource': 'Person', 'subresource': 'role'}], Constraint.fullAccess, 'true'), (Purpose.CORE, [{'resource': 'Person', 'subresource': 'gender'}], Constraint.fullAccess, 'true'), (Purpose.CORE, [{'resource': 'Person', 'subresource': 'email'}], Constraint.fullAccess, 'true'), (Purpose.CORE, [{'resource': 'Person', 'subresource': 'subscriptions'}], Constraint.fullAccess, 'true'), (Purpose.RECOMMENDEVENTS, [{'resource': 'Person', 'subresource': 'subscriptions'}], lambda self= None: self.role == dtm.Role.REGULARUSER, 'you are a regular user'), (Purpose.TARGETEDMARKETING, [{'resource': 'Person', 'subresource': 'gender'}], Constraint.fullAccess, 'true'), (Purpose.MASSMARKETING, [{'resource': 'Person', 'subresource': 'email'}], Constraint.fullAccess, 'true'), (Purpose.ANALYTICS, [{'resource': 'Person', 'subresource': 'gender'}], Constraint.fullAccess, 'true'), (Purpose.FUNCTIONAL, [{'resource': 'Person', 'subresource': 'attends'}], Constraint.fullAccess, 'true'), (Purpose.STATS, [{'resource': 'Person', 'subresource': 'name'}], lambda self= None: self.attends.size() > 2, 'you attended more than two events'), (Purpose.STATS, [{'resource': 'Person', 'subresource': 'subscriptions'}], lambda self= None: self.attends.size() > 2, 'you attended more than two events'), (Purpose.STATS, [{'resource': 'Person', 'subresource': 'attends'}], lambda self= None: self.attends.size() > 2, 'you attended more than two events')]

purpose_hierarchy = {
    EventPlatformNAGPrivacyModel.Purpose.ANY: [
        EventPlatformNAGPrivacyModel.Purpose.MARKETING, 
        EventPlatformNAGPrivacyModel.Purpose.INSIGHTS, 
        EventPlatformNAGPrivacyModel.Purpose.FUNCTIONAL
    ], 
    EventPlatformNAGPrivacyModel.Purpose.MARKETING: [
        EventPlatformNAGPrivacyModel.Purpose.TARGETEDMARKETING, 
        EventPlatformNAGPrivacyModel.Purpose.MASSMARKETING
    ], 
    EventPlatformNAGPrivacyModel.Purpose.TARGETEDMARKETING: [
    ], 
    EventPlatformNAGPrivacyModel.Purpose.MASSMARKETING: [
    ], 
    EventPlatformNAGPrivacyModel.Purpose.INSIGHTS: [
        EventPlatformNAGPrivacyModel.Purpose.ANALYTICS, 
        EventPlatformNAGPrivacyModel.Purpose.STATS
    ], 
    EventPlatformNAGPrivacyModel.Purpose.ANALYTICS: [
    ], 
    EventPlatformNAGPrivacyModel.Purpose.STATS: [
    ], 
    EventPlatformNAGPrivacyModel.Purpose.FUNCTIONAL: [
        EventPlatformNAGPrivacyModel.Purpose.RECOMMENDEVENTS, 
        EventPlatformNAGPrivacyModel.Purpose.CORE
    ], 
    EventPlatformNAGPrivacyModel.Purpose.RECOMMENDEVENTS: [
    ], 
    EventPlatformNAGPrivacyModel.Purpose.CORE: [
    ]
}

EventPlatformNAGPrivacyModel.validate()