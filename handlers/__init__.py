import webapp2
from trial import *

app = webapp2.WSGIApplication([
	('/', LandingPage),
], debug=True)
