from sqlalchemy.exc import SQLAlchemyError
from geoalchemy2 import Geometry
import geoalchemy2.functions as GeoFunctions
from main import db, json

def public_serialize(obj):
	dict = {}
	for public_key in obj.__public__:
		value = getattr(obj, public_key)
		if value:
			dict[public_key] = value
	for geo_key in obj.__geo__:
		value = getattr(obj, geo_key)
		geodata = json.loads(db.session.scalar(GeoFunctions.ST_AsGeoJSON(value)))
		if geodata['type'] == "Point":
			geopoint = geodata['coordinates']
			dict[geo_key] = {"longitude":geopoint[0], "latitude":geopoint[1]}
	return dict

class User(db.Model):
	__tablename__ = "user"
	__public__ = ["id", "username", "email", "created_on"]
	__geo__ = []

	id = db.Column(db.Integer, primary_key=True, unique=True)
	username = db.Column(db.String(255), index=True, unique=True)
	email = db.Column(db.String(255), index=True, unique=True)
	password = db.Column(db.String(255))
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
	__public__ = ["id", "owner_id", "label", "description", "created_on"]
	__geo__ = ["location"]

	id = db.Column(db.Integer, primary_key=True, unique=True)
	owner_id = db.Column(db.Integer)
	label = db.Column(db.String(255))
	description = db.Column(db.String(255))
	location = db.Column(Geometry("POINT"), unique=True)
	created_on = db.Column(db.TIMESTAMP, server_default = db.func.current_timestamp())

	def __init__(self, owner_id, label, description, location):
		self.owner_id = owner_id
		self.label = label
		self.description = description
		self.location = "POINT(%s %s)" % (location['longitude'], location['latitude'])

	#For printing purposes
	def __repr__(self):
		return str(public_serialize(self))

#Run once; upon postgresql installation.
#db.engine.execute("create extension postgis")

#user is a postgres reserved word, QUOTE IT!
#db.engine.execute('drop table "user"')

#db.engine.execute('drop table poi')

db.create_all()