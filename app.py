import os
from flask import Flask, render_template, abort, url_for, json, jsonify, request, redirect,make_response
import jwt 
from datetime import datetime, timedelta 
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker


app = Flask(__name__,template_folder='./templates')

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class User(db.Model):
	__tablename__ = 'User'
	name = db.Column(db.Text, primary_key=True)  
	password = db.Column(db.Text)  


@app.route('/')
def testdb():
	access_token = request.cookies.get('access_token')
	if (access_token):
		try:
			user = User.query.filter_by(name = 'Pan Yong').first() 
			return '<h1>It works.</h1>'+ user.name+" password:"+ user.password
		except Exception as e:
			error_text = "<p>The error:<br>" + str(e) + "</p>"
			hed = '<h1>Something is broken.</h1>'
			return hed + error_text
	return render_template('login.html',error='Please login')


app.config['SECRET_KEY'] = 'mysup3pa3rultraSeeCakeK3y!'

@app.route('/login', methods=['GET', 'POST'])
def login(): 
	error = None
	if request.method == 'POST' and request.form['username'] != '' and request.form['password'] != '':
		user = User.query.filter_by(name = request.form['username']).first() 		
		if user.password == request.form['password']:
			token = jwt.encode({ 'username': user.name, 'exp' : datetime.utcnow() + timedelta(minutes = 30) }, app.config['SECRET_KEY'])
			response = make_response(redirect('/verified'))
			response.set_cookie('access_token', token)
			return response
		else:
			return render_template('login.html',error='Could not verify')
	return render_template('login.html', error=error)

@app.route('/verified', methods=['GET', 'POST'])
def verified():	
	access_token = request.cookies.get('access_token')
	if (access_token):	
		return render_template('index.html')
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')



