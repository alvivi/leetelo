
# -*- coding: utf-8 -*-

# En este fichero se definen las vistas de la aplicación web. Las vistas se
# encargar de recoger los datos que sean necesarios, utilzar los modelos y
# luego devolver algo al usurio (normalemente una página HTML).

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template
from models import *
import logging


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

    def post(self):
        user = users.get_current_user()
        if user:
            logout = users.create_logout_url('/')
            return self.post_as_user(user, logout)
        else :
            return selt.post_as_anom()

    def post_as_user(self, user, logoutUri):
        self.redirect('/')

    def post_as_anom(self):
        self.redirect('/')


# Pérfil de usuario. Vista compartida entre todas las subsecciones del perfil
# de usuario.
class ProfileView(UserView):
    def get_as_user(self, user, logoutUri):
        self.redirect('/profile/alerts')


class ProfileAlertsView(UserView):
    def get_as_user(self, user, logoutUri):
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/')
        }
        self.response.out.write(template.render('html/profileAlerts.html', values))

class ProfileCopiesView(UserView):
    def get_as_user(self, user, logoutUri):
        values = {
            'copies'     : Copy.allCopiesOf(user),
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/')
        }
        self.response.out.write(template.render('html/profileCopies.html', values))

class ProfileNewCopyView(UserView):
    def get_as_user(self, user, logoutUri):
        title = self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =',title).get()
        values = {
            'books'      : Book.all(),
            'book'       : book,
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
        }
        self.response.out.write(template.render('html/profileNewCopy.html', values))

    def post_as_user(self, user, logoutUri):
        title = self.request.get('titleBook')
        logging.debug(title)
        
        tipoOferta = self.request.get('TipoOferta')
        precio = self.request.get('precio')
        fechaLim = self.request.get('fechaLimite')
        Paginas=self.request.get('Paginas')
        edicion=self.request.get('Edicion')   
        formato=self.request.get('Formato')
        
        #####Conversiones######
        import time
        #fechaf=time.strptime(precio, "%d/%m/%Y")
        from datetime import datetime
        #fechaParseada=date.strftime(fechaLim, "%d/%m/%Y")
        #fechaParseada=datetime.datetime(*time.strptime(fechaLim, "%d/%m/%Y")[0:5]);
        fechaParseada=datetime.strptime(fechaLim, "%d/%m/%Y")
        fechaParseada=fechaParseada.date()
        
        
        preciof=float(precio)
        pagina=int(Paginas)
        edit=int(edicion)
        
        ###escribir en log#####
        logging.debug(tipoOferta);
        logging.debug(preciof);
        logging.debug(fechaParseada);
        
        
        
        book = Book.all().filter('title =', title).get()
        #book.put()
        Copy(book=book, user=user, salePrice=preciof, limitOfferDate=fechaParseada, offerType=tipoOferta,format=formato,pages=pagina,edition=edit).put()
        self.redirect('/profile/copies')

class ProfileOffersView(UserView):
    def get_as_user(self, user, logoutUri):
        values = {
            'user'        : user,
            'logoutUri'   : users.create_logout_url('/'),
            'copies'      : Copy.allCopiesWithRequests(user)            
        }
        self.response.out.write(template.render('html/profileOffers.html', values))

class ProfileApplicationsView(UserView):
    def get_as_user(self, user, logoutUri):
        values = {
            'requests'     : Request.allRequestsOf(user),
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/')
        }
        self.response.out.write(template.render('html/profileApplications.html', values))

    def post_as_user(self, user, logoutUri):
        title = self.request.get('titleBook')
        logging.debug(title)
        book = Book.all().filter('title =', title).get()
        Request(Copy=copy, User=user).put()
        self.redirect('/profile/applications')

class CopyOffersView(UserView):
    def get_as_user(self, user, logoutUri):
        title = self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =',title).get()
        selectedCopy = Copy.all().filter('user =',user).filter('book =',book).get()
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'copies'      : Copy.allCopiesWithRequests(user),
            'selectedCopy': selectedCopy,
            'copyOffers'  : Request.allRequestsFor(selectedCopy)
        }
        self.response.out.write(template.render('html/copyOffers.html', values))
 
    def post_as_user(self, user, logoutUri):
        action = self.request.get('processOffer')
        appliantUser = users.User(self.request.get('offersRadios'))
        title = self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =',title).get()
        selectedCopy = Copy.all().filter('user =',user).filter('book =',book).get()
        request = Request.all().filter('user =',appliantUser).filter('copy =',selectedCopy).get()
        
        if action=="Vender" :
            selectedCopy.offerState='Esperando confirmacion'
            request.state='Negociando'
            selectedCopy.put()
            request.put()
        elif action=="Prestar" :
            selectedCopy.offerState='Esperando confirmacion'
            request.state='Negociando'
            request.put()
            selectedCopy.put()
        elif action=="Proponer intercambio indirecto" :
            selectedCopy.offerState='Esperando confirmacion'
            request.exchangeType='Indirecto'
            request.state='Negociando'
            request.put()
            selectedCopy.put()
            
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'copies'      : Copy.allCopiesWithRequests(user),
            'selectedCopy': selectedCopy,
            'copyOffers'  : Request.allRequestsFor(selectedCopy)
        }
        
        self.response.out.write(template.render('html/copyOffers.html', values))
        
        
        
        
