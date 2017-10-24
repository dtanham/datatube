from reset_environment import *
from app import *

import tempfile, os


do_setup()

def test_setup():
    assert len(User.query.all()) == 1
    assert len(Document.query.all()) == 1

def test_document_retrieval():
	assert len(get_all_documents()) == 1

def test_add_document():
	u = User.query.first()
	assert u.id == 1
	with open("tests/testdata/test_file_1.html", "rb") as f:
		d = add_document(file_handle=f, title="Test title", description="Small description", author={"id":u.id})

	assert len(get_all_documents()) == 2
	Document.query.filter(Document.id==d.id).delete()

def test_user_creation_and_authentication():
	u = add_user("testuser", "password123", "test@example.com")
	print(u)

	u1 = User.query.filter(User.username == "testuser").first()
	assert u.id == u1.id

	u2 = validate_user("testuser", "password123")
	assert u.id == u2.id

def test_good_login():
	c = app.test_client()
	r = c.post('/basic/login', data=dict(
        username="default",
        password="password"
    ), follow_redirects=True)
	assert "Logged in as" in str(r.data)

def test_bad_login():
	c = app.test_client()
	r = c.post('/basic/login', data=dict(
        username="default",
        password="baspassword"
    ), follow_redirects=True)
	assert "The username and password combination you provided is not valid." in str(r.data)

def test_session_logout():
	c = app.test_client()
	r = c.get('/basic/logout', follow_redirects=True)
	assert "You have been logged out" in str(r.data)

def test_admin_role_restriction():
	c = app.test_client()
	r = c.get('/admin', follow_redirects=True)
	assert "Admin" not in str(r.data)

def test_document_version_increment():
	# Given that there is an existing document
	d_initial = Document.query.first()
	d_latest = Document.query.filter(Document.external_id==d_initial.external_id).order_by(Document.version.desc()).first()

	# When a new document is uploaded to it
	f = tempfile.NamedTemporaryFile(delete=False)
	f.write(b"<h1>Some new file content</h1>")
	f.seek(0)
	d_new = update_document(external_id=d_latest.external_id, file_handle=f, description=d_latest.description+" changed")
	f.close()
	os.unlink(f.name)

	# Then the document version should increment
	assert d_new.version > d_latest.version

