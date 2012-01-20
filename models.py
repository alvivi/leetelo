# -*- coding: utf-8 -*-

# En este fichero se define toda la lógica de aplicación. Las instancias de los
# modelos son persistentes.

from google.appengine.ext import db
import datetime

class Usuario(db.Model):
    user = db.UserProperty()

class UserAvatar(db.Model):
    user = db.UserProperty()
    avatar = db.BlobProperty()

# Ficha del libro, la obra en sí
class Book(db.Model):
    author = db.StringProperty()
    genre  = db.StringProperty(choices=set([u'Aventuras', u'Biografía', u'Ciencia Ficción', u'Ensayo', u'Histórico', u'Narrativa', u'Novela', u'Poesía', u'Romántico']))
    image  = db.LinkProperty()
    title  = db.StringProperty(required=True)
    year   = db.IntegerProperty()

# El ejemplar del libro
class Copy(db.Model):
    book = db.ReferenceProperty(Book)
    user = db.UserProperty()
    copyState = db.StringProperty(choices=set(['Excelente','Bueno','Deteriorado','Muy viejo']))
    offerState = db.StringProperty(choices=set(['No disponible','Disponible','En oferta',
                                                'Con solicitud','Esperando confirmacion',
                                                'Esperando recepcion', 'Prestado',
                                                'Intercambiado','Vendido']))

    pages = db.IntegerProperty()
    edition = db.IntegerProperty()
    language = db.StringProperty()
    format = db.StringProperty(choices=set(['Bolsillo','Tapa dura','Tapa blanda','Coleccionista']))
    publishing = db.StringProperty()
    limitOfferDate = db.DateProperty()
    alertActivated = db.BooleanProperty() # flag para saber si se ha creado la alerta de limite de oferta excedido o no
    salePrice = db.FloatProperty()
    offerType = db.StringProperty(choices=set(['Intercambio','Venta','Prestamo','Ninguna']))
    # Método de clase que devuelve todos los ejemplares que posee un usuario
    @classmethod
    def allCopiesOf(cls, user):
        return cls.all().filter('user =', user).fetch(128)
    # Método de clase que devuelve todos los ejemplares que posee un usuario que están en oferta y tienen alguna solicitud
    @classmethod
    def allCopiesWithRequests(cls, user):
        #return cls.all().filter('user =', user).filter('offerState =', 'Con solicitud').fetch(128) + cls.all().filter('user =', user).filter('offerState =', 'Esperando confirmacion').fetch(128) + cls.all().filter('user =', user).filter('offerState =', 'Esperando recepcion').fetch(128) + cls.all().filter('user =', user).filter('offerState =', 'Prestado').fetch(128)
        return cls.all().filter('user =', user).filter('offerState !=', 'En oferta').filter('offerState !=', 'No disponible').fetch(128)

    @classmethod
    def allOfferredCopiesOf(cls, user):
        return cls.all().filter('user =', user).filter('offerState =', 'En oferta').fetch(128)

# Comentarios
class Comment(db.Model):
    text = db.StringProperty(required=True)
    user = db.UserProperty()
    date = db.DateTimeProperty(auto_now=True)

class BookComment(db.Model):
    book = db.ReferenceProperty(Book)
    comment = db.ReferenceProperty(Comment)

class UserComment(db.Model):
    user = db.UserProperty()
    comment = db.ReferenceProperty(Comment)
    @classmethod
    def allCommentsFor(cls, user):
        return cls.all().filter('user =', user).fetch(128)

# Ficha del Club
class Club(db.Model):
    image  = db.LinkProperty()
    name  = db.StringProperty(required=True)
    description = db.StringProperty()
    author = db.StringProperty()
    genre  = db.StringListProperty()
    book = db.ReferenceProperty(Book)
    owner = db.UserProperty()
    state = db.StringProperty(choices=set(['Habilitado','Deshabilitado']))
    invitaciones= db.StringListProperty()

class ClubComment(db.Model):
    club = db.ReferenceProperty(Club)
    comment = db.ReferenceProperty(Comment)

class ClubEvent(db.Model):
    club = db.ReferenceProperty(Club)
    name = db.StringProperty()
    place = db.StringProperty()
    comment = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def allOf(cls, club):
        return cls.all().filter('club =', club).filter('date <=', datetime.datetime.now()).fetch(128)

class ClubEventAssit(db.Model):
    event = db.ReferenceProperty(ClubEvent)
    user = db.UserProperty();

    @classmethod
    def allOf(cls, event):
         return cls.all().filter('event =', event).fetch(128)

    @classmethod
    def amINotIn(cls, event, user):
         return cls.all().filter('event =', event).filter('user =', user).count() == 0

#relacion usuarios - clubs
class Club_User(db.Model):
    user = db.UserProperty()
    club = db.ReferenceProperty(Club)
    state = db.StringProperty(choices=set(['Propietario', 'Solicitado', 'Solicitud Aceptada', 'Solicitud Rechazada', 'Invitado', 'Invitacion Aceptada', 'Invitacion Rechazada']))

    @classmethod
    def allParticipantsOf(cls, club):
        return cls.all().filter('club =', club).fetch(128)
    @classmethod
    def clubsForUser(cls, user):
	return cls.all().filter('user =', user).filter('state =','Invitacion Aceptada').fetch(128) + cls.all().filter('user =', user).filter('state =','Solicitud Aceptada').fetch(128) + cls.all().filter('user =', user).filter('state =','Propietario').fetch(128)