class SaleView(UserView):
    def get_as_user(self, user, logoutUri):
        title = self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =',title).get()
        selectedCopy = Copy.all().filter('user =',user).filter('book =',book).get()
        request = Request.all().filter('copy =', selectedCopy).filter('state =',"Aceptada").get()
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'copies'      : Copy.allCopiesWithRequests(user),
            'selectedCopy': selectedCopy,
            'request'  : request
        }
        self.response.out.write(template.render('html/sale.html', values))
    
    
class LoanView(UserView):
    def get_as_user(self, user, logoutUri):
        title = self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =',title).get()
        selectedCopy = Copy.all().filter('user =',user).filter('book =',book).get()
        request = Request.all().filter('copy =', selectedCopy).filter('state =',"Aceptada").get()
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'copies'      : Copy.allCopiesWithRequests(user),
            'selectedCopy': selectedCopy,
            'request'  : request
        }
        self.response.out.write(template.render('html/loan.html', values))
        
    def post_as_user(self, user, logoutUri):
        title = self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =',title).get()
        selectedCopy = Copy.all().filter('user =',user).filter('book =',book).get()
        request = Request.all().filter('copy =', selectedCopy).filter('state =',"Aceptada").get()
        
        selectedCopy.offerState = "No disponible"
        selectedCopy.put()
        
        Loan(copy=selectedCopy, owner=users.get_current_user(), lendingTo=request.user).put()
        
        request.delete()
        
        self.redirect('/html/profileOffers.html')
    
class ExchangeView(UserView):
    def get_as_user(self, user, logoutUri):
        title = self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =',title).get()
        selectedCopy = Copy.all().filter('user =',user).filter('book =',book).get()
        request = Request.all().filter('copy =', selectedCopy).filter('state =',"Aceptada").get()
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'copies'      : Copy.allCopiesWithRequests(user),
            'selectedCopy': selectedCopy,
            'request'  : request
        }
        self.response.out.write(template.render('html/exchange.html', values))
    
    def post_as_user(self, user, logoutUri):
        title = self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =',title).get()
        selectedCopy = Copy.all().filter('user =',user).filter('book =',book).get()
        request = Request.all().filter('copy =', selectedCopy).filter('state =',"Aceptada").get()
        
        selectedCopy.offerState = "No disponible"
        selectedCopy.put()
        
        Loan(copy=selectedCopy, owner=users.get_current_user(), lendingTo=request.user).put()
        
        request.delete()
        
        self.redirect('/html/profileOffers.html')
        
        
class AppliantCopiesView(UserView):
    def get_as_user(self, user, logoutUri):
        title = self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =',title).get()
        selectedCopy = Copy.all().filter('user =',user).filter('book =',book).get()
        appliantUser = users.User(self.request.get('appliant'))
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'copies'      : Copy.allCopiesWithRequests(user),
            'selectedCopy': selectedCopy,
            'copyOffers'  : Request.allRequestsFor(selectedCopy),
            'appliantUser' : appliantUser,
            'appliantCopies' : Copy.allCopiesOf(appliantUser)
        }
        self.response.out.write(template.render('html/appliantCopies.html', values))
    
    def post_as_user(self, user, logoutUri):
        action = self.request.get('processOffer')
        title = self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =',title).get()
        selectedCopy = Copy.all().filter('user =',user).filter('book =',book).get()
        appliantUser = users.User(self.request.get('appliant'))
        
        if action=="Proponer intercambio indirecto" :
            selectedCopy.offerState='Esperando confirmacion'
            request.exchangeType='Indirecto'
            request.state='Negociando'
            selectedCopy.put()
            request.put()
        elif action=="Proponer este libro para intercambio" :
            selectedCopy.offerState='Esperando confirmacion'
            request.state='Negociando'
            request.exchangeType='Directo'
            request.put()
            selectedCopy.put()
        
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'copies'      : Copy.allCopiesWithRequests(user),
            'selectedCopy': selectedCopy,
            'copyOffers'  : Request.allRequestsFor(selectedCopy),
            'appliantUser' : appliantUser,
            'appliantCopies' : Copy.allCopiesOf(appliantUser)
        }
        self.response.out.write(template.render('html/appliantCopies.html', values))

class ProfileHistorialView(UserView):
    def get_as_user(self, user, logoutUri):
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/')
        }
        self.response.out.write(template.render('html/profileHistorial.html', values))

# Página del buscador.
class SearchView(UserView):
    def get_as_user(self, user, logoutUri):
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/')
        }
        self.response.out.write(template.render('html/search.html', values))

    def get_as_anom(self):
        values = {
            'loginUri'   : users.create_login_url(self.request.uri),
            'newUserUri' : 'http://accounts.google.com'
        }
        self.response.out.write(template.render('html/search.html', values))
		
		
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

