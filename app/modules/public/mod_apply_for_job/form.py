from flask_wtf import Form
from wtforms import StringField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo

class CreateJob(Form):
    title = StringField(
        'title',
        validators=[DataRequired(), Length(min=6, max=40)])

    date = DateTimeField(
        'date',
        validators=[DataRequired(), Length(min=10, max=40)])

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
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.objects(email=self.email.data)
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True