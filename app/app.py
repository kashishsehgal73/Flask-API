from flask import Flask,request,jsonify,render_template
import requests, json
from urllib.parse import urlencode
from urllib.request import urlopen
from app import app
from app.forms import Search
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
base_url = "https://newsapi.org/v2/top-headlines?"
apikey = "eadb6da4bb5847a8b5f5b8a633e53ab9"


#Function to filter results according to keyword and change structure to our requirement
def filter_results(res, keyword, country, category):
	newdict = res.copy()
	newdict['articles'] = []
	count = 0
	print(newdict)
	for article in res['articles']:
		filtered_article = {}
		text =  article['content']
		if (text and keyword in text):
			filtered_article['Country'] = country
			filtered_article['Category'] = category
			filtered_article['Filter_keyword'] = keyword
			filtered_article['title'] = article['title']
			filtered_article['description'] = article['description']
			filtered_article['url'] = article['url']
			newdict['articles'].append(filtered_article)
			count = count + 1
		else:
			pass
	newdict['totalResults'] = count
	return newdict

#Simple test to get json response directly from request
@app.route('/test')
def test():
	mydict = {'country': None, 'category': None, 'apikey':apikey }
	country = request.args.get('country')
	category = request.args.get('category')
	mydict['country'] = country
	mydict['category'] = category
	url = base_url + urlencode(mydict)
	res = requests.get(url=url)
	return jsonify(res.json())

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
	mydict = {'country': None, 'category': None, 'apikey':apikey }
	country = request.form['country']
	category = request.form['category']
	keyword = request.form['keyword']
	mydict['country'] = country
	mydict['category'] = category

	#Generating url wrt search parameters
	url = base_url + urlencode(mydict)
	res = requests.get(url=url)
	data = json.loads(res.text)

	#Calling the filter_results function
	result = filter_results(data, keyword, country, category)
	return jsonify(json.loads(json.dumps(result)))

#Error handler for 404
@app.errorhandler(404)
def not_found_error(error):
    return (render_template('404.html'), 404)

#Error handler for 404
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return (render_template('500.html'), 500)
