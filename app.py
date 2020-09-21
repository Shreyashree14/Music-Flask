from flask import Flask,redirect,render_template,url_for,flash,send_file,request
from flask_login import LoginManager,login_user,logout_user,current_user,login_required
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import secrets,os

app=Flask(__name__)
app.config["SECRET_KEY"]="fd7a97d9ce9bf2c7af93d4f5f83338f5"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///site.db"
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

from models import User,Song
from forms import RegistrationForm,LoginForm,UploadForm,SearchForm

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

@app.route("/user",methods=["POST","GET"])
@login_required
def user():
	form=SearchForm()
	if form.validate_on_submit():
		title=form.title.data+"%"
		artist=form.artist.data+"%"
		album=form.album.data+"%"
		songs=Song.query.filter(Song.title.like(title),Song.artist.like(artist),Song.album.like(album))
	else:
		songs=Song.query.order_by(Song.title.asc()).all()
	return render_template('user.html',title="User Page",songs=songs,form=form)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	flash("Logged Out","success")
	return redirect(url_for('home'))

def save_file(file,path):
	random_name=secrets.token_hex(8)
	_,ext=os.path.splitext(file.filename)
	new_filename=random_name+ext
	new_filepath=os.path.join(app.root_path,path,new_filename)
	file.save(new_filepath)
	return new_filename
	
@app.route("/upload",methods=["POST","GET"])
@login_required
def upload():
	form=UploadForm()
	if form.validate_on_submit():
		file=save_file(form.file.data,"static")
		song=Song(title=form.title.data,artist=form.artist.data,album=form.album.data,file=file,user=current_user)
		db.session.add(song)
		db.session.commit()
		flash("Song uploaded successfully","success")
		return redirect(url_for('user'))
	return render_template("upload.html",title="Upload Song",form=form)

@app.route("/<song_id>")
@login_required	
def song_page(song_id):
	song=Song.query.filter_by(id=song_id).first()
	return render_template("song_page.html",title="Song Page",song=song)

@app.route("/<song_id>/download")
@login_required
def download(song_id):
	song=Song.query.filter_by(id=song_id).first()
	file=os.path.join(app.root_path,"static",song.file)
	return send_file(file,as_attachment=True,attachment_filename=song.title)
	
@app.route("/<song_id>/delete",methods=['POST','GET'])
@login_required	
def delete(song_id):
	if request.method=="POST":
		Song.query.filter_by(id=song_id).delete()
		db.session.commit()
		flash("Song deleted successfully","success")
	return redirect(url_for('my_uploads'))
	
@app.route("/myuploads")
@login_required
def my_uploads():
	songs=Song.query.filter_by(user=current_user)
	return render_template('my_uploads.html',title="My Uploads",songs=songs)

@app.route("/allsongs")
@login_required
def all_songs():	
	songs=Song.query.order_by(Song.title.asc()).all()
	return render_template('all_songs.html',title="All Songs",songs=songs)

	
if __name__=='__main__':
	app.run(debug=True)