from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User (db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)
	
	def __init__(self, username, email):
		self.username = username
		self.email = email
		

class UserSchema (ma.Schema):
	class Meta:
		# Fields to expose
		fields = ('id', 'username', 'email')


userSchema = UserSchema()
usersSchema = UserSchema(many=True)


# endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user ():
	username = request.json["username"]
	email = request.json["email"]

	if db.session.query(User).filter_by(email=email).count() > 0:
		return jsonify({"message": "User already exists"})

	user = User(username, email)

	db.session.add(user)
	db.session.commit()

	return userSchema.jsonify(user)



# endpoint to show all users
@app.route("/user", methods=["GET"])
def getUsers ():
	users = User.query.all()
	return usersSchema.jsonify(users)


# endpoint to get user detail by id
@app.route("/user/<id>", methods=["GET"])
def getUser (id):
	user = User.query.get(id)
	return userSchema.jsonify(user)


# endpoint to update user
@app.route("/user/<id>", methods=["PUT"])
def updateUser (id):
	user = User.query.get(id)
	username = request.json['username']
	email= request.json['email']

	user.email = email
	user.username = username

	db.session.commit()
	return userSchema.jsonify(user)


# endpoint to delete user
@app.route("/user/<id>", methods=["DELETE"])
def deleteUser (id):
	user = User.query.get(id)
	db.session.delete(user)
	db.session.commit()

	return userSchema.jsonify(user)


if __name__ == '__main__':
	app.run(debug = True)
