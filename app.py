from flask import Flask,request,redirect,url_for,render_template,session,jsonify
from database import UserDb
import re

app = Flask(__name__)
db = UserDb(app)

@app.route('/' , methods=['GET','POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		account = db.get_account(username, password)
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			return redirect(url_for('home'))
		else:
			msg = 'invalid username and password!'
			return jsonify({'message':msg})
	return render_template('index.html')

@app.route('/register',methods = ['POST'])
def register():
	msg = ''
	data = request.get_json()
	username = data['username']
	password = data['password']
	email = data['email']
	account = db.get_registered(username)
	if account:
		msg = 'Account already exists!'
		return jsonify({'message':msg})
	elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
		msg = 'Invalid email address!'
		return jsonify({'message':msg})
	elif not re.match(r'[A-Za-z0-9]+', username):
		msg = 'Username must contain only characters and numbers!'
		return jsonify({'message':msg})
	elif not username or not password or not email:
		msg = 'Please fill out the form!'
		return jsonify({'message':msg})
	else:
		db.get_register(username, password, email)
		msg = 'You have successfully registered!'
		return jsonify({'message':msg})
	if request.method == 'POST':
		msg = 'please fill the form'
		return jsonify({'message':msg})
	return render_template('register.html')

@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'loggedin' in session:
    	s = session['id']
    	account = db.get_profile(s)
    	return render_template('profile.html', account=account)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
	#remove session data
	session.pop('loggedin',None)
	session.pop('id',None)
	session.pop('username',None)
	#loginpage
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug = True)
