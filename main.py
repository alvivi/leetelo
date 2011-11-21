
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
        ('/book/new', BookNewView),
        ('/book/details', BookDetailsView),
        ('/search', SearchView),
        ('/profile', ProfileView),
        ('/profile/alerts', ProfileAlertsView),
        ('/profile/copies', ProfileCopiesView),
        ('/profile/copies/delete', ProfileDeleteCopiesView),
        ('/profile/historial', ProfileHistorialView),
        ('/profile/newcopy', ProfileNewCopyView),
        ('/profile/editcopy', ProfileEditCopyView),
        ('/profile/datacopy', ProfileDataCopyView),
        ('/profile/offers', ProfileOffersView),
        ('/profile/applications', ProfileApplicationsView),
        ('/profile/applications/new', ProfileApplicationsNewView),
        ('/profile/copyoffers', CopyOffersView),
        ('/profile/appliantcopies', AppliantCopiesView),
        ('/profile/sale', SaleView),
        ('/profile/loan', LoanView),
        ('/profile/exchange', ExchangeView),
        ('/profile/applicationcontent', ApplicationContentView),
        ('/profile/account',ProfileAccountView),
        ('/profile/newclub', ProfileNewClubView),
        ('/profile/editclub', ProfileEditClubView),
        ('/img',Image)
        ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

