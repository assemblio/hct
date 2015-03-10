from app import db

class Job(db.Document):
    title = db.StringField(max_length=255)
    #date = db.DateTimeField()
    location = db.StringField()
    description = db.StringField()
    requirements = db.StringField()
