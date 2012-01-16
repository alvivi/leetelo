
# -*- coding: utf-8 -*-

# En este fichero se definen las vistas de la aplicación web. Las vistas se
# encargar de recoger los datos que sean necesarios, utilzar los modelos y
# luego devolver algo al usurio (normalemente una página HTML).

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import images
from google.appengine.api import logservice
from google.appengine.api import mail
from google.appengine.ext.webapp import template
from models import *
from functions import *
import logging
import time
import urllib
import hashlib
import unicodedata
from datetime import datetime
from compiler.ast import Break


def elimina_tildes(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))


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
            userAvatar = UserAvatar.all().filter('user =', user).get()
            if userAvatar:
                avatarImg = userAvatar
            else:
                avatarImg = ""
            return self.get_as_user(user, logout, avatarImg)
        else:
            return self.get_as_anom()

    def get_as_user(self, user, logoutUri, avatarImg):
        self.redirect('/')

    def get_as_anom(self):
        self.redirect('/')

    def post(self):
        user = users.get_current_user()
        if user:
            logout = users.create_logout_url('/')
            userAvatar = UserAvatar.all().filter('user =', user).get()
            if userAvatar:
                avatarImg = userAvatar
            else:
                avatarImg = ""
            return self.post_as_user(user, logout, avatarImg)
        else :
            return selt.post_as_anom()

    def post_as_user(self, user, logoutUri):
        self.redirect('/')

    def post_as_anom(self):
        self.redirect('/')


class BooksByTitleRequest(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/javascript'
        books = Book.all()
        book_count = books.count()
        current = 1
        json = u'['
        for book in books.fetch(512):
            json += u'\"' +book.title + u'\"'
            if current != book_count: json += u','
            current += 1
        json += u']'
        self.response.out.write(json)

# Pérfil de usuario. Vista compartida entre todas las subsecciones del perfil
# de usuario.
class ProfileView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        self.redirect('/profile/alerts')

class Image (webapp.RequestHandler):
    def get(self):
        avatarUser = users.User(self.request.get('user'))
        avatar = UserAvatar.all().filter('user =', avatarUser).get()
        greeting = db.get(avatar.key())

        if greeting.avatar:
            self.response.headers['Content-Type'] = "img/png"
            self.response.out.write(greeting.avatar)
        else:
            self.response.out.write("No image")

class ProfileAccountView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        error = self.request.get('error')
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg,
            'error'      : error
        }
        self.response.out.write(template.render('html/profileAccount.html', values))

    def post_as_user(self, user, logoutUri, avatarImg):
        previousAvatar = UserAvatar.all().filter('user = ',user).get()
        if previousAvatar:
            previousAvatar.delete()

        avatar = self.request.get("imagen")
        UserAvatar(user = user, avatar = db.Blob(avatar)).put()
        userAvatar = UserAvatar.all().filter('user = ',user).get()
        if len(userAvatar.avatar) > 10000:
            userAvatar.delete()
            if previousAvatar:
                previousAvatar.put()
            self.redirect('/profile/account?error=true')
        else:
            self.redirect('/profile/alerts')

class ProfileAlertsView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        
        tod = Alert.setDate()
        
        
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg,
            'alerts'     : Alert.allAlertsOf(user),
            'today'      : tod
        }
        self.response.out.write(template.render('html/profileAlerts.html', values))



class ProfileCopiesView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        offset = self.request.get('offset')
        offset = int(offset) if offset else 0
        values = {
            'copies'     : Copy.all().filter('user =', user).fetch(limit=10, offset=offset),
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg
        }
        self.response.out.write(template.render('html/profileCopies.html', values))

class ProfileDeleteCopiesView(UserView):
    def post_as_user(self, user, logoutUri, avatarImg):
        try:
            copies = self.request.get('selected').split(",")
            for c in Copy.get(copies):
                if c.offerState == 'No disponible' or c.offerState == 'En oferta':
                    c.delete()
        except:
            pass
        finally:
            values = {
                'copies'     : Copy.allCopiesOf(user),
                'user'       : user,
                'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg
            }
            self.response.out.write(template.render('html/profileCopies.html', values))

# /book/new
# Vista utilizada a la hora de crear un nuevo libro
class BookNewView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        values = {
            'user'        : user,
            'logoutUri'   : users.create_logout_url('/'),
            'avatar'     : avatarImg
        }
        self.response.out.write(template.render('html/bookNew.html', values))

    def post_as_user(self, user, logoutUri, avatarImg):
        try:
            title  = self.request.get('title')
            author = self.request.get('author')
            genre  = self.request.get('genre')
            year   = int(self.request.get('year'))
            image  = db.Link(self.request.get('image'))
            if Book.all().filter('title =', title).count() > 0:
                self.redirect('/book/new?errorrepeat=true')
            else:
                Book(title=title, author=author, genre=genre, year=year, image=image).put()
                self.redirect('/profile/newcopy?selectedCopyTitle=' + title)
        except Exception, e:
            campos=[]
            strExp=str(e)
            values = {
                'user'        : user,
                'logoutUri'   : users.create_logout_url('/'),
                'textoerror'  : e,
                'error'       : True,
                'campos'      : campos
            }
            self.response.out.write(template.render('html/bookNew.html', values))
            #self.redirect('/book/new?error=true')

