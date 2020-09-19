from flask_wtf import FlaskForm
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
	