import flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import logging
import os
import hashlib

logging.getLogger(__name__)
logger = logging.getLogger()
if os.environ.get("FLASK_DEBUG", "0") == "1":
	logger.setLevel(logging.DEBUG)
else:
	logger.setLevel(logging.INFO)

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///test_db.sqlite')

db = SQLAlchemy(app)


# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=False, nullable=False)
    password_salt = db.Column(db.String(128), unique=False, nullable=False)
    role = db.Column(db.String(128), unique=False, nullable=False, default="reader")

    def __repr__(self):
        return '<User %r>' % self.username

class Document(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	external_id = db.Column(db.String(128), nullable=True)
	title = db.Column(db.String(80), nullable=False)
	description = db.Column(db.Text, nullable=True)
	pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	body = db.Column(db.Text, nullable=True)

# class Tag(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	tag = db.Column(db.String(128), nullable=False, unique=True)


# Views
#######
@app.route("/")
def home():
	return flask.render_template("home.html", documents=get_all_documents())

# View raw document
@app.route("/dox/raw/<external_id>")
def view_raw_document(external_id):
	d = get_document(external_id)
	if not d:
		flask.abort(404)
	return d.body

@app.route("/dox/viewer/<external_id>")
def view_document(external_id):
	d = get_document(external_id)
	if not d:
		flask.abort(404)
	return flask.render_template("document_viewer.html", document=d)

@app.route("/dox/editor/<external_id>")
def edit_document(external_id):
	return "Hi"

@app.route('/dox/raw/', methods=['POST'])
def upload_file():
	f = flask.request.files['the_file']
	new_doc = add_document(file_handle=f, title=flask.request.form['title'], description=flask.request.form['description'])
	return flask.redirect(flask.url_for('view_document', external_id=new_doc.external_id))


# Controllers
#############
def get_all_documents():
	return Document.query.all()

def get_document(external_id):
	d = Document.query.filter_by(external_id=external_id).first()
	if not d:
		logger.info("No document found for: "+external_id)
	return d

def add_document(**kwargs):
	d = Document()

	d.title = kwargs['title']
	d.description = kwargs['description']

	file_handle = kwargs['file_handle']
	d.body = file_handle.read().decode('utf-8')

	d.external_id = hashlib.sha256(d.title.encode('utf-8')).hexdigest()

	d.author_id = 1

	db.session.add(d)
	db.session.commit()

	return d

