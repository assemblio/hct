from flask_wtf import Form
from wtforms import StringField, DateField, TextAreaField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, EqualTo

class CreateJob(Form):
    title = StringField(
        'title',
        validators=[DataRequired(), Length(max=40)])
    date = DateField(
        'date', format="%Y-%m-%d",
        validators=[DataRequired()])
    location = StringField(
        'location',
        validators=[DataRequired(), Length(max=40)])

    short_description = TextAreaField(
        'Short description.',
        validators=[DataRequired(), Length(max=300)])

    description = TextAreaField(
        'Description',
        validators=[DataRequired(), Length(max=500)])

    requirements = TextAreaField(
        'requirements',
        validators=[DataRequired(), Length(max=500)])

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

    industry = SelectMultipleField(
        'Industry!',
        choices=[
            ('administration', 'Administration'),
            ('manufactoring', 'Manufactoring'),
            ('healthcare', 'Healthcare'),
            ('it', 'IT'),
            ('marketing', 'Marketing'),
            ('transportation', 'Transportation')
        ],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
        )


    def validate(self):
        initial_validation = super(CreateJob, self).validate()
        if not initial_validation:
            return False
        return True