import json
from app.cache import get_cached_json

#Function to filter results according to keyword and change structure to our requirement
def filter_results(data, keyword, country, category):
	newdict = data.copy()
	newdict['articles'] = []
	count = 0
	for article in data['articles']:
		filtered_article = {}
		text =  article['content']
		if (text and any(key in text for key in keyword.split())):
			filtered_article['Country'] = country
			filtered_article['Category'] = category
			filtered_article['Filter_keyword'] = keyword
			filtered_article['title'] = article['title']
			filtered_article['description'] = article['description']
			filtered_article['content'] = article['content']
			filtered_article['url'] = article['url']
			newdict['articles'].append(filtered_article)
			count = count + 1
		newdict['totalResults'] = count
	return json.loads(json.dumps(newdict))
