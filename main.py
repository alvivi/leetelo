
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
        ('/book/details/comment/new', BookCommentNew),
        ('/book/details/comment/delete', BookCommentDelete),
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
        ('/profile/club/comment/new', ProfileClubCommentNew),
        ('/profile/club/comment/delete', ProfileClubCommentDelete),
        ('/profile/club/content', ProfileClubContentView),
        ('/profile/club/deleteparticipation', ProfileDeleteParticipationView),
        ('/profile/club/disable', ProfileDisableClubsView),
        ('/profile/club/disabledcontent', ProfileDisabledClubContentView),
        ('/profile/club/edit', ProfileEditClubView),
        ('/profile/club/new', ProfileNewClubView),
        ('/profile/club/view', ProfileDataClubView),
        ('/profile/copies', ProfileCopiesView),
        ('/profile/copies/delete', ProfileDeleteCopiesView),
        ('/profile/copyoffers', ProfileCopyOffersView),
        ('/profile/datacopy', ProfileDataCopyView),
        ('/profile/editcopy', ProfileEditCopyView),
        ('/profile/historial', ProfileHistorialView),
        ('/profile/transaction', TransactionView),
        ('/profile/newcopy', ProfileNewCopyView),
        ('/profile/offers', ProfileOffersView),
        ('/search', SearchView),
        ('/user/details', UserDetailsView),
        ('/user/details/comment/new', UserCommentNew),
        ('/user/details/comment/delete', UserCommentDelete)
        ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

