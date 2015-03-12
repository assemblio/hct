from flask_wtf import Form
from wtforms import StringField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo

class CreateJob(Form):
    title = StringField(
        'title',
        validators=[DataRequired(), Length(min=6, max=40)])
    date = DateField(
        'date', format="%Y-%m-%d",
        validators=[DataRequired()])
    location = StringField(
        'location',
        validators=[DataRequired(), Length(min=6, max=40)])

    description = TextAreaField(
        'description',
        validators=[DataRequired(), Length(min=6, max=100)])

    requirements = TextAreaField(
        'requirements',
        validators=[DataRequired(), Length(min=6, max=100)])

    def validate(self):
        initial_validation = super(CreateJob, self).validate()
        if not initial_validation:
            return False
        return True