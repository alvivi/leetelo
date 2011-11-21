
# -*- coding: utf-8 -*-

# En este fichero se definen las vistas de la aplicación web. Las vistas se
# encargar de recoger los datos que sean necesarios, utilzar los modelos y
# luego devolver algo al usurio (normalemente una página HTML).

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import images
from google.appengine.ext.webapp import template
from models import *
import logging
import time
import urllib
import hashlib
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



# Pérfil de usuario. Vista compartida entre todas las subsecciones del perfil
# de usuario.
class ProfileView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        self.redirect('/profile/alerts')

class Image (webapp.RequestHandler):
    def get(self):
        greeting = db.get(self.request.get("img_id"))
        if greeting.avatar:
            self.response.headers['Content-Type'] = "image/png"
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
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg
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
    def get_as_user(self, user, logoutUri, avatarImg):
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
        except:
            self.redirect('/book/new?error=true')

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
            title      = self.request.get('titleBook')
            book       = Book.all().filter('title =', title).get()
            edit       = int(self.request.get('edicion'))
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

        except:
            title = self.request.get('titleBook')
            book = Book.all().filter('title =', title).get()
            values = {
                'book'      : book,
                'books'     : Book.all(),
                'user'       : user,
                'logoutUri'  : users.create_logout_url('/'),
                'error'      : True,
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
                copy.offerState = 'Con solicitud'
                copy.put()
                self.response.out.write('OK')
        except:
            self.response.out.write(u'No ha sido posible realizar su petición.')


class CopyOffersView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        title = self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =',title).get()
        selectedCopy = Copy.all().filter('user =',user).filter('book =',book).get()
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg,
            'copies'      : Copy.allCopiesWithRequests(user),
            'selectedCopy': selectedCopy,
            'copyOffers'  : Request.allRequestsFor(selectedCopy)
        }
        self.response.out.write(template.render('html/copyOffers.html', values))

    def post_as_user(self, user, logoutUri, avatarImg):
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
            'avatar'     : avatarImg,
            'copies'      : Copy.allCopiesWithRequests(user),
            'selectedCopy': selectedCopy,
            'copyOffers'  : Request.allRequestsFor(selectedCopy)
        }

        self.response.out.write(template.render('html/copyOffers.html', values))


class ApplicationContentView(UserView):
    def get_as_user(self,user,logoutUri,avatarImg):
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
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg

        }
        self.response.out.write(template.render('html/applicationcontent.html',values))

    def post_as_user(self, user, logoutUri, avatarImg):
        action = self.request.get('processConfirm')
        title = self.request.get('selectedCopyTitle')
        ownerUser = users.User(self.request.get('owner'))
        book = Book.all().filter('title =', title).get()
        selectedCopy = Copy.all().filter('user =',ownerUser).filter('book =',book).get()
        request = Request.all().filter('user =',user).filter('copy =',selectedCopy).get()

        if action == "Confirmar":
            request.state='Aceptada'
            request.put()

            selectedCopy.offerState='Esperando recepcion'
            selectedCopy.put()
        elif action == "Recibido!":
            if selectedCopy.offerType == "Intercambio" and request.exchangeType == "Indirecto":
                selectedCopy.offerState = 'No disponible'
                selectedCopy.offerType = 'Ninguna'
                selectedCopy.user = user
                selectedCopy.put()
                Exchange(copy1 = selectedCopy, owner1=ownerUser, owner2=user, exchangeType='Indirecto').put()
                request.delete()

            elif selectedCopy.offerType=="Intercambio" and request.exchangeType=="Directo":
                exchange = Exchange.all().filter('copy1 =',selectedCopy).filter('copy2 =',request.exchangeCopy).filter('owner1 =', ownerUser).filter('owner2 =',user).filter('exchangeType =','Directo').get()
                #getDirectExchange(selectedcopy, ownerUser, request.exchangeCopy, users.get_current_user())

                if exchange==None:
                    Exchange(copy1 = selectedCopy, owner1=ownerUser, copy2=request.exchangeCopy, owner2=user, exchangeType='Directo').put()
                    request.llegaCopia1 = True
                    selectedCopy.put()
                    request.put()
                else:
                    selectedCopy.offerState = 'No disponible'
                    selectedCopy.offerType = 'Ninguna'
                    selectedCopy.user = user
                    selectedCopy.put()
                    request.exchangeCopy.offerState = 'No disponible'
                    request.exchangeCopy.offerType = 'Ninguna'
                    request.exchangeCopy.user = ownerUser
                    request.exchangeCopy.put()
                    request.delete()

            elif selectedCopy.offerType=="Venta":
                selectedCopy.offerState = 'No disponible'
                selectedCopy.offerType = 'Ninguna'
                selectedCopy.user = user
                selectedCopy.put()

                request.delete()

                Sale(copy=selectedCopy, vendor=ownerUser, buyer=user).put()

            elif selectedCopy.offerType=="Prestamo":
                selectedCopy.offerState = 'Prestado'
                selectedCopy.put()
                Loan(copy=selectedCopy, owner=ownerUser, lendingTo=user, arrivalDate=datetime.now().date()).put()


        values = {
            'requests'     : Request.allRequestsOf(user),
            'user'       : user,
            'avatar'     : avatarImg,
            'logoutUri'  : users.create_logout_url('/')
        }
        self.response.out.write(template.render('html/profileApplications.html', values))