class BookDetailsView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        try:
            book   = Book.get(self.request.get('book'))
            copies = Copy.all().filter('book =', book).filter('offerState =', 'Con solicitud').fetch(128) + Copy.all().filter('book =', book).filter('offerState =', 'En oferta').fetch(128)
            values = {
                'user'        : user,
                'logoutUri'   : users.create_logout_url('/'),
                'avatar'     : avatarImg,
                'copies'      : copies,
                'book'        : Book.get(self.request.get('book'))
            }
            self.response.out.write(template.render('html/bookDetails.html', values))
        except:
            values = {
                'user'        : user,
                'logoutUri'   : users.create_logout_url('/'),
                'avatar'     : avatarImg,
                'error'       : True,
            }
            self.response.out.write(template.render('html/bookDetails.html', values))


class UserDetailsView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        selectedUser = users.User(self.request.get('selectedUser'))
        
        values = {
            'user'        : user,
            'logoutUri'   : users.create_logout_url('/'),
            'avatar'     : avatarImg,
            'copies'      : Copy.allCopiesOf(selectedUser),
            'selectedUser': selectedUser
        }
        self.response.out.write(template.render('html/userDetails.html', values))
        
            
            
# /profile/newcopy
# Vista que se encarga de crear una nuevo ejemplar de un libro
class ProfileNewCopyView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        title = self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =', title).get()
        values = {}
        if book:
            values = {
                'book' : book,
                'books'     : Book.all(),
                'user'       : user,
                'logoutUri'  : users.create_logout_url('/'),
                'avatar'     : avatarImg,
                'error'      : False
            }
        else:
            values = {
                'book' : Book.all().get(),
                'books'     : Book.all(),
                'user'       : user,
                'logoutUri'  : users.create_logout_url('/'),
                'avatar'     : avatarImg,
                'error'      : False
            }
        self.response.out.write(template.render('html/profileNewCopy.html', values))

    def post_as_user(self, user, logoutUri, avatarImg):
        try:
            error = 1
            title      = self.request.get('titleBook')
            book       = Book.all().filter('title =', title).get()
            edit       = int(self.request.get('edicion'))
            error = 2
            formato    = self.request.get('Formato')
            lang       = self.request.get('Idioma')
            pagina     = int(self.request.get('paginas'))
            tipoOferta = self.request.get('TipoOferta')

            if tipoOferta == "Venta":
               precio = self.request.get('precio')
               fechaLim = self.request.get('fechaLimite')
               fechaParseada=datetime.strptime(fechaLim, "%d/%m/%Y")
               fechaParseada=fechaParseada.date()
               preciof=float(precio)
               Copy(book=book, user=user, salePrice=preciof, language=lang, limitOfferDate=fechaParseada, offerType=tipoOferta, offerState="En oferta",format=formato, pages=pagina, edition=edit).put()

            if tipoOferta == "Intercambio" or tipoOferta == "Prestamo":
               fechaLim = self.request.get('fechaLimite')
               fechaParseada=datetime.strptime(fechaLim, "%d/%m/%Y")
               fechaParseada=fechaParseada.date()
               Copy(book=book, user=user, limitOfferDate=fechaParseada, language=lang, offerType=tipoOferta,format=formato,pages=pagina,edition=edit, offerState="En oferta").put()

            if tipoOferta == "Ninguna":
                Copy(book=book, user=user, offerType=tipoOferta, format=formato, pages=pagina, language=lang, edition=edit, offerState="No disponible").put()

            self.redirect('/profile/copies')

        except Exception, e:
            campos=[]
            strExp=str(e)
            
            if error == 1:
                campos.append("edicion")
            
            if error == 2:
                campos.append("paginas")
                
            title = self.request.get('titleBook')
            book = Book.all().filter('title =', title).get()
            values = {
                'book'      : book,
                'books'     : Book.all(),
                'user'       : user,
                'logoutUri'  : users.create_logout_url('/'),
                'error'      : True,
                'textoerror' : e,
                'campos'     : campos,
                'avatar'     : avatarImg
            }
            self.response.out.write(template.render('html/profileNewCopy.html', values))

