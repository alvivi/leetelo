# -*- coding: utf-8 -*-

# En este fichero se definen las vistas de la aplicación web. Las vistas se
# encargar de recoger los datos que sean necesarios, utilzar los modelos y
# luego devolver algo al usurio (normalemente una página HTML).

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template
from models import *


# Clase que ayuda a la hora de crear vistas que requieran un usuario. Las
# clases que hereden de ella deben implementar get_as_user (si requiren de un
# usuario registrado) o get_as_anom (si no lo requieren) en lugar de
# implementar el método get.
# Nota: por defecto get_as_* redirige a la página principal.
class UserView(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            logout = users.create_logout_url('/')
            return self.get_as_user(user, logout)
        else:
            return self.get_as_anom()

    def get_as_user(self, user, logoutUri):
        self.redirect('/')

    def get_as_anom(self):
        self.redirect('/')


# Pérfil de usuario.
class ProfileView(UserView):
    def get_as_user(self, user, logoutUri):
        values = {
            'copies'     : Copy.allCopiesOf(user),
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/')
        }
        self.response.out.write(template.render('html/profile.html', values))


# Página principal.
class IndexView(UserView):
    def get_as_user(self, user, logoutUri):
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/')
        }
        self.response.out.write(template.render('html/index.html', values))

    def get_as_anom(self):
        values = {
            'loginUri'   : users.create_login_url(self.request.uri),
            'newUserUri' : 'http://accounts.google.com'
        }
        self.response.out.write(template.render('html/index.html', values))

