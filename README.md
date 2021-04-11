# Shajbari
  Full Functional Web application


# Live Server
  http://mdiqbal00.pythonanywhere.com/
 
 
# User manual
  https://drive.google.com/file/d/1OjfvINKcW6uxO-mw9iX7V85dpkPE3FjD/view?usp=sharing

# Getting Started

Clone the repository with 
$ git clone https://www/github.com/Md-Iqbal/ShajBari.git

Unzip the file and go to the directory.

Open terminal and go through these command line below.

$ virtualenv project-env
$ source project-env/bin/activate
$ pip install -r https://raw.githubusercontent.com/juanifioren/django-project-template/master/requirements.txt

# You may want to change the name `projectname`.
$ django-admin startproject --template https://github.com/juanifioren/django-project-template/archive/master.zip projectname

$ cd projectname/
$ cp settings_custom.py.edit settings_custom.py
$ python manage.py migrate
$ python manage.py runserver
Features

Basic Django scaffolding (commands, templatetags, statics, media files, etc).
Split settings in two files. settings_custom.py for specific environment settings (localhost, production, etc). projectname/settings.py for core settings.
Simple logging setup ready for production envs.
Contributing

I love contributions, so please feel free to fix bugs, improve things, provide documentation. Just send a pull request.