# Solicitud sobre un libro
class Request(db.Model):
    copy = db.ReferenceProperty(Copy,collection_name='owner_copy')
    user = db.UserProperty()
    state = db.StringProperty(choices=set(['Sin contestar','Negociando','Aceptada','Rechazada']))

    #si copy.offerType es Intercambio, se usan estas dos propiedades para indicar la copia por la que se solicita intercambiar, y si el intercambio es directo o indirecto
    exchangeCopy = db.ReferenceProperty(Copy,collection_name='exchange_copy')
    exchangeType = db.StringProperty(choices=set(['Directo','Indirecto']))

    #estas dos propiedades se usan para la logica de visualizacion (indican cuando ha llegado cada copia a su destino)
    llegaCopia1 = db.BooleanProperty()
    llegaCopia2 = db.BooleanProperty()
    # Método de clase que devuelve todas las solicitudes que ha realizado un usuario
    @classmethod
    def allRequestsOf(cls, user):
        return cls.all().filter('user =', user).fetch(128)

    # Método de clase que devuelve todas las solicitudes que se han recibido sobre un libro
    @classmethod
    def allRequestsFor(cls, copy):
        return cls.all().filter('copy =', copy).filter('state !=','Rechazada').fetch(128)

    @classmethod
    def getNotAnsweredRequest(cls, copy):
        return cls.all().filter('copy =', copy).filter('state =', 'Sin contestar').fetch(128)

class RequestComment(db.Model):
    comment = db.ReferenceProperty(Comment)
    request = db.ReferenceProperty(Request)
    viewed  = db.BooleanProperty(default=False)

    @classmethod
    def notViewedCount(cls, request, user):
        count = 0
        cs = cls.all().filter('request =', request).fetch(128)
        for c in cs:
            if c.comment.user != user and not c.viewed:
                count += 1
        return count

    @classmethod
    def markAllAsViewed(cls, request, user):
        cs = cls.all().filter('request =', request).fetch(128)
        for c in cs:
            if c.comment.user != user and not c.viewed:
                c.viewed = True
                c.put()

    @classmethod
    def allFrom(cls, request):
        return cls.all().filter('request =', request).fetch(128)

class HistoricalRequest(db.Model):
    copy = db.ReferenceProperty(Copy)
    appliant = db.UserProperty()
    initialUser = db.UserProperty()
    initialOfferType = db.StringProperty(choices=set(['Intercambio','Venta','Prestamo','Ninguna']))
    state = db.StringProperty(choices=set(['Sin contestar','Negociando','Aceptada','Rechazada']))
    date = db.DateTimeProperty(auto_now=True)

class Transaction(db.Model):
    copy = db.ReferenceProperty(Copy,collection_name='copy')
    owner = db.UserProperty()
    appliant = db.UserProperty()
    transactionType = db.StringProperty(choices=set(['Intercambio','Venta','Prestamo']))
    #si se trata de intercambio directo, tendrá "appliantCopy"
    appliantCopy = db.ReferenceProperty(Copy,collection_name='appliantCopy')
    exchangeType = db.StringProperty(choices=set(['Directo','Indirecto']))
    #startDate:
    # - prestamo: indica el dia en que el solicitante recibe el libro
    # - venta: indica el dia en que se inicia la venta
    # - intercambio: indica el dia en que se inicia el intercambio
    startDate = db.DateTimeProperty(auto_now=True)
    #endDate:
    # - prestamo: indica el dia en que el propietario recibe el ejemplar de vuelta
    # - venta: indica el dia en que el solicitante recibe el libro
    # - intercambio: indica el dia en que ambos participantes han recibido los libros intercambiados
    endDate = db.DateTimeProperty()

class Alert(db.Model):
    date = db.DateProperty(required=True)
    type = db.StringProperty(choices=set(['Club: Solicitud','Club: Aceptado','Club: Rechazado','Solicitud: Cancelada','Solicitud: Finalizada','Solicitud: Rechazada', 'Solicitud: Aceptada','Club: Invitacion','Nuevo mensaje','Solicitud: Nueva', 'Fecha oferta excedida']))
    description = db.StringProperty()
    user = db.UserProperty(required=True)
    remainder = db.IntegerProperty()
    relatedClub = db.ReferenceProperty(Club)
    #Campo para que la alerta lleve a una pagina de club.

    relatedCopy = db.ReferenceProperty(Copy)
    #Campo para que la alerta lleve a una pagina de ofertas de copia (solo para owners)

    relatedApp = db.StringProperty()
    #Campo para que la alerta lleve a la pagina de applications (normalmente para requesting users)

    @classmethod
    def setDate(today):
	today = datetime.date.today()
	return today

    @classmethod
    def allAlertsOf(result, user):
        alertlist = []
	result = []

	alertlist = Alert.all().filter('user =', user).fetch(512)

	today = datetime.date.today()

	for alert in alertlist:
	    delta = today - alert.date
	    if delta.days < 11:
		alert.remainder = 10 - delta.days
		result.append(alert)
	    else:
		db.delete(alert)

	return result

