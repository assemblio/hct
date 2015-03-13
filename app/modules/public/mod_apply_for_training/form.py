from flask_wtf import Form
from wtforms import StringField, DateField, TextAreaField, IntegerField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length


class RegisterTraining(Form):
    title = StringField(
        'title',
        validators=[DataRequired(), Length(max=40)])

    startDate = DateField(
        'startDate', format="%Y-%m-%d",
        validators=[DataRequired()])

    endDate = DateField(
        'endDate', format="%Y-%m-%d",
        validators=[DataRequired()])

    space = IntegerField(
        'space',
        validators=[DataRequired()])

    instructorName = StringField(
        'instructorName',
        validators=[DataRequired(), Length( max=40)])

    instructorSurname = StringField(
        'instructorSurname',
        validators=[DataRequired(), Length( max=40)])

    agenda = TextAreaField(
        'agenda',
        validators=[DataRequired(), Length(max=100)])

    short_description = TextAreaField(
        'Short description.',
        validators=[DataRequired(), Length(min=100, max=300)])

    description = TextAreaField(
        'Description',
        validators=[DataRequired(), Length(min=300, max=500)])

    requirements = TextAreaField(
        'requirements',
        validators=[DataRequired(), Length(max=100)])

    target_group = SelectMultipleField(
        'Target Group!',
        choices=[
            ('students', 'Students'),
            ('employees', 'Employees'),
            ('delemployees', 'Deloitte Employees'),
            ('nondelemployees', 'Non Deloitte Employees')
        ],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
        )

    def validate(self):
        initial_validation = super(RegisterTraining, self).validate()
        if not initial_validation:
            return False
        return True