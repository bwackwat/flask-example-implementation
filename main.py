import sys
import jwt

from functools import wraps
from flask import Flask, jsonify, request, json
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

app = Flask(__name__);
app.config.update(
	PROPAGATE_EXCEPTIONS = True,
	SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:aq12ws@localhost:5432/postgres"
)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

MYSECRET = "thisismyrealsecret"

from models import User, public_serialize

def protected(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		try:
			data = request.json
			token = data['token']
			tokendata = jwt.decode(token, MYSECRET, algorithms=["HS256"])

			print tokendata
			user = User.query.filter_by(username=tokendata['username']).first()
			if user == None:
				return jsonify(error="NO USER :O!")
			if user.password == tokendata['password']:
				return f(*args, **kwargs)
			else:
				return jsonify(error="Invalid password!")

		except KeyError as e:
			return jsonify(error=str(e) + " must be provided.")
		except IntegrityError as e:
			return jsonify(error=e.message)
		except Exception as e:
			return jsonify(error=repr(e) + "(Invalid JSON.)")
	return decorated_function

@app.route("/users", methods=["POST"])
@protected
def users():
	users = User.query.all()
	results = []
	for user in users:
		results.append(public_serialize(user))
	return jsonify(result=results)

@app.route("/signup", methods=["POST"])
def signup():
	try:
		data = request.json

		username = data['username']
		email = data['email']
		password = data['password']

		user = User(username, email, bcrypt.generate_password_hash(password))
		db.session.add(user)
		db.session.commit()

	except KeyError as e:
		return jsonify(error=str(e) + " must be provided.")
	except IntegrityError as e:
		return jsonify(error=e.message)
	except Exception as e:
		return jsonify(error=repr(e) + "(Invalid JSON.)")

	return jsonify(result=repr(user))

@app.route("/login", methods=["POST"])
def login():
	try:
		data = request.json

		username = data['username']
		password = data['password']

		user = User.query.filter_by(username=username).first()
		if user == None:
			return jsonify(error="Invalid username!")
		if bcrypt.check_password_hash(user.password, password):
			token = jwt.encode({"time": str(db.func.current_timestamp()), "username": user.username, "password": user.password}, MYSECRET, algorithm="HS256")
			return jsonify(result="Successful login! Your authentication token is: " + token)
		else:
			return jsonify(error="Invalid password!")

	except ValueError as e:
		return jsonify(error=str(e) + ": Password was stored improperly...")
	except KeyError as e:
		return jsonify(error=str(e) + " must be provided.")
	except IntegrityError as e:
		return jsonify(error=e.message)

app.run()