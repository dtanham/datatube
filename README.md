# DataTube - Publish your data

Lots of data analysis frameworks allow the publication of projects as flat HTML files.

DataTube lets you upload, version and present these to your users.

# Installation and configuration
I'd always recommend running a python application inside a virtualenv: ```python3 -m venv venv && . venv/bin/activate```.

First install the dependencies with ```pip install -r requirements.txt```.

Then set the ```SQLALCHEMY_DATABASE_URI``` environment variable with something that sqlalchemy can handle.

# Running

```
export SQLALCHEMY_DATABASE_URI="postgresql://<username:password>@<postgreshost>/<database-name>"
FLASK_DEBUG=1 FLASK_APP=app.py flask run

```

[![Build Status](https://travis-ci.org/dtanham/datatube.svg?branch=master)](https://travis-ci.org/dtanham/datatube)