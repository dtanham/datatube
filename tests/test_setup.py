from reset_env import *
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

