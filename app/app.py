from flask import Flask,request,jsonify,render_template
import requests, json, os
from urllib.request import urlopen
from app import app
from app.forms import Search
from app.config import Config
from app.processing import  filter_results
from app.cache import get_data,get_cached_json

app = Flask(__name__)
app.config.from_object(Config)


#Simple test to get json response directly from request
@app.route('/test')
def test():
	country = request.args.get('country')
	category = request.args.get('category')
	keyword = request.args.get('filter')
	if(not(category and country)):
		return render_template('bad_parameters.html', title='Error')
	data = get_cached_json(country, category)
	if(keyword):
		data = filter_results(data, keyword, country, category)
	return jsonify(data)

#Home Page
@app.route('/')
def home():
	return render_template('index.html', title='Home')


#Search Form
@app.route('/search')
def search():
	form = Search()
	return render_template('form.html', title='Search', form=form)


#Receive search parameters and return json
@app.route('/search_data', methods=['POST'])
def search_data():
	country, category, keyword = request.form['country'], request.form['category'], request.form['keyword']

	data = get_cached_json(country, category)

	#data = filter_results(data, keyword, country, category)

	return jsonify(data)


#Error handler for 404
@app.errorhandler(404)
def not_found_error(error):
    return (render_template('404.html'), 404)

#Error handler for 404
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return (render_template('500.html'), 500)
