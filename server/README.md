# WIP-server

## Description
Django, RESTful server to support the gists metadata.

## Install
In the directory/ [virtual machine](https://virtualenvwrapper.readthedocs.io/en/latest/)

* Create the local_setting
```python
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
GITHUB_APP_ID = 'XXXXXXXXXXXXXXXXXXX'
GITHUB_API_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SITE_ID = 1

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static")
```

* Create a virtual env (optional)

        mkvirtualenv gistx-env
        
        workon gistx-env

* Install 

		install.cmd
    
* Or    
	* Install requirements

			install pip3
	        pip3 install -r requirements.txt


    
	* Create DB

	        python manage.py migrate
		
	* Install server

	        python manage.py install

	* Run server

	        python manage.py runserver

		
## routes
### get
- [x]  `/api/gists/?category=hot&page=2` Shows the public gists hot data from github.
- [x]  `category=fresh` Shows the public gists fresh data from github.
- [x]  `category=trending` Shows the public gists trending data from github.
- [x]  `/accounts/github/login` With the github client-id the server will identify the user.
- [ ]  `/user/gist/comments` Shows the public gist comments from github.
- [ ]  `/user/gist/likes` Shows the public gist likes from github/server.
- [ ]  `/user/<client-id>/<gist-id>/?` Post a comment.
- [ ]  `/user/gists` Shows the User public gist.
- [ ]  `/user/<gist-id>/comments` Shows the user gist comments from github.
- [ ]  `/user/<gist-id>/likes` Shows the user gist likes.

