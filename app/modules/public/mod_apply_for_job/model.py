from app import db

class Job(db.Document):
    title = db.StringField()
    date = db.DateTimeField()
    location = db.StringField()
    description = db.StringField()
    requirements = db.StringField()
    applicants = db.StringField()
