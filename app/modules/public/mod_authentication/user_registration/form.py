from flask_wtf import Form
from wtforms import \
    PasswordField, RadioField, StringField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo


from app.modules.public.mod_authentication.user_registration.model import User


class LoginForm(Form):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(Form):
    email = StringField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    behaviour = RadioField(
        'Label',
        choices=[
        ('employer', 'Employer'),
        ('recruiter', 'Recruiter')]
    )

    first_name = StringField(
        'first_name',
        validators=[DataRequired(), Length(min=6, max=40)])

    last_name = StringField(
        'email',
        validators=[DataRequired(), Length(min=6, max=40)])

    phone_mobile = StringField(
        'phone_mobile',
        validators=[DataRequired(), Length(min=6, max=40)])

    phone_work = StringField(
        'phone_work',
        validators=[DataRequired(), Length(min=6, max=40)])

    fax = StringField(
        'fax',
        validators=[DataRequired(), Length(min=6, max=40)])

    address1 = StringField(
        'address1',
        validators=[DataRequired(), Length(min=6, max=40)])

    address2 = StringField(
        'address2',
        validators=[DataRequired(), Length(min=6, max=40)])

    expected_salary = StringField(
        'expected_salary',
        validators=[DataRequired(), Length(min=6, max=40)])

    school = StringField(
        'school',
        validators=[DataRequired(), Length(min=6, max=40)])

    fieldOfStudy = StringField(
        'fieldOfStudy',
        validators=[DataRequired(), Length(min=6, max=40)])

    schoolDegree = StringField(
        'schoolDegree',
        validators=[DataRequired(), Length(min=6, max=40)])

    startDateSchool = DateField(
        'startDateSchool', format="%Y-%m-%d",
        validators=[DataRequired()])

    endDateSchool = DateField(
        'endDateSchool', format="%Y-%m-%d",
        validators=[DataRequired()])

    schoolDescription = TextAreaField(
        'schoolDescription',
        validators=[DataRequired(), Length(min=10, max=500)])

    companyName = StringField(
        'companyName',
        validators=[DataRequired(), Length(min=6, max=40)])

    startDateWork = DateField(
        'startDateSchool', format="%Y-%m-%d",
        validators=[DataRequired()])

    endDateWork = DateField(
        'endDateWork', format="%Y-%m-%d",
        validators=[DataRequired()])

    workPosition = StringField(
        'companyName',
        validators=[DataRequired(), Length(min=6, max=40)])

    companyLocation = StringField(
        'companyLocation',
        validators=[DataRequired(), Length(min=6, max=40)])

    experienceDescription = TextAreaField(
        'experienceDescription',
        validators=[DataRequired(), Length(min=10, max=600)])

    cvSummary = TextAreaField(
        'cvSummary',
        validators=[DataRequired(), Length(min=10, max=1600)])

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.objects(email=self.email.data)
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True
