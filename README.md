# DataTube - Publish your data

Lots of data analysis frameworks allow the publication of projects as flat HTML files.

DataTube lets you upload, version and present these to your users.

# Configuration
Create a ```dev_env.py``` file or similar with at least the following contents:

```
SQLALCHEMY_DATABASE_URI = "postgresql://<username:password>@<postgreshost>/<database-name>"

```

<img src="https://travis-ci.org/dtanham/datatube.svg?branch=master" alt="Travis build status">