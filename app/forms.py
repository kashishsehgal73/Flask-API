from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField, TextField
from wtforms.validators import DataRequired, Required

class Search(FlaskForm):
	country = SelectField('Country', choices = [('us', 'USA'), ('in', 'India'), ('ch', 'China'), ('au', 'Australia'), ('ar', 'Argentina'), ('ch', 'China'), ('ca', 'Canada')])
	category = SelectField('Category',choices = [('business', 'Business'), ('entertainment', 'Entertainment'), ('health', 'Health'), ('technology', 'Technology')] )
	keyword = TextField("Keyword",[Required("Please enter the keyword to search for.")])
	submit = SubmitField('Search')
