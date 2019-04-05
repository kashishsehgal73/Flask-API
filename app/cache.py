from urllib.parse import urlencode
import requests, json
from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()


base_url = "https://newsapi.org/v2/top-headlines?"
apikey = "eadb6da4bb5847a8b5f5b8a633e53ab9"
mydict = {'country': None, 'category': None, 'apikey':apikey }


#Function to fetch json from news api
def get_data(country, category):
	mydict['country'] = country
	mydict['category'] = category
	url = base_url + urlencode(mydict)
	res = requests.get(url=url)
	data = json.loads(res.text)
	return data



def get_cached_json(country, category):
	key = str(country) + str(category)
	cached_json = cache.get(key)
	if not cached_json:
		cached_json = get_data(country, category)
		cache.set(key, cached_json, timeout=10 * 60)
	return cached_json
