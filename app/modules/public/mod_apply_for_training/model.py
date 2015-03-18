from app import db

class Training(db.Document):
    title = db.StringField(max_length=255)
    startDate = db.DateTimeField()
    endDate = db.DateTimeField()
    space = db.IntField()
    instructorName = db.StringField(max_length=255)
    instructorSurname = db.StringField(max_length=255)
    agenda = db.StringField()
    short_description = db.StringField()
    description = db.StringField()
    requirements = db.StringField()
    participants = db.StringField()
    target_group = db.ListField()