class ProfileEditCopyView(UserView):

    def get_as_user(self, user, logoutUri, avatarImg):
        key= self.request.get('selected')
        selectedCopy = Copy.get(key)
        #selectedCopy = Copy.all().filter('user =', user).filter('book =',book).get()

        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg,
            'selectedCopy': selectedCopy
        }
        if selectedCopy.offerState == "No disponible" or selectedCopy.offerState == "En oferta":self.response.out.write(template.render('html/profileEditCopy.html', values))
        else:self.response.out.write(template.render('html/profileDataCopy.html', values))



    def post_as_user(self, user, logoutUri, avatarImg):
        key = self.request.get('selected')
        selectedCopy = Copy.get(key)
        book=selectedCopy.book

        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg,
            'error'      : False,
            'selectedCopy': selectedCopy

        }

        try:
            tipoOferta = self.request.get('TipoOferta')
            Paginas=self.request.get('page')
            edicion=self.request.get('edition')
            formato=self.request.get('Formato')
            lang=self.request.get('Idioma')

            pagina=int(Paginas)
            edit=int(edicion)

            if tipoOferta == "Venta":
                precio = self.request.get('precio')
                preciof=float(precio)
                fechaLim = self.request.get('fechaLimite')
                fechaParseada=datetime.strptime(fechaLim, "%d/%m/%Y")
                fechaParseada=fechaParseada.date()

                db.delete(selectedCopy)
                Copy(book=book, user=user, salePrice=preciof, limitOfferDate=fechaParseada, offerType="Venta", format=formato, pages=pagina, edition=edit, language=lang, offerState="En oferta").put()
            elif tipoOferta == "Intercambio":
                fechaLim = self.request.get('fechaLimite')
                fechaParseada=datetime.strptime(fechaLim, "%d/%m/%Y")
                fechaParseada=fechaParseada.date()

                db.delete(selectedCopy)
                Copy(book=book, user=user,limitOfferDate=fechaParseada, offerType="Intercambio", format=formato, pages=pagina, edition=edit, language=lang, offerState="En oferta").put()
            elif tipoOferta == "Prestamo":
                fechaLim = self.request.get('fechaLimite')
                fechaParseada=datetime.strptime(fechaLim, "%d/%m/%Y")
                fechaParseada=fechaParseada.date()
                db.delete(selectedCopy)
                Copy(book=book, user=user,limitOfferDate=fechaParseada, offerType="Prestamo", format=formato, pages=pagina, edition=edit, language=lang, offerState="En oferta").put()
            else:
                db.delete(selectedCopy)
                Copy(book=book, user=user, offerType="Ninguna", format=formato, pages=pagina, edition=edit, language=lang, offerState="No disponible").put()
            self.redirect('/profile/copies')



        except:
               key = self.request.get('selected')
               selectedCopy = Copy.get(key)
               values = {

                    'user'       : user,
                    'logoutUri'  : users.create_logout_url('/'),
                    'avatar'     : avatarImg,
                    'error'      : True,
                    'selectedCopy': selectedCopy

               }
               self.response.out.write(template.render('html/profileEditCopy.html', values))


class ProfileDataCopyView(UserView):
     def get_as_user(self, user, logoutUri, avatarImg):
        key= self.request.get('selected')
        #book = Book.all().filter('title =',title).get()
        selectedCopy = Copy.get(key)

        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg,
            'selectedCopy': selectedCopy
        }
        self.response.out.write(template.render('html/profileDataCopy.html', values))



class ProfileOffersView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        values = {
            'user'        : user,
            'logoutUri'   : users.create_logout_url('/'),
            'avatar'     : avatarImg,
            'copies'      : Copy.allCopiesWithRequests(user)
        }
        self.response.out.write(template.render('html/profileOffers.html', values))

class ProfileApplicationsView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        values = {
            'requests'     : Request.allRequestsOf(user),
            'user'       : user,
            'logoutUri'  : logoutUri,
            'avatar'     : avatarImg
        }
        self.response.out.write(template.render('html/profileApplications.html', values))

class ProfileApplicationsNewView(UserView):
    def post_as_user(self, user, logoutUri, avatarImg):
        try:
            copy = Copy.get(self.request.get('copy'))
            if copy.user == user:
                self.response.out.write(u'Usted ya posee este ejemplar.')
            elif Request.all().filter('user =', user).filter('copy =', copy).count() > 0:
                self.response.out.write(u'Ya ha solicitado este ejemplar.')
            else:
                Request(copy=copy, user=user, state='Sin contestar').put()
                HistoricalRequest(appliant=user, copy=copy, initialUser=user, state='Sin contestar', initialOfferType=copy.offerType).put()
                copy.offerState = 'Con solicitud'
                copy.put()
                # notificación: notificar a "copy.user" que tiene una nueva solicitud sobre el libro "copy"
                Alert( user=copy.user, type='Solicitud: Nueva', date=Alert.setDate(), description='El usuario %s solicita tu libro %s.' % (user.email() , copy.book.title) ).put()
                self.response.out.write('OK')
        except:
            self.response.out.write(u'No ha sido posible realizar su petición.')


class ProfileCopyOffersView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        selectedCopy = Copy.get(self.request.get('selectedCopy'))
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg,
            'copies'      : Copy.allCopiesWithRequests(user),
            'selectedCopy': selectedCopy,
            'copyRequests'  : Request.allRequestsFor(selectedCopy)
        }
        self.response.out.write(template.render('html/copyOffers.html', values))

    def post_as_user(self, user, logoutUri, avatarImg):
        action = self.request.get('action')
        selectedCopy = Copy.get(self.request.get('selectedCopy'))
        request = Request.get(self.request.get('requestKey'))
        appliantUser = request.user
        
        if action=="Rechazar oferta":
            HistoricalRequest(appliant=appliantUser, copy=selectedCopy, initialUser=user, state='Rechazada', initialOfferType=selectedCopy.offerType).put()
            if request.state=='Sin contestar':
                request.delete()
                if len(Request.allRequestsFor(selectedCopy)) == 0:
                    selectedCopy.offerState = 'En oferta'
                else:
                    selectedCopy.offerState = 'Con solicitud'
                selectedCopy.put()
                # notificación: notificar a appliantUser de que su solicitud se ha rechazado
                Alert( user=appliantUser, type='Solicitud: Rechazada', date=Alert.setDate(), description='El usuario %s ha rechazado tu solicitud por el libro %s.' % (user.email() , selectedCopy.book.title) ).put()
                
            else:
                request.state='Sin contestar'
                request.put()
                selectedCopy.offerState='Con solicitud'
                selectedCopy.put()
                # notificación: notificar a appliantUser de que su solicitud se ha cancelado
                Alert( user=appliantUser, type='Solicitud: Cancelada', date=Alert.setDate(), description='Tu solicitud por el libro %s de %s ha sido cancelada.' % (selectedCopy.book.title, user.email()) ).put()
                
        else:
            selectedCopy.offerState='Esperando confirmacion'
            request.state='Negociando'
            if action=="Proponer intercambio indirecto" :
                request.exchangeType='Indirecto'
            elif action=="Proponer este libro para intercambio":
                wantedCopy = Copy.get(self.request.get('appliantSelectedCopy'))
                request.exchangeCopy = wantedCopy
                request.exchangeType='Directo'
            request.put()
            selectedCopy.put()
            HistoricalRequest(appliant=appliantUser, copy=selectedCopy, initialUser=user, state=request.state, initialOfferType=selectedCopy.offerType).put()
            # notificación: notificar a appliantUser que su solicitud se ha aceptado
            Alert( user=appliantUser, type='Solicitud: Aceptada', date=Alert.setDate(), description='El usuario %s ha aceptado tu solicitud por el libro %s. Debes confirmar el intercambio.' % (user.email() , selectedCopy.book.title) ).put()
        
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg,
            'copies'      : Copy.allCopiesWithRequests(user),
            'selectedCopy': selectedCopy,
            'copyRequests'  : Request.allRequestsFor(selectedCopy)
        }

        self.redirect('/profile/copyoffers?selectedCopy=' + str(selectedCopy.key()))


