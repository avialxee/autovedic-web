from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, id, name='', password=''):
        self.id = id
        self.name = name
        self.password = password
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)

    