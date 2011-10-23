
# -*- coding: utf-8 -*-


from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import util
from views import *


def main():
    application = webapp.WSGIApplication([
        ('/',     IndexView),
        ('/user', UserView)
        ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

