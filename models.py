from app import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
	
class User(db.Model,UserMixin):
	id=db.Column(db.Integer,primary_key=True)
	email=db.Column(db.String(30),nullable=False,unique=True)
	password=db.Column(db.String(60),nullable=False)
	song=db.relationship('Song',backref="user",lazy=True)
	
	def __repr__(self):
		return f"User({self.id},{self.email},{self.password})"
		
class Song(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(50),nullable=False)
	artist=db.Column(db.String(50),nullable=False)
	album=db.Column(db.String(50),nullable=False)
	file=db.Column(db.String(50),nullable=False)
	user_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
	
	def __repr__(self):
		return f"Song({self.id},{self.title},{self.artist},{self.album},{self.file},{self.user_id})"