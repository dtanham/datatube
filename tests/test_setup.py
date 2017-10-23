from reset_environment import *
from app import *


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
		d = add_document(file_handle=f, title="Test title", description="Small description")

	assert len(get_all_documents()) == 2
	Document.query.filter(Document.id==d.id).delete()

def test_user_creation_and_authentication():
	u = add_user("testuser", "password123", "test@example.com")
	print(u)

	u1 = User.query.filter(User.username == "testuser").first()
	assert u.id == u1.id

	u2 = validate_user("testuser", "password123")
	assert u.id == u2.id

def test_session_login():
	c = app.test_client()
	r = c.post('/basic/login', data=dict(
        username="default",
        password="password"
    ), follow_redirects=True)
	assert "Logged in as" in str(r.data)

def test_session_logout():
	c = app.test_client()
	r = c.get('/basic/logout', follow_redirects=True)
	assert "You have been logged out" in str(r.data)