class ApplicationContentView(UserView):
    def get_as_user(self,user,logoutUri,avatarImg):
        request = Request.get(self.request.get('requestKey'))
	values = {
            'requests'     : Request.allRequestsOf(user),
            'selectedCopy' : request.copy,
            'request'    : request,
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg

        }
        self.response.out.write(template.render('html/applicationcontent.html',values))

    def post_as_user(self, user, logoutUri, avatarImg):
        action = self.request.get('action')
        request = Request.get(self.request.get('requestKey'))
        ownerUser = request.copy.user
        selectedCopy = request.copy

        if action == "Confirmar":
            request.state='Aceptada'
            request.put()
            
            if selectedCopy.offerType=="Venta":
                Transaction(copy=selectedCopy, owner=ownerUser, appliant=user, transactionType=selectedCopy.offerType).put()
            elif selectedCopy.offerType=="Intercambio" and request.exchangeType=="Indirecto":
                Transaction(copy=selectedCopy, owner=ownerUser, appliant=user, transactionType=selectedCopy.offerType, exchangeType="Indirecto").put()
            selectedCopy.offerState='Esperando recepcion'
            selectedCopy.put()
            
            HistoricalRequest(copy=selectedCopy, initialUser=ownerUser, appliant=user, state='Aceptada', initialOfferType=selectedCopy.offerType).put()
            
            #eliminar el resto de solicitudes sobre esta oferta y pasarlas al historico
            notAnsweredRequests = Request.getNotAnsweredRequest(selectedCopy)
            for r in notAnsweredRequests:
                HistoricalRequest(copy=selectedCopy, initialUser=ownerUser, appliant=r.user, state='Rechazada', initialOfferType=selectedCopy.offerType).put()
                r.delete()
                # notificación: notificar a r.user que se ha rechazado su solicitud porque se está realizando una transacción con otro usuario. El libro ya no está en oferta.
                Alert( user=r.user, type='Solicitud: Rechazada', date=Alert.setDate(), description='Tu solicitud por el libro %s de %s ha sido cancelada. El libro ya no esta en oferta.' % (selectedCopy.book.title, user.email()) ).put()
                
        elif action == "Recibido!":
            if selectedCopy.offerType=="Venta" or (selectedCopy.offerType == "Intercambio" and request.exchangeType == "Indirecto"):
                transaction = Transaction.all().filter('copy =',selectedCopy).filter('owner =', ownerUser).filter('appliant =',user).filter('transactionType =',selectedCopy.offerType).get()
                transaction.endDate = datetime.now()#.date()
                transaction.put()
                
                selectedCopy.offerState = 'No disponible'
                selectedCopy.offerType = 'Ninguna'
                selectedCopy.user = user
                selectedCopy.put()

                request.delete()
                # notificación opcional: notificar a ownerUser de que el libro ha llegado a user
                Alert( user=ownerUser, type='Solicitud: Finalizada', date=Alert.setDate(), description='El usuario %s ha recibido tu libro %s.' % (user.email() , selectedCopy.book.title) ).put()

            elif selectedCopy.offerType=="Intercambio" and request.exchangeType=="Directo":
                transaction = Transaction.all().filter('copy =',selectedCopy).filter('owner =', ownerUser).filter('appliant =',user).filter('transactionType =',selectedCopy.offerType).filter('appliantCopy =',request.exchangeCopy).filter('exchangeType =','Directo').get()
                
                if transaction==None or (transaction!=None and transaction.endDate!=None):
                    Transaction(copy=selectedCopy, owner=ownerUser, appliant=user, transactionType=selectedCopy.offerType, appliantCopy=request.exchangeCopy, exchangeType="Directo").put()
                    
                    request.llegaCopia1 = True
                    selectedCopy.put()
                    request.put()
                else:
                    transaction.endDate = datetime.now()#.date()
                    transaction.put()
                    selectedCopy.offerState = 'No disponible'
                    selectedCopy.offerType = 'Ninguna'
                    selectedCopy.user = user
                    selectedCopy.put()
                    request.exchangeCopy.offerState = 'No disponible'
                    request.exchangeCopy.offerType = 'Ninguna'
                    request.exchangeCopy.user = ownerUser
                    request.exchangeCopy.put()
                    request.delete()
                    
                # notificación opcional: notificar a ownerUser de que el libro ha llegado a user
                Alert( user=ownerUser, type='Solicitud: Finalizada', date=Alert.setDate(), description='El usuario %s ha recibido tu libro %s.' % (user.email() , selectedCopy.book.title) ).put()
                
            elif selectedCopy.offerType=="Prestamo":
                selectedCopy.offerState = 'Prestado'
                selectedCopy.put()
                Transaction(copy=selectedCopy, owner=ownerUser, appliant=user, transactionType=selectedCopy.offerType).put()
                # notificación opcional: notificar a ownerUser de que el libro que prestó le ha llegado a user
                Alert( user=ownerUser, type='Solicitud: Finalizada', date=Alert.setDate(), description='El usuario %s ha recibido tu libro %s.' % (user.email() , selectedCopy.book.title) ).put()
                
        elif action=="Cancelar":
            request.delete()
            if len(Request.allRequestsFor(selectedCopy)) == 0:
                selectedCopy.offerState = 'En oferta'
            else:
                selectedCopy.offerState = 'Con solicitud'
            selectedCopy.put()
            # notificación: notificar a ownerUser que user ha cancelado la solicitud
            Alert( user=ownerUser, type='Solicitud: Cancelada', date=Alert.setDate(), description='La solicitud por el libro %s ha sido cancelada por %s.' % (selectedCopy.book.title, user.email()) ).put()
            HistoricalRequest(copy=selectedCopy, initialUser=ownerUser, appliant=user, state='Rechazada', initialOfferType=selectedCopy.offerType).put()
        

        values = {
            'requests'     : Request.allRequestsOf(user),
            'user'       : user,
            'avatar'     : avatarImg,
            'logoutUri'  : users.create_logout_url('/')
        }
        self.response.out.write(template.render('html/profileApplications.html', values))



