from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I-wont-tell-you'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Members(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(80), nullable=False)
	name = db.Column(db.String(50), nullable=False)

class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(80), nullable=False)
	name = db.Column(db.String(50), nullable=False)
	password = db.Column(db.String(50), nullable=False)

@app.route('/api/members', methods=['GET', 'POST'])
def all():
	if request.method == 'GET':
		email = request.args.get('email')
		name = request.args.get('name')
		mmb = []
		if email:
			members = Members.query.filter_by(email=email).all()
			for member in members:
				mmb.append({'id':member.id, 'email':member.email, 'name':member.name})
		elif name:
			members = Members.query.filter_by(name=name).all()
			for member in members:
				mmb.append({'id':member.id, 'email':member.email, 'name':member.name})
		else:
			members = Members.query.all()
			for member in members:
				mmb.append({'id':member.id, 'email':member.email, 'name':member.name})
		return jsonify(mmb)
	if request.method == 'POST':
		data = request.get_json()
		member = members(email=data['email'], name=data['name'])
		db.session.add(member)
		db.session.commit()
		return jsonify({ 'msg': 'Member Added!'})


@app.route('/api/members/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def api(id):
	if request.method == 'GET':
		mmb = {}
		member = Members.query.filter_by(id=id).first()
		if member:
			mmb['id'] = member.id
			mmb['email'] = member.email
			mmb['name'] = member.name
		else:
			mmb['msg'] = 'No member with id of'+str(id)
		return jsonify(mmb)

	if request.method == 'PUT':
		member = Members.query.filter_by(id=id).first()
		data = request.get_json()
		if data['email']:
			member.email = data['email']
		if data['name']:
			member.name = data['name']
		db.session.commit()
		return jsonify({'msg': 'Member Updated!'})

	if request.method == 'DELETE':
		member = Members.query.filter_by(id=id).first()
		db.session.delete(member)
		db.session.commit()
		return jsonify({'msg': 'Member Deleted!'})


@app.route('/login', methods=['POST'])
def login():
	data = request.get_json()
	email = data['email'] if 'email' in data else ''
	password = data['password'] if 'password' in data else ''
	if email and password:
		user = Users.query.filter_by(email=email).first()
		if user and bcrypt.check_password_hash(user.password, password):
			return jsonify({'msg':'User Logged In'})
		return jsonify({'msg': 'Incorrect email and password'})
	return jsonify({'msg': 'Enter email and password'})


@app.route('/register', methods=['POST'])
def register():
	data = request.get_json()
	email = data['email'] if 'email' in data else ''
	name = data['name'] if 'name' in data else ''
	password = data['password'] if 'password' in data else ''
	if email and name and password:
		hash_pw = bcrypt.generate_password_hash(password)
		user = Users(email=email, name=name, password=hash_pw)
		db.session.add(user)
		db.session.commit()
		return jsonify({'msg': 'User Registered!'})
	return jsonify({'msg':'Enter name, email and password'})

if __name__ == '__main__':
	app.run(debug=True, port=8000)