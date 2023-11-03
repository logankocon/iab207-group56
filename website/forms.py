from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, IntegerField, SelectField, DateField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name'), Length(min=3, max=30)], render_kw={'class':'form-control rounded border border-secondary'})
    password=PasswordField("Password", validators=[InputRequired('Enter user password'), Length(min=3, max=30)], render_kw={'class':'form-control rounded border border-secondary'})
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired(), Length(min=3, max=30)], render_kw={'class':'form-control rounded border border-secondary'})
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email"), Length(min=3, max=45)], render_kw={'class':'form-control rounded border border-secondary'})
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(), Length(min=3, max=30),
                  EqualTo('confirm', message="Passwords should match")], render_kw={'class':'form-control rounded border border-secondary'})
    confirm = PasswordField("Confirm Password", validators=[InputRequired(), Length(min=3, max=30)], render_kw={'class':'form-control rounded border border-secondary'})

    #submit button
    submit = SubmitField("Register")


ALLOWED_FILE = {"PNG", "JPG", "JPEG", "png", "jpg", "jpeg"}

#create new event form
class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[InputRequired(), Length(min=3, max=50)], render_kw={'class':'form-control rounded border border-secondary'})
    artist = StringField('Event Artist', validators=[InputRequired('Pleae enter an event artist.'), Length(min=3, max=75)], render_kw={'class':'form-control rounded border border-secondary'})
    description = TextAreaField('Description', render_kw={'class':'form-control rounded border border-secondary'},
            validators=[InputRequired('Pleae enter a description.'), Length(min=3, max=500)])
    location = StringField('Event Location', validators = [InputRequired('Pleae enter a location.'), Length(min=3, max=50)], render_kw={'class':'form-control rounded border border-secondary'})

    image = FileField('Event Image', validators = [
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')], render_kw={'class':'form-control rounded border border-secondary'})
    tickets = IntegerField('Available Tickets', validators = [InputRequired('Pleae enter available tickets.')], render_kw={'class':'form-control rounded border border-secondary'})
    date = DateField('Event Date', format='%Y-%m-%d', validators=[InputRequired('Please enter an event date.')], render_kw={'class': 'form-control rounded border border-secondary datepicker'})
    time_choices = []
    for hour in range(24):
        for minute in ["00", "30"]:
            time_value = f"{str(hour).zfill(2)}:{minute}"
            time_choices.append((time_value, time_value))
    time = SelectField('Event Time', choices=time_choices, validators=[InputRequired('Please select an event time')], render_kw={'class': 'form-control rounded border border-secondary'})

    genre = StringField('Event Genre', validators=[InputRequired('Pleae enter an event genre.'), Length(min=3, max=50)], render_kw={'class':'form-control rounded border border-secondary'})
    submit = SubmitField('Create', render_kw={'class':'form-control rounded border border-secondary'})

class EditEventForm(FlaskForm):
    name = StringField('Event Name', validators=[InputRequired(), Length(min=3, max=50)], render_kw={'class':'form-control rounded border border-secondary'})
    artist = StringField('Event Artist', validators=[InputRequired('Pleae enter an event artist.'), Length(min=3, max=75)], render_kw={'class':'form-control rounded border border-secondary'})
    description = TextAreaField('Description', render_kw={'class':'form-control rounded border border-secondary'},
            validators=[InputRequired('Pleae enter a description.'), Length(min=3, max=500)])
    location = StringField('Event Location', validators = [InputRequired('Pleae enter a location.'), Length(min=3, max=50)], render_kw={'class':'form-control rounded border border-secondary'})

    image = FileField('Event Image', validators = [
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')], render_kw={'class':'form-control rounded border border-secondary'})
    tickets = IntegerField('Available Tickets', validators = [InputRequired('Pleae enter available tickets.')], render_kw={'class':'form-control rounded border border-secondary'})
    date = DateField('Event Date', format='%Y-%m-%d', validators=[InputRequired('Please enter an event date.')], render_kw={'class': 'form-control rounded border border-secondary datepicker'})
    time_choices = []
    for hour in range(24):
        for minute in ["00", "30"]:
            time_value = f"{str(hour).zfill(2)}:{minute}"
            time_choices.append((time_value, time_value))
    time = SelectField('Event Time', choices=time_choices, validators=[InputRequired('Please select an event time')], render_kw={'class': 'form-control rounded border border-secondary'})
    genre = StringField('Event Genre', validators=[InputRequired('Pleae enter an event genre.'), Length(min=3, max=50)], render_kw={'class':'form-control rounded border border-secondary'})
    cancel = BooleanField('Cancel Event?', render_kw={'class':'border border-secondary'})
    submit = SubmitField('Save Changes', render_kw={'class':'form-control rounded border border-secondary'})

    

class BookingForm(FlaskForm):
    tickets = tickets = IntegerField('Tickets to Purchase', validators = [InputRequired()], render_kw={'class':'form-control rounded border border-secondary'})
    submit = SubmitField('Book', render_kw={'class':'form-control rounded border border-secondary'})

#comment form
class CommentForm(FlaskForm):
    text = TextAreaField('Comment', [InputRequired(), Length(min=3, max=140)], render_kw={'class':'form-control rounded border border-secondary'})
    submit = SubmitField('Post')
