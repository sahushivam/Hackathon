from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home/')
def home():
	return render_template('home.html');

@app.route('/about/')
def about():
	return render_template('about.html');

@app.route('/service/')
def service():
	return render_template('service.html');

@app.route('/contact/')
def contact():
	return render_template('contact.html');