class TransactionView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        selectedCopy = Copy.get(self.request.get('selectedCopy'))
        request = Request.all().filter('copy =', selectedCopy).filter('state =',"Aceptada").get()
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg,
            'copies'      : Copy.allCopiesWithRequests(user),
            'selectedCopy': selectedCopy,
            'request'  : request
        }
        self.response.out.write(template.render('html/transaction.html', values))
        
    def post_as_user(self, user, logoutUri, avatarImg):
        selectedCopy = Copy.get(self.request.get('selectedCopy'))
        request = Request.get(self.request.get('requestKey'))
        
        if selectedCopy.offerType=="Intercambio":
            transaction = Transaction.all().filter('copy =',selectedCopy).filter('owner =', user).filter('appliant =',request.user).filter('transactionType =',selectedCopy.offerType).filter('appliantCopy =',request.exchangeCopy).filter('exchangeType =',"Directo").get()
            
            if transaction==None or (transaction!=None and transaction.endDate!=None):
                Transaction(copy=selectedCopy, owner=user, appliant=request.user, transactionType=selectedCopy.offerType, appliantCopy=request.exchangeCopy, exchangeType="Directo").put()
                
                request.llegaCopia2 = True
                selectedCopy.put()
                request.put()
            else:
                transaction.endDate = datetime.now()#.date()
                transaction.put()
                selectedCopy.offerState = 'No disponible'
                selectedCopy.offerType = 'Ninguna'
                selectedCopy.user = request.user
                selectedCopy.put()
                request.exchangeCopy.offerState = 'No disponible'
                request.exchangeCopy.offerType = 'Ninguna'
                request.exchangeCopy.user = user
                request.exchangeCopy.put()
                request.delete()
                
            # notificación opcional: notificar a request.user que el libro que ha intercambiado ya le ha llegado a user
            Alert( user=request.user, type='Solicitud: Finalizada', date=Alert.setDate(), description='El usuario %s ha recibido tu libro %s.' % (user.email() , selectedCopy.book.title) ).put()
            
        elif selectedCopy.offerType=="Prestamo":
            selectedCopy.offerState = "No disponible"
            selectedCopy.offerType = "Ninguna"
            selectedCopy.put()
            # notificación opcional: notificar a request.user que el libro que devolvió ya le ha llegado al dueño
            Alert( user=request.user, type='Solicitud: Finalizada', date=Alert.setDate(), description='El usuario %s ha recibido tu libro %s.' % (user.email() , selectedCopy.book.title) ).put()
            
            transaction = Transaction.all().filter('copy =',selectedCopy).filter('owner =',user).filter('appliant =',request.user).filter('transactionType =',"Prestamo").get()
            transaction.endDate=datetime.now()#.date()
            transaction.put()
            
            request.delete()

        values = {
            'user'        : user,
            'logoutUri'   : users.create_logout_url('/'),
            'avatar'      : avatarImg,
            'copies'      : Copy.allCopiesWithRequests(user)
        }
        self.response.out.write(template.render('html/profileOffers.html', values))




class AppliantCopiesView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        selectedCopy = Copy.get(self.request.get('selectedCopy'))
        request = Request.get(self.request.get('requestKey'))
        appliantUser = request.user
        
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg,
            'copies'      : Copy.allCopiesWithRequests(user),
            'selectedCopy': selectedCopy,
            'copyRequests'  : Request.allRequestsFor(selectedCopy),
            'appliantUser' : appliantUser,
            'appliantCopies' : Copy.allCopiesOf(appliantUser),
            'request' : request
        }
        self.response.out.write(template.render('html/appliantCopies.html', values))
        
    

