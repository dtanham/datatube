import flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import logging, os, hashlib, random, string
from functools import wraps

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

    def compare_passwords(u, password):
    	if not u:
    		return False
    	if str(hashlib.sha256((str(u.password_salt)+str(password)).encode('utf-8')).hexdigest()) == str(u.password_hash):
    		return True
    	return False

class Document(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	external_id = db.Column(db.String(128), nullable=True)
	title = db.Column(db.String(80), nullable=False)
	description = db.Column(db.Text, nullable=True)
	pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	body = db.Column(db.Text, nullable=True)

# Authentication setup
app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_lowercase+string.digits) for i in range(16))


# Views
#######
def login_required(role):
	def wrap(f):
		@wraps(f)
		def wrapped_f(*args, **kwargs):
			if 'user' in flask.session:
				if flask.session['user']['role'] in role:
					logger.info("Attempt by user ["+flask.session['user']['username']+" with role ["+flask.session['user']['role']
							+"] to access function requiring ["+",".join(role)+"]")
					return f(*args, **kwargs)
				else:
					return "You do not have permission to do that", 403
			else:
				flask.flash("You must log in first")
				return flask.redirect(flask.url_for('basic_login', error="Please log in first."))
		return wrapped_f
	return wrap

@app.route("/")
def home():
	return flask.render_template("home.html", documents=get_all_documents())

# View raw document
@app.route("/dox/raw/<external_id>")
@login_required(['analyst','admin', 'viewer'])
def view_raw_document(external_id):
	d = get_document(external_id)
	if not d:
		flask.abort(404)
	return d.body

@app.route("/dox/viewer/<external_id>")
@login_required(['analyst','admin', 'viewer'])
def view_document(external_id):
	d = get_document(external_id)
	if not d:
		flask.abort(404)
	return flask.render_template("document_viewer.html", document=d)

@app.route("/dox/editor/<external_id>")
@login_required(['analyst','admin', 'viewer'])
def edit_document(external_id):
	return "Hi"

@app.route('/dox/raw/', methods=['POST'])
@login_required(['analyst','admin'])
def upload_file():
	f = flask.request.files['the_file']
	new_doc = add_document(file_handle=f, title=flask.request.form['title'], description=flask.request.form['description'])
	return flask.redirect(flask.url_for('view_document', external_id=new_doc.external_id))

# Authentication views

@app.route('/basic/login')
def basic_login():
	return flask.render_template("login.html", error=flask.request.args.get("error",""), message=flask.request.args.get("message",""))

@app.route('/basic/login', methods=['POST'])
def basic_login_submit():
	username = flask.request.form.get('username', 'default')
	password = flask.request.form.get('password', 'default')
	u = validate_user(username, password)

	if u:
		flask.session['user'] = {
			"username": u.username,
			"id": u.id,
			"role": u.role
		}
		return flask.redirect(flask.url_for('home', message="Success"))
	else:
		return flask.render_template("login.html", error="The username and password combination you provided is not valid.")

@app.route('/basic/logout')
def basic_logout():
	if flask.session.get('user', None):
		flask.session.pop("user")
	return flask.redirect(flask.url_for('basic_login', message="You have been logged out."))


@app.route('/admin')
@login_required(['admin'])
def administration():
	return flask.render_template("admin.html")

@login_required(['admin'])
@app.route('/admin/create-user', methods=['POST'])
def create_user():
	username = flask.request.form.get("username", "")
	password = flask.request.form.get("password", "")
	email = flask.request.form.get("email", "")
	role = flask.request.form.get("role", "")

	if username and password and email and role:
		u = add_user(
			flask.request.form.get("username"),
			flask.request.form.get("password"),
			flask.request.form.get("email"),
			flask.request.form.get("role")
		)
		if u:
			return flask.render_template("admin.html", message="User "+u.username+" created successfully!")
		else:
			return flask.render_template("admin.html", error="That user already exists", args=flask.request.form)
	errormsg = ""
	if not username:
		errormsg += "Username required<br/>"
	if not password:
		errormsg += "Password required<br/>"
	if not email:
		errormsg += "Email required<br/>"
	if not role:
		errormsg += "Role required<br/>"
	return flask.render_template("admin.html", error=errormsg, args=flask.request.args)

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

def add_user(username, password, email, role="default"):
	u = User()
	u.username = username
	u.email = email
	u.role = role

	if User.query.filter(User.username == username).first():
		return None
	if User.query.filter(User.email == email).first():
		return None

	u.password_salt = ''.join(random.choice(string.ascii_lowercase+string.digits) for i in range(16))
	sp = (u.password_salt+password).encode("utf-8")

	u.password_hash = hashlib.sha256(sp).hexdigest()
	db.session.add(u)
	db.session.commit()

	return u

def validate_user(username, password):
	u = User.query.filter(User.username == username).first()
	if User.compare_passwords(u, password):
		return u
	else:
		return None

