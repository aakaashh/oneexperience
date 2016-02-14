import webapp2
import jinja2
import logging
from google.appengine.ext import ndb
from models import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class LandingPage(webapp2.RequestHandler):
	def get(self):
		template= JINJA_ENVIRONMENT.get_template('landing.html')
		self.response.write(template.render())

