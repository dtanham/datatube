from app import *
import hashlib

# Add test users
from app import User

def clean_env():
	db.drop_all()
	db.create_all()

def do_setup():
	clean_env()
	# s = b"asdflkjweofijfslkj"
	# hashed_pass = hashlib.sha256(s+b"password").hexdigest()

	# u = User(username="default", email="default@example.com", password_hash=hashed_pass, password_salt=s, role="admin")

	# db.session.add(u)
	# db.session.commit()

	u = add_user("default", "password", "default@example.com", role="admin")


	# Add test documents
	eid = hashlib.sha256(b"First test document").hexdigest()
	d = Document(author_id=u.id, title="First test document", external_id=eid, description="Our first document", body="<html><body><h1>First doc</h1></body></html>")

	db.session.add(d)
	db.session.commit()

if __name__ == "__main__":
	do_setup()

