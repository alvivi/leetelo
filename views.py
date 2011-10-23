# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template
from models import *

class UsersView(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            logout = users.create_logout_url('/')
            return self.get_with_user(user, logout)
        else:
            return self.get_without_user()

    def get_with_user(self, user, logoutUri):
        pass

    def get_without_user(self):
        self.redirect('/')


class UserView(UsersView):
    def get_with_user(self, user, logoutUri):
        copies = Copy.all().filter('user =', user).fetch(64)
        values = {
            'copies'     : copies,
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/')
        }

        self.response.out.write(template.render('html/user.html', values))


class IndexView(UsersView):
    def get_with_user(self, user, logoutUri):
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/')
        }
        self.response.out.write(template.render('html/index.html', values))

    def get_without_user(self):
        values = {
            'loginUri'   : users.create_login_url(self.request.uri),
            'newUserUri' : 'http://accounts.google.com'
        }
        self.response.out.write(template.render('html/index.html', values))