class ProfileHistorialView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg
        }
        self.response.out.write(template.render('html/profileHistorial.html', values))

# Página del buscador.
class SearchView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
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




#Vista general del mis clubs

class ProfileClubListView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        offset = self.request.get('offset')
        offset = int(offset) if offset else 0
        values = {
            'participations'     : Club_User.all().filter('user =', user).fetch(limit=10, offset=offset),
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg
        }

        self.response.out.write(template.render('html/profileClub.html', values))


class ProfileDisableClubsView(UserView):
    def post_as_user(self, user, logoutUri, avatarImg):
        try:
            c = Club.get(self.request.get('selected'))
            if c.state == 'Habilitado':
                c.state = 'Deshabilitado'
                c.put()
            elif c.state == 'Deshabilitado':
                c.state = 'Habilitado'
                c.put()

        except:
            pass
        finally:
            offset = self.request.get('offset')
            offset = int(offset) if offset else 0
            values = {
                'participations'      : Club_User.all().filter('user =', user).fetch(limit=10, offset=offset),
                'user'       : user,
                'logoutUri'  : users.create_logout_url('/'),
                'avatar'     : avatarImg
            }
            self.response.out.write(template.render('html/profileClub.html', values))

#Vista para darse de baja en un club
class ProfileDeleteParticipationView(UserView):
    def post_as_user(self, user, logoutUri, avatarImg):
        selectedClub = Club.get(self.request.get('selected'))
        participation = Club_User.all().filter('user =', user).filter('club =', selectedClub).get()
        participation.delete()
        self.redirect('/profile/club')

#Vista para aceptar o rechazar invitaciones a clubs
class ProfileAnswerInvitationView(UserView):
    def post_as_user(self, user, logoutUri, avatarImg):
        selectedClub = Club.get(self.request.get('selected'))
        option = self.request.get('option')
        if option == 'Aceptar':
            participation = Club_User.all().filter('user =', user).filter('club =', selectedClub).get()
            participation.state = 'Invitacion Aceptada'
            participation.put()
        elif option == 'Rechazar':
            participation = Club_User.all().filter('user =', user).filter('club =', selectedClub).get()
            participation.state = 'Invitacion Rechazada'
            participation.put()
        self.redirect('/profile/club')



class ProfileAnswerRequestView(UserView):
    def post_as_user(self, user, logoutUri, avatarImg):
        participation = Club_User.get(self.request.get('selected'))
        option = self.request.get('option')
        if option == 'Aceptar':
            participation.state = 'Solicitud Aceptada'
            participation.put()
            # notificación: notificar a participation.user que su solicitud sobre el club ha sido aceptada
            Alert( user=participation.user, type='Club: Aceptado', date=Alert.setDate(), description='Has sido aceptado en el club %s.' % ( participation.club.name ) ).put()
            
        elif option == 'Rechazar':
            participation.state = 'Solicitud Rechazada'
            participation.put()
            # notificación: notificar a participation.user que su solicitud sobre el club ha sido rechazada
            Alert( user=participation.user, type='Club: Rechazado', date=Alert.setDate(), description='Has sido rechazado en el club %s.' % ( participation.club.name ) ).put()
        self.redirect('/profile/club/content?selectedClub=' + str(participation.club.key()) )

# /profile/newclub
# Vista que se encarga de crear una nuevo club
class ProfileNewClubView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        values={
                'user': user,
                'books': Book.all(),
                'logoutUri': users.create_logout_url('/'),
                'error': False,
                'avatar': avatarImg
                }
        self.response.out.write(template.render('html/profileNewClub.html', values))


    def post_as_user(self, user, logoutUri, avatarImg):
        try:
            nameClub= self.request.get('nombreClub')
            description= self.request.get('description')
            imagen_txt = self.request.get('image')
            generos = self.request.get('resultado').split(',')
            #autor = self.request.get('autores')
            libro = self.request.get('libros')
            book=None
            invitaciones = self.request.get('invitaciones').split(',')

            if imagen_txt == '' or imagen_txt == 'http://':
                imagen=None
            else:
                imagen = db.Link(imagen_txt)

            #Ya no hace falta, el cliente lo ha cambiado
            #if len(generos[0])<2 and libro == '' and autor == '':
            #    raise ValueError("No se cumple la condición")


            if not(libro is'Ninguno'):
                book = Book.all().filter('title =', libro).get()

            if len(invitaciones)<2 and len(invitaciones[0])<2:
                invitaciones = [];            
            
            #if Club.all().filter('name =', nameClub).count() > 0:
            #   self.redirect('/profile/club/new?errorrepeat=true')
            
            #NO DISTINGUIR ENTRE MAYUSCULAS MINUSCULAS Y ACENTOS
            repetido = False
            for clubf in Club.all():
                nombre=elimina_tildes(clubf.name).lower()
                nombreNuevo=elimina_tildes(nameClub).lower()
                logging.debug(nombre)
                if nombre == nombreNuevo:
                    repetido= True
                    break
                    
            if repetido:
                self.redirect('/profile/club/new?errorrepeat=true')
                
            else:
                club_actual=Club(book=book, owner=user, name=nameClub, description=description, image=imagen, genre=generos, invitaciones=invitaciones, state="Habilitado").put()
                logging.debug(club_actual)
                Club_User(user=user, club=club_actual,state="Propietario").put()
                for inv in invitaciones:
                    if not(inv == ''):
                        user_ins=users.User(inv)
                        Club_User(user=user_ins, club=club_actual,state="Invitado").put()
                        user_model = Usuario.all().filter('user =', user_ins).get()
                        if not user_model:
                            logging.debug('enviar correo')
                            try:
                                mail.send_mail(sender="Leetelo Web",
                                to=inv,
                                subject="Invitacion a club",
                                body="""
                                Has sido invitado al Club """ + nameClub + """ por el usuario %s, Registrate ya!
                                Copia esta direccion en tu navegador.
                                http://localhost:8080/
                                """ % user)
                            except Exception, e:
                                logging.debug(e)
                        # notificación: si el usuario sí que existe en el sistema, enviarle notificación avisando de que tiene una nueva invitación a club
                        Alert( user=user_ins, type='Club: Invitacion', date=Alert.setDate(), description='Has sido invitado al club %s por el usuario %s.' % ( nameClub ,user.email() ) ).put()
                self.redirect('/profile/club')
                logging.debug(invitaciones)

        except Exception, e:
            campos=[]
            strExp=str(e)
            
            if "URL" in strExp:
                campos.append("image")
            
            if "name" in strExp:
                campos.append("nombreClub")
                
            libro = self.request.get('libros')
            book = Book.all().filter('title =', libro).get()
            values = {
                 'book'      : book,
                 'books'     : Book.all(),
                 'user'       : user,
                 'logoutUri'  : users.create_logout_url('/'),
                 'error'      : True,
                 'textoerror' : e,
                 'campos'     : campos,
                 'avatar'     : avatarImg
              }
            self.response.out.write(template.render('html/profileNewClub.html', values))

