from app import db

class Job(db.Document):
    title = db.StringField()
    date = db.DateTimeField()
    location = db.StringField()
    short_description = db.StringField()
    description = db.StringField()
    requirements = db.StringField()
    applicants = db.StringField()
    target_group = db.StringField()

