# DataTube - Publish your data

Lots of data analysis frameworks allow the publication of projects as flat HTML files.

DataTube lets you upload, version and present these to your users.

# Configuration
Set the ```SQLALCHEMY_DATABASE_URI``` environment variable with something that sqlalchemy can handle, for example:

```
SQLALCHEMY_DATABASE_URI="postgresql://<username:password>@<postgreshost>/<database-name>"

```

[![Build Status](https://travis-ci.org/dtanham/datatube.svg?branch=master)](https://travis-ci.org/dtanham/datatube)