# /profile/editclub
# Vista que se encarga de editar un club ya creado
class ProfileEditClubView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        key= self.request.get('selectedClub')
        selectedClub = Club.get(key)
        values = {
            'user'       : user,
            'books'      : Book.all(),
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg,
            'selectedClub': selectedClub
        }
        if selectedClub.state == "Habilitado" and selectedClub.owner == user :self.response.out.write(template.render('html/profileEditClub.html', values))
        else:self.response.out.write(template.render('html/profileDataClub.html', values))

    def post_as_user(self, user, logoutUri, avatarImg):
        key = self.request.get('selectedClub')
        selectedClub = Club.get(key)

        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg,
            'error'      : False,
            'errorrepeat': False,
            'selectedClub': selectedClub
        }
        try:
            invitados_existentes=selectedClub.invitaciones
            nameClub= self.request.get('nombreClub')
            description= self.request.get('description')
            imagen_txt = self.request.get('image')
            generos= self.request.get('resultado').split(',')
            #autor= self.request.get('autores')
            libro= self.request.get('libros')
            book=None
            nuevos_invitados= self.request.get('invitaciones').split(',')
            invitaciones=invitados_existentes+nuevos_invitados


            #Comprovaciones
            if imagen_txt == '' or imagen_txt == 'http://' or imagen_txt == 'None':
                imagen=None
            else:
                imagen = db.Link(imagen_txt)

            if not(libro is'Ninguno'):
                book = Book.all().filter('title =', libro).get()


            #comprovar que no hay email Un poco chungo xo....
            if len(invitaciones)<2 and len(invitaciones[0])<2:
                invitaciones = [];

            if len(nuevos_invitados)<2 and len(nuevos_invitados[0])<2:
                nuevos_invitados = [];

            
            #NO DISTINGUIR ENTRE MAYUSCULAS MINUSCULAS Y ACENTOS
            if elimina_tildes(selectedClub.name).lower() == elimina_tildes(nameClub).lower():

                selectedClub.description=description
                selectedClub.genre=generos
                #selectedClub.author=autor
                selectedClub.book=book
                selectedClub.invitaciones=invitaciones
                selectedClub.image=imagen
                selectedClub.state="Habilitado"
                selectedClub.put()

                for inv in nuevos_invitados:
                    if not(inv == ''):
                        user_ins=users.User(inv)
                        Club_User(user=user_ins, club=selectedClub,state="Invitado").put()
                        user_model = Usuario.all().filter('user =', user_ins).get()
                        if not user_model:
                            logging.debug('enviar correo')
                            try:
                                mail.send_mail(sender="Leetelo Web",
                                to=inv,
                                subject="Invitacion a club",
                                body="""
                                Has sido invitado al Club """ + nameClub + """ por el usuario %s, Registrate ya!
                                Copia esta direccion en tu navegador.
                                http://localhost:8080/
                                """ % user)
                            except Exception, e:
                                logging.debug(e)
                        # notificación: si el usuario sí que existe en el sistema, enviarle notificación avisando de que tiene una nueva invitación a club
                        Alert( user=user_ins, type='Club: Invitacion', date=Alert.setDate(), description='Has sido invitado al club %s por el usuario %s.' % ( nameClub,user.email() ) ).put()
                self.redirect('/profile/club')
            else:
                if Club.all().filter('name =', nameClub).count()>0:
                    values = {
                         'user'       : user,
                         'logoutUri'  : users.create_logout_url('/'),
                         'avatar'     : avatarImg,
                         'error'      : False,
                         'errorrepeat': True,
                         'selectedClub': selectedClub

                    }
                    self.response.out.write(template.render('html/profileEditClub.html', values))
                    #self.redirect('/profile/club/edit?errorrepeat=true')
                else:
                    selectedClub.name=nameClub
                    selectedClub.description=description
                    selectedClub.genre=generos
                    #selectedClub.author=autor
                    selectedClub.book=book
                    selectedClub.invitaciones=invitaciones
                    selectedClub.image=imagen
                    selectedClub.state="Habilitado"
                    selectedClub.put()

                    for inv in nuevos_invitados:
                        if not(inv == ''):
                            user_ins=users.User(inv)
                            Club_User(user=user_ins, club=selectedClub,state="Invitado").put()
                            user_model = Usuario.all().filter('user =', user_ins).get()
                            if not user_model:
                                logging.debug('enviar correo')
                                mail.send_mail(sender="Leetelo Web",
                                to=inv,
                                subject="Invitacion a club",
                                body="""
                                Has sido invitado al Club """ + nameClub + """ por el usuario %s, ¡Registrate ya!
                                \nCopia esta direccion en tu navegador:\n
                                http://localhost:8080/
                                """ % user)

                    self.redirect('/profile/club')
        except Exception, e:
            campos=[]
            strExp=str(e)
            
            if "URL" in strExp:
                campos.append("image")
            
            if "name" in strExp:
                campos.append("nombreClub")
            
            key = self.request.get('selectedClub')
            selectedClub = Club.get(key)
            values = {
                    'user'       : user,
                    'logoutUri'  : users.create_logout_url('/'),
                    'avatar'     : avatarImg,
                    'error'      : True,
                    'errorrepeat': False,
                    'textoerror' : e,
                    'campos'     : campos,
                    'selectedClub': selectedClub
               }
            self.response.out.write(template.render('html/profileEditClub.html', values))


