from flask_wtf import Form
from wtforms import StringField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, Length
import datetime
class RegisterTraining(Form):
    title = StringField(
        'title',
        validators=[DataRequired(), Length(min=6, max=40)])

    startDate = DateTimeField(
        'startDate',format="%Y-%m-%dT%H:%M:%S",
        validators=[DataRequired()])

    endDate = DateTimeField(
        'endDate', format="%Y-%m-%dT%H:%M:%S",
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
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.objects(email=self.email.data)
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True