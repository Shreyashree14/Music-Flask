# Music App-Flask

Music App is a platform to manage, share and stream music. User can register and login into the application to upload, download, delete, play and search songs. 

## Getting Started

### Technologies

```
Python 3.7.3
Flask 1.0.2
Sqlite 3.27.2
```

### Packages

```
flask
flask_login
flask_sqlalchemy
flask_bcrypt
wtforms
flask_wtf
flask_limiter
```

### Installation and Setup

To install the above packages use:
```
sudo pip install –r requirements.txt
```
Database file is already uploaded in the repo. To create your own db, navigate to app.py from the terminal and use the python interpreter:
```
from app import db
db.create_all()
```
A secret key is present in the config.py file. Create your own using the python interpreter and replace the existing secret key:
```
import os
print(os.urandom(16))
```


## Running the app

- Clone the repo to your local machine.
- Follow the install and setup instructions mentioned above.
- Go to the directory from terminal where app.py is cloned and use the command: flask run
- Go to http://127.0.0.1:5000/ in your local browser where the app is being run.

## Features

- Registration and Login
- Upload a song with metadata (album, artist, title)
- Delete an uploaded song
- View all songs
- Search songs using filters on the metadata
- Stream a song
- Download a song
- Share a song using its unique URL

## Security Features

- Authentication using Email and Password
- Strong password criteria (atleast 1 uppercase, lowercase, number & special character) 
- Storing hashed passwords in the database using Bcrypt
- Authorization using Flask-Login (@login_required)
- User session management using Flask-Login
- Use of SECRET_KEY in app configuration to protect sensitive user-data
- Use of Flask-Limiter to limit the number of requests on the pages
- Allowing only mp3 files to upload

## Future Enhancements

- Forgot password functionality with secure token-based email authentication using Flask_Mail
- Deploying app using HTTPS with SSL/TLS Certificate
- Implementing limited login attempts/captcha based login

