
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
        ('/', IndexView),
        ('/api/books/title', BooksByTitleRequest),
        ('/book/details', BookDetailsView),
        ('/book/new', BookNewView),
        ('/club', clubView),
        ('/club/requestparticipation', ClubRequestParticipationView),
        ('/img',Image),
        ('/profile', ProfileView),
        ('/profile/account',ProfileAccountView),
        ('/profile/alerts', ProfileAlertsView),
        ('/profile/appliantcopies', AppliantCopiesView),
        ('/profile/applicationcontent', ApplicationContentView),
        ('/profile/applications', ProfileApplicationsView),
        ('/profile/applications/new', ProfileApplicationsNewView),
        ('/profile/club', ProfileClubListView),
        ('/profile/club/answerinvitation', ProfileAnswerInvitationView),
        ('/profile/club/answerrequest', ProfileAnswerRequestView),
        ('/profile/club/content', ProfileClubContentView),
        ('/profile/club/deleteparticipation', ProfileDeleteParticipationView),
        ('/profile/club/disable', ProfileDisableClubsView),
        ('/profile/club/disabledcontent', ProfileDisabledClubContentView),
        ('/profile/club/edit', ProfileEditClubView),
        ('/profile/club/new', ProfileNewClubView),
        ('/profile/club/view', ProfileDataClubView),
        ('/profile/copies', ProfileCopiesView),
        ('/profile/copies/delete', ProfileDeleteCopiesView),
        ('/profile/copyoffers', CopyOffersView),
        ('/profile/datacopy', ProfileDataCopyView),
        ('/profile/editcopy', ProfileEditCopyView),
        ('/profile/exchange', ExchangeView),
        ('/profile/historial', ProfileHistorialView),
        ('/profile/loan', LoanView),
        ('/profile/newcopy', ProfileNewCopyView),
        ('/profile/offers', ProfileOffersView),
        ('/profile/sale', SaleView),
        ('/search', SearchView)
        ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

