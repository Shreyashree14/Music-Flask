from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from models import User
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo,ValidationError,Length

class RegistrationForm(FlaskForm):
	email=StringField("Email-id",validators=[DataRequired(),Email()])
	password=PasswordField("Password",validators=[DataRequired(),Length(min=6,max=10)])
	conf_password=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])
	submit=SubmitField("Sign Up")
	
	def validate_email(self,email):
		user=User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("Email already exists! Enter a different email id")
			
	def validate_password(self,password):
		upper, lower, number, special = 0, 0, 0, 0
		for i in range(len(password.data)): 
			if password.data[i].isupper(): 
				upper += 1
			elif password.data[i].islower(): 
				lower += 1
			elif password.data[i].isdigit(): 
				number += 1
			else: 
				special += 1 
		if upper==0 or lower==0 or number==0 or special==0:
			raise ValidationError("Password should contain atleast 1 uppercase, lowercase, number and special character")
			
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
	
