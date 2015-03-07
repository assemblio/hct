from app import db
from flask.ext.security import UserMixin, RoleMixin

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])
    role = db.StringField(max_length=255)
    name = db.StringField(max_length=255)
    surname = db.StringField(max_length=255)
    date_of_birth = db.DateTimeField()
    phone = db.StringField()
    address1 = db.StringField()
    address2 = db.StringField()
    expected_salary = db.StringField()


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<email {}'.format(self.email)
