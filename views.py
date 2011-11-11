
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
import time
from datetime import datetime

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


class ProfileNewBookView(UserView):
    def get_as_user(self, user, logoutUri):
        values = {
            'user'        : user,
            'logoutUri'   : users.create_logout_url('/'),
            
        }
        self.response.out.write(template.render('html/profileNewBook.html', values))


class ProfileNewCopyView(UserView):
    def get_as_user(self, user, logoutUri):
        title = self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =', title).get()
        values = {}
        if book:         
            values = {
                'book' : book,
                'books'     : Book.all(),
                'user'       : user,
                'logoutUri'  : users.create_logout_url('/'),
                'error'      : False
            }
        else:
            values = {
                'book' : Book.all().get(),
                'books'     : Book.all(),
                'user'       : user,
                'logoutUri'  : users.create_logout_url('/'),
                'error'      : False
            }
        self.response.out.write(template.render('html/profileNewCopy.html', values))

    def post_as_user(self, user, logoutUri):
        
        try:

            title = self.request.get('titleBook')
            logging.debug(title)
            book = Book.all().filter('title =', title).get()
            tipoOferta = self.request.get('TipoOferta')
            logging.debug(tipoOferta)
            Paginas=self.request.get('Paginas')
            edicion=self.request.get('Edicion')   
            formato=self.request.get('Formato')
            pagina=int(Paginas)
            edit=int(edicion)

            if tipoOferta == "2":
               precio = self.request.get('precio')
               fechaLim = self.request.get('fechaLimite')
               fechaParseada=datetime.strptime(fechaLim, "%d/%m/%Y")
               fechaParseada=fechaParseada.date()
               preciof=float(precio)
               Copy(book=book, user=user, salePrice=preciof, limitOfferDate=fechaParseada, offerType="Venta", offerState="En oferta",format=formato, pages=pagina, edition=edit).put()
       
            if tipoOferta == "3":
               fechaLim = self.request.get('fechaLimite')
               fechaParseada=datetime.strptime(fechaLim, "%d/%m/%Y")
               fechaParseada=fechaParseada.date()
               Copy(book=book, user=user, limitOfferDate=fechaParseada, offerType="Intercambio",format=formato,pages=pagina,edition=edit, offerState="En oferta").put()       
            
            if tipoOferta == "4":
               fechaLim = self.request.get('fechaLimite')
               fechaParseada=datetime.strptime(fechaLim, "%d/%m/%Y")
               fechaParseada=fechaParseada.date()
               Copy(book=book, user=user, limitOfferDate=fechaParseada, offerType="Prestamo",format=formato,pages=pagina,edition=edit, offerState="En oferta").put()       
            

            
            if tipoOferta == "1":
               Copy(book=book, user=user, offerType="Ninguno", format=formato, pages=pagina, edition=edit, offerState="No disponible").put() 

            ###escribir en log#####
            logging.debug(tipoOferta);
            #logging.debug(preciof);
            #logging.debug(fechaParseada);
        
        
        
            #book = Book.all().filter('title =', title).get()
            #Copy(book=book, user=user, salePrice=preciof, limitOfferDate=fechaParseada, offerType=tipoOferta,format=formato,pages=pagina,edition=edit).put()
            self.redirect('/profile/copies')
        
        except:
            title = self.request.get('selectedCopyTitle')
            book = Book.all().filter('title =', title).get()
            #selectedCopy = Copy.all().filter('user =',user).filter('book =', book).get()
            values = {
                'book' : book,
                'books'     : Book.all(),
                'user'       : user,
                'logoutUri'  : users.create_logout_url('/'),
                'error'      : True,
              
            }
            
            self.response.out.write(template.render('html/profileNewCopy.html', values))

class ProfileNewCopyView1(UserView):

    def get_as_user(self, user, logoutUri):
        title= self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =',title).get()
        selectedCopy = Copy.all().filter('user =', user).filter('book =',book).get()
       
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'selectedCopy': selectedCopy
        }
        if selectedCopy.offerState == "No disponible" or selectedCopy.offerState == "En oferta":self.response.out.write(template.render('html/profileNewCopy1.html', values))
        else:self.response.out.write(template.render('html/profileNewCopy2.html', values))
               
           

    def post_as_user(self, user, logoutUri):
        title = self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =', title).get()
        selectedCopy = Copy.all().filter('user =',user).filter('book =', book).get()
	
        logging.debug(title)
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'error'      : False,
            'selectedCopy': selectedCopy
            
        } 
        try:
            tipoOferta = self.request.get('TipoOferta')
	    precio = self.request.get('precio')
	    fechaLim = self.request.get('fechaLimite')
            Paginas=self.request.get('page')
	    edicion=self.request.get('edition')   
	    formato=self.request.get('Formato')
	    lang=self.request.get('Idioma')
            logging.debug(selectedCopy.offerState)
            estadoOferta=selectedCopy.offerState
            logging.debug(estadoOferta)
		
	    #####Conversiones######
		
	    #fechaf=time.strptime(precio, "%d/%m/%Y")
	    #from datetime import datetime
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
		
		
		
		
	    #book.put()
	    book = Book.all().filter('title =',title).get()
            db.delete(selectedCopy)
	    Copy(book=book, user=user, salePrice=preciof, limitOfferDate=fechaParseada, offerType=tipoOferta, format=formato, pages=pagina, edition=edit, language=lang, offerState=estadoOferta).put()
            logging.debug(book)
            self.redirect('/profile/copies')
            
        except:  
               title = self.request.get('selectedCopyTitle')
               book = Book.all().filter('title =', title).get()
               selectedCopy = Copy.all().filter('user =',user).filter('book =', book).get()
               values = {
                    
                    'user'       : user,
                    'logoutUri'  : users.create_logout_url('/'),
                    'error'      : True,
                    'selectedCopy': selectedCopy

               }   
               
	       self.redirect("/profile/newcopy1?selectedCopyTitle="+selectedCopy.book.title)
               
   

