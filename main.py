
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import util
from views import *
import logging

# Aquí se define la aplicación web. Básicamente consistene en una asociación
# url / vista. Por ejemplo, ('/profile', ProfileView) dice que la vista
# ProfileView se muestra cuando accedemos a http://misitio.com/profile .
def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([
        ('/',     IndexView),
        ('/profile', ProfileView),
        ('/profile/alerts', ProfileAlertsView),
        ('/profile/copies', ProfileCopiesView),
        ('/profile/historial', ProfileHistorialView),
        ('/profile/newcopy', ProfileNewCopyView),
        ('/profile/offers', ProfileOffersView),
        ('/profile/applications', ProfileApplicationsView),
        ('/profile/copyoffers', CopyOffersView),
        ('/profile/appliantcopies', AppliantCopiesView)
        ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

