from collections import OrderedDict

import json

from sqlalchemy import create_engine
from sqlalchemy import Sequence
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref

from sqlalchemy.exc import IntegrityError

class Db():

    def __init__(self, name):
        self.engine = create_engine("sqlite:///{}".format(name), echo=False)
        self.Base = declarative_base()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        class User(self.Base):
            __tablename__ = 'users'

            id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
            email = Column(String(254), unique=True)
            name = Column(String(773)) # Wolfe+585, Sr.
            password = Column(String)

            def get_json(self):
                d = OrderedDict()
                d['id'] = self.id
                d['email'] = self.email
                d['name'] = self.name
                d['password'] = self.password

                return json.dumps(d)

            def __repr__(self):
                return "User" + str(self.get_json())
        self.User = User

        class Group(self.Base):
            __tablename__ = 'groups'

            id = Column(Integer, Sequence('group_id_seq'), primary_key=True)
            name = Column(String(254), unique=True)

            def get_json(self):
                d = OrderedDict()
                d['id'] = self.id
                d['name'] = self.name

                return json.dumps(d)

            def __repr__(self):
                return "Group" + str(self.get_json())
        self.Group = Group

        #class Event(self.Base):
            #__tablename__ = 'events'

            #id = Column(Integer, Sequence('event_id_seq'), primary_key=True)
            #name = Column(String(500))
            #desc = Column(String(2000))
            #resurant_id = Column(Integer, ForeignKey('resturants.id'))
            #group_id = Column(Integer, ForeignKey('groups.id'))
            #time = Column(Integer)

            #resturant = relationship("resturants")

            #def get_json(self):
                #d = OrderedDict()
                #d['id'] = self.id
                #d['name'] = self.name
                #d['desc'] = self.desc
                #d['resturant_id'] = self.resturant_id
                #d['time'] = self.time
                #d['group'] = self.group

                #return json.dumps(d)

            #def __repr__(self):
                #return "Event" + str(self.get_json())
        #self.Event = Event

        #class Resturant(self.Base):
            #__tablename__ = 'resturants'

            #id = Column(Integer, Sequence('resturant_id_seq'), primary_key=True)
            #name = Column(String(500))
            #address = Column(String(500))

            #def get_json(self):
                #d = OrderedDict()
                #d['id'] = self.id
                #d['name'] = self.name
                #d['address'] = self.address

                #return json.dumps(d)

            #def __repr__(self):
                #return "Resturant" + str(self.get_json())
        #self.Resturant = Resturant

        #class UserGroup(self.Base):
            #__tablename__ = 'usergroup'

            #id = Column(Integer, Sequence('usergroup_id_seq'), primary_key=True)
            #user_id = Column(Integer, ForeignKey('users.id'))
            #group_id = Column(Integer, ForeignKey('groups.id'))
            #is_admin = Column(Boolean)

            #def get_json(self):
                #d = OrderedDict()
                #d['id'] = self.id
                #d['user_id'] = self.user_id
                #d['group_id'] = self.group_id
                #d['is_admin'] = self.is_admin

                #return json.dumps(d)

            #def __repr__(self):
                #return "UserGroup" + str(self.get_json())
        #self.UserGroup = UserGroup

        #class UserEvent(self.Base):
            #__tablename__ = 'userevent'

            #id = Column(Integer, Sequence('userevent_id_seq'), primary_key=True)
            #user_id = Column(Integer, ForeignKey('users.id'))
            #event_id = Column(Integer, ForeignKey('events.id'))

            #def get_json(self):
                #d = OrderedDict()
                #d['id'] = self.id
                #d['user_id'] = self.user_id
                #d['event_id'] = self.event_id

                #return json.dumps(d)

            #def __repr__(self):
                #return "UserEvent" + str(self.get_json())
        #self.UserEvent = UserEvent


        self.Base.metadata.create_all(self.engine)


