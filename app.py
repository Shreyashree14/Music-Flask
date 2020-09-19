from flask import Flask,redirect,render_template,url_for,flash
from flask_login import LoginManager,login_user,logout_user,current_user,login_required
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app=Flask(__name__)
app.config["SECRET_KEY"]="fd7a97d9ce9bf2c7af93d4f5f83338f5"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///site.db"
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

from models import User
from forms import RegistrationForm,LoginForm

@app.route("/")
def home():
	return render_template('home.html')
	
@app.route('/register',methods=["GET","POST"])
def register():
	form=RegistrationForm()
	if form.validate_on_submit():
		hashed_pass=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user=User(email=form.email.data,password=hashed_pass)
		db.session.add(user)
		db.session.commit()
		flash(f"Account Created","success")
		return redirect(url_for('login'))
	return render_template('register.html',form=form,title="Registration Page")
	

@app.route('/login',methods=["GET","POST"])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user)
			flash(f"Logged In",'success')
			return redirect(url_for('user'))
		else:
			flash(f"Login Unsuccessful","danger")
			return redirect(url_for('login'))
	return render_template('login.html',form=form,title="Login Page")

@app.route("/user")
@login_required
def user():
	return render_template('user.html',title="User Page")

@app.route("/logout")
@login_required
def logout():
	logout_user()
	flash("Logged Out","success")
	return redirect(url_for('home'))


	
if __name__=='__main__':
	app.run(debug=True)