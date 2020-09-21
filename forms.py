from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from models import User
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo,ValidationError

class RegistrationForm(FlaskForm):
	email=StringField("Email-id",validators=[DataRequired(),Email()])
	password=PasswordField("Password",validators=[DataRequired()])
	conf_password=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])
	submit=SubmitField("Sign Up")
	
	def validate_email(self,email):
		user=User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("Email already exists! Enter a different email id")
			
class LoginForm(FlaskForm):
	email=StringField("Email-id",validators=[DataRequired(),Email()])
	password=PasswordField("Password",validators=[DataRequired()])
	submit=SubmitField("Sign In")

class UploadForm(FlaskForm):
	title=StringField("Title",validators=[DataRequired()])
	artist=StringField("Artist",validators=[DataRequired()])
	album=StringField("Album",validators=[DataRequired()])
	file=FileField("Song Upload",validators=[DataRequired(),FileAllowed(['mp3'])])
	submit=SubmitField("Upload")
	
class SearchForm(FlaskForm):
	title=StringField("Title")
	artist=StringField("Artist")
	album=StringField("Album")
	submit=SubmitField("Search")
	
