# DataTube - Publish your data

Lots of data analysis frameworks allow the publication of projects as flat HTML files.

DataTube lets you upload, version and present these to your users.

# Installation and configuration
I'd always recommend running a python application inside a virtualenv: ```python3 -m venv venv && . venv/bin/activate```.

First install the dependencies with ```pip install -r requirements.txt```.

Then set the ```SQLALCHEMY_DATABASE_URI``` environment variable with something that sqlalchemy can handle.

Create tables in the database:

```
from app import db
db.create_all()
```

# Running

```
export SQLALCHEMY_DATABASE_URI="postgresql://<username:password>@<postgreshost>/<database-name>"
FLASK_DEBUG=1 FLASK_APP=app.py flask run

```

# Tests
Can I test it? Yes you can!

The core API and behaviour is well covered by tests, with some of the view layer to boot.

To see for yourself run ```pytest```.

Current build status show below:

[![Build Status](https://travis-ci.org/dtanham/datatube.svg?branch=master)](https://travis-ci.org/dtanham/datatube)

# Contribute
The best way to contribute is to [submit a feature request or bug](https://github.com/dtanham/datatube/issues/new). Even better if you then code up a fix and submit a pull request! :)

[![Waffle info](https://badge.waffle.io/dtanham/datatube.png?columns=all)](https://badge.waffle.io/dtanham/datatube.png?columns=all)
