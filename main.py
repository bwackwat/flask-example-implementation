import sys
import jwt

from functools import wraps
from flask import Flask, jsonify, request, json, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

app = Flask(__name__);
app.config.update(
	PROPAGATE_EXCEPTIONS = True,
	SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:aq12ws@localhost:5432/postgres",
	SQLALCHEMY_TRACK_MODIFICATIONS = True
)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

MYSECRET = "thisismyrealsecret"

from models import User, Poi, public_serialize

@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
	return response

def exceptor(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		print request.json

		try:
			return f(*args, **kwargs)
		except jwt.DecodeError as e:
			return jsonify(error=str(e) + ": Invalid token! Go login again...")
		except ValueError as e:
			return jsonify(error=str(e) + ": Password was stored improperly...")
		except KeyError as e:
			return jsonify(error=str(e) + " must be provided.")
		except IntegrityError as e:
			return jsonify(error=e.message)
		#except Exception as e:
		#	return jsonify(error=repr(e) + "(Invalid JSON?)")
	return decorated

def protected(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		data = request.json
		token = data['token']
		request.tokendata = jwt.decode(token, MYSECRET, algorithms=["HS256"])

		user = User.query.filter_by(id=request.tokendata['id']).first()
		if user == None:
			return jsonify(error="Invalid username! Are you tring to forge a token?")
		if user.password == request.tokendata['password']:
			return f(*args, **kwargs)
		else:
			return jsonify(error="Invalid password! Are you tring to forge a token?")
	return decorated

apiPrefix = "/api";

@app.route(apiPrefix + "/users", methods=["POST"])
@exceptor
@protected
def users():
	users = User.query.all()
	results = []
	for user in users:
		results.append(public_serialize(user))
	return jsonify(result=results)

@app.route(apiPrefix + "/poi/new", methods=["POST"])
@exceptor
@protected
def newpoi():
	data = request.json

	owner_id = request.tokendata['id']
	label = data['label']
	description = data['description']
	location = data['location']

	poi = Poi(owner_id, label, description, location)
	db.session.add(poi)
	db.session.commit()

	return jsonify(result=repr(poi))

@app.route(apiPrefix + "/poi/all", methods=["POST"])
@exceptor
@protected
def allpois():
	data = request.json

	owner_id = request.tokendata['id']

	pois = Poi.query.filter_by(owner_id=request.tokendata['id'])
	results = []
	for poi in pois:
		results.append(public_serialize(poi))
	return jsonify(result=results)

@app.route(apiPrefix + "/signup", methods=["POST"])
@exceptor
def signup():
	data = request.json

	username = data['username']
	email = data['email']
	password = data['password']

	user = User(username, email, bcrypt.generate_password_hash(password))
	db.session.add(user)
	db.session.commit()

	return jsonify(result=repr(user))

@app.route(apiPrefix + "/login", methods=["POST"])
@exceptor
def login():
	data = request.json

	username = data['username']
	password = data['password']

	user = User.query.filter_by(username=username).first()
	if user == None:
		return jsonify(error="Invalid username!")
	if bcrypt.check_password_hash(user.password, password):
		token = jwt.encode({"time": str(db.func.current_timestamp()), "id": user.id, "password": user.password}, MYSECRET, algorithm="HS256")
		return jsonify(result="Successful login!", token=token)
	else:
		return jsonify(error="Invalid password!")

app.run()