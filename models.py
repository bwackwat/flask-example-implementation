from sqlalchemy.exc import SQLAlchemyError
from geoalchemy2 import Geometry
from main import db

def public_serialize(obj):
	dict = {}
	for public_key in obj.__public__:
		value = getattr(obj, public_key)
		if value:
			dict[public_key] = value
	return dict

class User(db.Model):
	__tablename__ = "user"
	__public__ = ["id", "username", "email", "created_on"]

	id = db.Column(db.Integer, primary_key=True, unique=True)
	username = db.Column(db.String(255), index=True, unique=True)
	email = db.Column(db.String(255), index=True, unique=True)
	password = db.Column(db.String(255))
	token = db.Column(db.String(255))
	created_on = db.Column(db.TIMESTAMP, server_default = db.func.current_timestamp())

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = password

	#For printing purposes
	def __repr__(self):
		return str(public_serialize(self))

class Poi(db.Model):
	__tablename__ = "poi"

	id = db.Column(db.Integer, primary_key=True, unique=True)
	label = db.Column(db.String(255))
	description = db.Column(db.String(255))
	location = db.Column(Geometry("POINT"), unique=True)
	created_on = db.Column(db.TIMESTAMP, server_default = db.func.current_timestamp())

	def __init__(self, label, description, location):
		self.label = label
		self.description = description
		self.location = location

	#For printing purposes
	def __repr__(self):
		return str(public_serialize(self))

db.create_all()