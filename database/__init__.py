from flask_mysqldb import MySQL
import os

class UserDb():
	def __init__(self, app):
		key = os.urandom(24) #random number
		key = str(key)
		app.secret_key = key
		#database connection
		app.config['MYSQL_HOST'] = 'localhost' 
		app.config['MYSQL_USER'] = 'root'	   
		app.config['MYSQL_PASSWORD'] = '12345' 
		app.config['MYSQL_DB'] = 'pythonlogin' 
		app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  
		self.app = app
		self.mysql = MySQL(self.app)
	def get_account(self, username, password):
		cursor = self.mysql.connection.cursor()
		cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s',(username,password))
		return cursor.fetchone()
	def get_registered(self,username):
		cursor = self.mysql.connection.cursor()
		cursor.execute('SELECT * FROM accounts WHERE username = %s', [username])
		return cursor.fetchone()
	def get_register(self,username, password, email):
		cursor = self.mysql.connection.cursor()
		cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', [username, password, email])
		return self.mysql.connection.commit()
	def get_profile(self,s):
		cursor =self.mysql.connection.cursor()
		cursor.execute('SELECT * FROM accounts WHERE id = %s', [s])
		return cursor.fetchone()