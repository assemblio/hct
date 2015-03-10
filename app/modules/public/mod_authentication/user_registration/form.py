from flask_wtf import Form
from wtforms import PasswordField, RadioField, StringField
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
    role = RadioField(
        'Label',
        choices=[('employer','Employer'),('recruiter','Recruiter')])

    name = StringField(
        'name',
        validators=[DataRequired(), Length(min=6, max=40)])

    surname = StringField(
        'email',
        validators=[DataRequired(), Length(min=6, max=40)])

    date_of_birth = StringField(
        'date_of_birth',
        validators=[DataRequired(), Length(min=6, max=40)])

    phone_mobile = StringField(
        'phone',
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

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.objects(email=self.email.data)
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True