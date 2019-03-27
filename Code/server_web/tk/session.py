from flask_login import UserMixin
from random import choice
from .db import database
import uuid

HomeDB = database('db/home.db')

def get_info(email=None, id=None):
    if id:
        return HomeDB.select('ID = %s' % id)
    return HomeDB.select('Email = "%s"' % email)

class User(UserMixin):
    def __init__(self, email=None, **kwar):
        self._email = email
        if not kwar:
            self.get_info(email)
        else:
            self._id = kwar['id']
            self._password = kwar['password']
            self._username = kwar['username']
            self._date = kwar['date']
            self._money = kwar['money']
            self._mode = 'menber'

    def __repr__(self):
        return '-'.join(map(str, [self._id, self._username, self._password, 
                        self._email, self._money, self._mode]))
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        raise AttributeError('password does not support resetting in this version')

    def verify_password(self, password):
        if password != self._password:
            return False
        return True

    def get_id(self):
        return self._id

    def get_info(self, email=None, id=None):
        menber = get_info(email, id)
        if menber != []:
            self._id = menber[0][0]
            self._username = menber[0][1].encode('utf-8')
            self._password = menber[0][2]
            self._email = menber[0][3]
            self._date = menber[0][4]
            self._money = menber[0][5]
            self._mode = 'member'
        else:
            self._id = uuid.uuid4().int
            self._username = choice(['Jack', 'Henry', 'Iris', 'Julie'])
            self._password = None
            self._email = None
            self._date = 20180101
            self._money = 0
            self._mode = 'guest'

    @staticmethod
    def get(user_id):
        if not user_id:
            return None
        menber = get_info(None, user_id)
        if menber == []:
            return None
        return User(email=menber[0][3],
                    id=menber[0][0],
                    username=menber[0][1],
                    password=menber[0][2],
                    date=menber[0][4],
                    money=menber[0][5])
        



        
