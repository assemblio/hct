from app import db
from flask.ext.security import UserMixin, RoleMixin


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class Experience(db.EmbeddedDocument):
    exp_id = db.StringField()
    companyName = db.StringField()
    startDateWork = db.DateTimeField()
    endDateWork = db.DateTimeField()
    workPosition = db.StringField()
    companyLocation = db.StringField()
    experienceDescription = db.StringField()


class Education(db.EmbeddedDocument):
    school = db.StringField()
    fieldOfStudy = db.StringField()
    schoolDegree = db.StringField()
    startDateSchool = db.DateTimeField()
    endDateSchool = db.DateTimeField()
    schoolDescription = db.StringField()


class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])
    behaviour = db.StringField(max_length=255)
    first_name = db.StringField(max_length=255)
    last_name = db.StringField(max_length=255)
    dateOfBirth =db.DateTimeField()
    phone_mobile = db.StringField()
    phone_work = db.StringField()
    fax = db.StringField()
    address1 = db.StringField()
    address2 = db.StringField()
    expected_salary = db.StringField()
    trainings = db.StringField()
    jobs_applied = db.StringField()
    next = db.StringField()
    cvSummary = db.StringField()
    country = db.StringField()
    stateProvince = db.StringField()
    city = db.StringField()
    zipCode = db.IntField()
    experience = db.ListField(db.EmbeddedDocumentField(Experience))
    education = db.ListField(db.EmbeddedDocumentField(Education))


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