class SaleView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        title = self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =',title).get()
        selectedCopy = Copy.all().filter('user =',user).filter('book =',book).get()
        request = Request.all().filter('copy =', selectedCopy).filter('state =',"Aceptada").get()
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg,
            'copies'      : Copy.allCopiesWithRequests(user),
            'selectedCopy': selectedCopy,
            'request'  : request
        }
        self.response.out.write(template.render('html/sale.html', values))


class LoanView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        title = self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =',title).get()
        selectedCopy = Copy.all().filter('user =',user).filter('book =',book).get()
        request = Request.all().filter('copy =', selectedCopy).filter('state =',"Aceptada").get()
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg,
            'copies'      : Copy.allCopiesWithRequests(user),
            'selectedCopy': selectedCopy,
            'request'  : request
        }
        self.response.out.write(template.render('html/loan.html', values))

    def post_as_user(self, user, logoutUri, avatarImg):
        title = self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =',title).get()
        selectedCopy = Copy.all().filter('user =',user).filter('book =',book).get()
        request = Request.all().filter('copy =', selectedCopy).filter('state =',"Aceptada").get()

        selectedCopy.offerState = "No disponible"
        selectedCopy.offerType = "Ninguna"
        selectedCopy.put()

        Loan(copy=selectedCopy, owner=user, lendingTo=request.user, returningDate=datetime.now().date()).put()

        request.delete()

        values = {
            'user'        : user,
            'logoutUri'   : users.create_logout_url('/'),
            'avatar'      : avatarImg,
            'copies'      : Copy.allCopiesWithRequests(user)
        }
        self.response.out.write(template.render('html/profileOffers.html', values))

class ExchangeView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        title = self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =',title).get()
        selectedCopy = Copy.all().filter('user =',user).filter('book =',book).get()
        request = Request.all().filter('copy =', selectedCopy).filter('state =',"Aceptada").get()
        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg,
            'copies'      : Copy.allCopiesWithRequests(user),
            'selectedCopy': selectedCopy,
            'request'  : request
        }
        self.response.out.write(template.render('html/exchange.html', values))

    def post_as_user(self, user, logoutUri, avatarImg):
        title = self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =',title).get()
        selectedCopy = Copy.all().filter('user =',user).filter('book =',book).get()
        request = Request.all().filter('copy =', selectedCopy).filter('state =','Aceptada').get()

        exchange = Exchange.all().filter('copy1 =',selectedCopy).filter('copy2 =',request.exchangeCopy).filter('owner1 =', user).filter('owner2 =', request.user).filter('exchangeType =','Directo').get()
        #getDirectExchange(selectedcopy, users.get_current_user(), request.exchangeCopy, request.user)
        if exchange==None:
            Exchange(copy1=selectedCopy, owner1=user, copy2=request.exchangeCopy, owner2=request.user, exchangeType='Directo').put()
            request.llegaCopia2 = True
            selectedCopy.put()
            request.put()
        else:
            selectedCopy.offerState = 'No disponible'
            selectedCopy.offerType = 'Ninguna'
            selectedCopy.user = request.user
            selectedCopy.put()
            request.exchangeCopy.offerState = 'No disponible'
            request.exchangeCopy.offerType = 'Ninguna'
            request.exchangeCopy.user = user
            request.exchangeCopy.put()
            request.delete()

        values = {
            'user'        : user,
            'logoutUri'   : users.create_logout_url('/'),
            'copies'      : Copy.allCopiesWithRequests(user),
            'avatar'      : avatarImg
        }
        self.response.out.write(template.render('html/profileOffers.html', values))


class AppliantCopiesView(UserView):
    def get_as_user(self, user, logoutUri, avatarImg):
        title = self.request.get('selectedCopyTitle')
        book = Book.all().filter('title =',title).get()
        selectedCopy = Copy.all().filter('user =',user).filter('book =',book).get()
        appliantUser = users.User(self.request.get('appliant'))
        request = Request.all().filter('copy =', selectedCopy).filter('user =', appliantUser).get()

        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'avatar'     : avatarImg,
            'copies'      : Copy.allCopiesWithRequests(user),
            'selectedCopy': selectedCopy,
            'copyOffers'  : Request.allRequestsFor(selectedCopy),
            'appliantUser' : appliantUser,
            'appliantCopies' : Copy.allCopiesOf(appliantUser),
            'request' : request
        }
        self.response.out.write(template.render('html/appliantCopies.html', values))

    def post_as_user(self, user, logoutUri, avatarImg):
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
            wantedBook = Book.all().filter('title =', self.request.get('appliantCopiesRadios')).get()
            wantedCopy = Copy.all().filter('user =', appliantUser).filter('book =', wantedBook).get()

            request.exchangeCopy = wantedCopy
            request.state = 'Negociando'
            request.exchangeType='Directo'
            request.put()

            selectedCopy.offerState='Esperando confirmacion'
            selectedCopy.put()

        values = {
            'user'       : user,
            'logoutUri'  : users.create_logout_url('/'),
            'copies'      : Copy.allCopiesWithRequests(user),
            'selectedCopy': selectedCopy,
            'copyOffers'  : Request.allRequestsFor(selectedCopy),
            'avatar'      : avatarImg
        }
        self.response.out.write(template.render('html/copyOffers.html', values))

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
