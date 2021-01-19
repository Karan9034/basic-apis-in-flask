from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I-wont-tell-you'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(80), nullable=False)
	name = db.Column(db.String(50), nullable=False)

@app.route('/api/users', methods=['GET', 'POST'])
def all():
	if request.method == 'GET':
		email = request.args.get('email')
		name = request.args.get('name')
		usr = []
		if email:
			users = Users.query.filter_by(email=email).all()
			for user in users:
				usr.append({'id':user.id, 'email':user.email, 'name':user.name})
		elif name:
			users = Users.query.filter_by(name=name).all()
			for user in users:
				usr.append({'id':user.id, 'email':user.email, 'name':user.name})
		else:
			users = Users.query.all()
			for user in users:
				usr.append({'id':user.id, 'email':user.email, 'name':user.name})
		return jsonify(usr)
	if request.method == 'POST':
		data = request.get_json()
		user = Users(email=data['email'], name=data['name'])
		db.session.add(user)
		db.session.commit()
		return jsonify({ 'msg': 'User Updated!'})


# @app.route('/api/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# def api(id):
# 	pass

if __name__ == '__main__':
	app.run(debug=True, port=8000)