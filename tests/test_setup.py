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