from flask_wtf import Form
from wtforms import StringField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length
import datetime
class RegisterTraining(Form):
    title = StringField(
        'title',
        validators=[DataRequired(), Length(min=6, max=40)])

    startDate = DateField(
        'startDate', format="%Y-%m-%d",
        validators=[DataRequired()])

    endDate = DateField(
        'endDate', format="%Y-%m-%d",
        validators=[DataRequired()])

    space = StringField(
        'space',
        validators=[DataRequired(), Length(min=6, max=40)])

    instructorName = StringField(
        'instructorName',
        validators=[DataRequired(), Length(min=6, max=40)])

    instructorSurname = StringField(
        'instructorSurname',
        validators=[DataRequired(), Length(min=6, max=40)])

    agenda = TextAreaField(
        'agenda',
        validators=[DataRequired(), Length(min=6, max=100)])

    description = TextAreaField(
        'description',
        validators=[DataRequired(), Length(min=6, max=100)])

    requirements = TextAreaField(
        'requirements',
        validators=[DataRequired(), Length(min=6, max=100)])

    def validate(self):
        initial_validation = super(RegisterTraining, self).validate()
        if not initial_validation:
            return False
        return True