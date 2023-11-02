from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')], render_kw={'class':'form-control rounded border border-secondary'})
    password=PasswordField("Password", validators=[InputRequired('Enter user password')], render_kw={'class':'form-control rounded border border-secondary'})
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()], render_kw={'class':'form-control rounded border border-secondary'})
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")], render_kw={'class':'form-control rounded border border-secondary'})
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")], render_kw={'class':'form-control rounded border border-secondary'})
    confirm = PasswordField("Confirm Password", render_kw={'class':'form-control rounded border border-secondary'})

    #submit button
    submit = SubmitField("Register")


ALLOWED_FILE = {"PNG", "JPG", "JPEG", "png", "jpg", "jpeg"}

#create new event form
class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[InputRequired()], render_kw={'class':'form-control rounded border border-secondary'})
    artist = StringField('Event Artist', validators=[InputRequired()], render_kw={'class':'form-control rounded border border-secondary'})
    description = TextAreaField('Description', render_kw={'class':'form-control rounded border border-secondary'},
            validators=[InputRequired()])
    location = StringField('Event Location', validators = [InputRequired()], render_kw={'class':'form-control rounded border border-secondary'})

    image = FileField('Event Image', validators = [
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')], render_kw={'class':'form-control rounded border border-secondary'})
    tickets = StringField('Available Tickets', validators = [InputRequired()], render_kw={'class':'form-control rounded border border-secondary'})
    date = StringField('Event Date', validators = [InputRequired()], render_kw={'class':'form-control rounded border border-secondary'})
    time = StringField('Event TIme', validators = [InputRequired()], render_kw={'class':'form-control rounded border border-secondary'})
    genre = StringField('Event Genre', validators=[InputRequired()], render_kw={'class':'form-control rounded border border-secondary'})
    submit = SubmitField('Create', render_kw={'class':'form-control rounded border border-secondary'})

class BookingForm(FlaskForm):
    tickets = tickets = StringField('Tickets to Purchase', validators = [InputRequired()], render_kw={'class':'form-control rounded border border-secondary'})
    submit = SubmitField('Book', render_kw={'class':'form-control rounded border border-secondary'})

#comment form
class CommentForm(FlaskForm):
    text = TextAreaField('Comment', [InputRequired()])
    submit = SubmitField('Post')