class ProfileDataClubView(UserView):
   def get_as_user(self, user, logoutUri, avatarImg):
        key= self.request.get('selectedClub')
        selectedClub = Club.get(key)
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg,
            'selectedClub': selectedClub
        }


class ProfileClubContentView(UserView):
   def get_as_user(self, user, logoutUri, avatarImg):
        key = self.request.get('selectedClub')
        selectedClub = Club.get(key)
        comments = ClubComment.all().filter('club =', selectedClub).fetch(512)
        values = {
            'avatar'         : avatarImg,
            'comments'       : comments,
            'logoutUri'      : users.create_logout_url('/'),
            'participations' : Club_User.allParticipantsOf(selectedClub),
            'selectedClub'   : selectedClub,
            'user'           : user
        }
        self.response.out.write(template.render('html/profileClubContent.html', values))

class ProfileDisabledClubContentView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        key = self.request.get('selectedClub')
        selectedClub = Club.get(key)
        comments = ClubComment.all().filter('club =', selectedClub).fetch(512)
        values = {
            'avatar'         : avatarImg,
            'comments'       : comments,
            'logoutUri'      : users.create_logout_url('/'),
            'participations' : Club_User.allParticipantsOf(selectedClub),
            'selectedClub'   : selectedClub,
            'user'           : user
        }
        self.response.out.write(template.render('html/profileDisabledClubContent.html', values))

# Añade comentarios a un club
class ProfilenClubCommentNew(UserView):
    def post_as_user(self, user, logoutUri, avatarImg):
        try:
            clubKey = self.request.get('selectedClub')
            club = Club.get(clubKey)
            text = self.request.get('comment')
            comment = Comment(text=text, user=user).put()
            ClubComment(club=club, comment=comment).put()
        except:
            pass
        finally:
            self.redirect('/profile/club/content?selectedClub=' + clubKey)

# Página principal.
class IndexView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
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


class clubView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):

        nombre = self.request.get("club_name")
        creador = self.request.get("club_maker")
        genero = self.request.get("club_genre")
        libro = self.request.get("book_name")


        res = ClubResult.searchAll(nombre,creador,genero,libro)

        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'misclubs'  : Club_User.clubsForUser(user),
            'results' : res
        }


        self.response.out.write(template.render('html/club.html', values))


    def get_as_anom(self):
        values = {
            'loginUri'   : users.create_login_url(self.request.uri),
            'newUserUri' : 'http://accounts.google.com'
        }
        self.response.out.write(template.render('html/club.html', values))

class ClubRequestParticipationView(UserView):
    def post_as_user(self, user, logoutUri, avatarImg):
        selectedClub = Club.get(self.request.get('selected'))
        participation = Club_User.all().filter('user =',user).filter('club =',selectedClub).get()
        if participation:
            if participation.state == 'Invitado' or participation.state == 'Solicitado':
                self.response.out.write(u'Usted ya ha solicitado participar en este club')
            elif participation.state == 'Invitacion Aceptada' or participation.state == 'Solicitud Aceptada' or participation.state == 'Propietario':
                self.response.out.write(u'Usted ya participa en este club')
                #self.redirect('/profile/club/content?selectedClub=' + str(selectedClub.key()))
            else:
                participation.state='Solicitado'
                participation.put()
                self.response.out.write('OK')
                Alert( user=selectedClub.owner, type='Club: Solicitud', date=Alert.setDate(), description='Usuario %s quiere unirse al club %s.' % ( user.email(), selectedClub.name ) ).put()
        else:
            Club_User(user=user,club=selectedClub,state='Solicitado').put()
            self.response.out.write('OK')
            Alert( user=selectedClub.owner, type='Club: Solicitud', date=Alert.setDate(), description='Usuario %s quiere unirse al club %s.' % ( user.email(), selectedClub.name ) ).put()
            #self.redirect('/profile/club/disabledcontent?selectedClub=' + str(selectedClub.key()))
            