class ProfileNewCopyView2(UserView):
     def get_as_user(self, user, logoutUri):
        title= self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =',title).get()
        selectedCopy = Copy.all().filter('user =', user).filter('book =',book).get()
       
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'selectedCopy': selectedCopy
        }
        self.response.out.write(template.render('html/profileNewCopy2.html', values))
       


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
        
        if action=="Vender" or action=="Prestar":
            selectedCopy.offerState='Esperando confirmacion'
            request.state='Negociando'
            selectedCopy.put()
            request.put()
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
        
        
class ApplicationContentView(UserView):
    def get_as_user(self,user,logoutUri):
        title = self.request.get('selectedCopyTitle')
        ownerUser = users.User(self.request.get('owner'))
        book = Book.all().filter('title =', title).get()
        selectedCopy = Copy.all().filter('user =',ownerUser).filter('book =',book).get()
        request = Request.all().filter('user =',user).filter('copy =',selectedCopy).get()
        
	values = {
            'requests'     : Request.allRequestsOf(user),
            'selectedCopy' : selectedCopy,
            'request'    : request,
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/')
        }
        self.response.out.write(template.render('html/applicationcontent.html',values))
    
    def post_as_user(self,user,logoutUri):
        title = self.request.get('selectedCopyTitle')
        ownerUser = users.User(self.request.get('owner'))
        selectedCopy = Copy.all().filter('user =',ownerUser).filter('book =',book).get()
	selectedCopy.offerState='Esperando confirmacion'
	selectedCopy.put()
	
	request = Request.all().filter('user =',user).filter('copy =',selectedCopy).get()
	request.state='Aceptada'
	request.put()
        values = {
            'requests'     : Request.allRequestsOf(user),
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/')
        }
        self.response.out.write(template.render('html/profileApplications.html',values))
        
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
        request = Request.all().filter('copy =', selectedCopy).filter('user =', appliantUser).get()
        
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'copies'      : Copy.allCopiesWithRequests(user),
            'selectedCopy': selectedCopy,
            'copyOffers'  : Request.allRequestsFor(selectedCopy),
            'appliantUser' : appliantUser,
            'appliantCopies' : Copy.allCopiesOf(appliantUser),
            'request' : request
        }
        self.response.out.write(template.render('html/appliantCopies.html', values))
    
    def post_as_user(self, user, logoutUri):
        action = self.request.get('processOffer')
        title = self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =',title).get()
        selectedCopy = Copy.all().filter('user =',user).filter('book =',book).get()
        appliantUser = users.User(self.request.get('appliant'))
        request = Request.all().filter('copy =', selectedCopy).filter('user =', appliantUser).get()
        
        if action=="Proponer intercambio indirecto" :
            selectedCopy.offerState='Esperando confirmacion'
            request.exchangeType='Indirecto'
            request.state='Negociando'
            selectedCopy.put()
            request.put()
        elif action=="Proponer este libro para intercambio":
            selectedCopy.offerState='Esperando confirmacion'
            request.state='Negociando'
            request.exchangeType='Directo'
            request.exchangeCopy=''
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
        title = self.request.get("title")
        author = self.request.get("author")
        publisher = self.request.get("publisher")
        genre = self.request.get("genre")	
        yearFrom = self.request.get("yearFrom")
        yearTo = self.request.get("yearTo")
        optionsExchange = self.request.get("optionsExchange")
        optionsRent = self.request.get("optionsRent")
        optionsSell = self.request.get("optionsSell")	
		
        res = SearchResults.searchAll(title,author,genre,publisher,yearFrom,yearTo,optionsExchange,optionsRent,optionsSell)
		
        values = {
		'user'       : user,
		'logoutUri'  : users.create_logout_url('/'),
		'results' : res
        }
        self.response.out.write(template.render('html/search.html', values))
			
	
    def get_as_anom(self):
        title = self.request.get("title")
        author = self.request.get("author")
        publisher = self.request.get("publisher")
        genre = self.request.get("genre")	
        yearFrom = self.request.get("yearFrom")
        yearTo = self.request.get("yearTo")
        optionsExchange = self.request.get("optionsExchange")
        optionsRent = self.request.get("optionsRent")
        optionsSell = self.request.get("optionsSell")	
		
        res = SearchResults.searchAll(title,author,genre,publisher,yearFrom,yearTo,optionsExchange,optionsRent,optionsSell)
		
        values = {
		'loginUri'   : users.create_login_url(self.request.uri),
		'newUserUri' : 'http://accounts.google.com',
		'results' : res
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

