# -*- coding: utf-8 -*-

# En este fichero se define toda la lógica de aplicación. Las instancias de los
# modelos son persistentes.

from google.appengine.ext import db

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
        return cls.all().filter('user =', user).filter('offerState !=', 'En oferta').fetch(128) + cls.all().filter('user !=', user).filter('offerState =', 'No disponible').fetch(128)

# Comentarios
class Comment(db.Model):
    text = db.StringProperty(required=True)
    user = db.UserProperty()
    date = db.DateProperty(auto_now=True)

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
    exchangeCopy = db.ReferenceProperty(Copy,collection_name='exchange_copy')
    user = db.UserProperty()
    state = db.StringProperty(choices=set(['Sin contestar','Negociando','Aceptada','Rechazada']))
    exchangeType = db.StringProperty(choices=set(['Directo','Indirecto']))
    llegaCopia1 = db.BooleanProperty()
    llegaCopia2 = db.BooleanProperty()
    # Método de clase que devuelve todas las solicitudes que ha realizado un usuario
    @classmethod
    def allRequestsOf(cls, user):
        return cls.all().filter('user =', user).fetch(128)

    # Método de clase que devuelve todas las solicitudes que se han recibido sobre un libro
    @classmethod
    def allRequestsFor(cls, copy):
        return cls.all().filter('copy =', copy).fetch(128)

class Sale(db.Model):
    copy = db.ReferenceProperty(Copy)
    vendor = db.UserProperty()
    buyer = db.UserProperty()
    date = db.DateProperty(auto_now=True)

class Loan(db.Model):
    copy = db.ReferenceProperty(Copy)
    owner = db.UserProperty()
    lendingTo = db.UserProperty()
    arrivalDate = db.DateProperty()
    returningDate = db.DateProperty()

class Exchange(db.Model):
    copy1 = db.ReferenceProperty(Copy,collection_name='copy1')
    owner1 = db.UserProperty()
    copy2 = db.ReferenceProperty(Copy,collection_name='copy2')
    owner2 = db.UserProperty()
    exchangeDate = db.DateProperty(auto_now=True)
    exchangeType = db.StringProperty(choices=set(['Directo','Indirecto']))

    @classmethod
    def allExchangesFromUser(cls, user):
        return cls.all().filter('owner2', user).fetch(128)

    @classmethod
    def switchFor(cls, copy, user):
        return cls.all().filter('copy1 =', copy).filter('copy2.user =', user).fetch(128)

    @classmethod
    def getDirectExchange(cls, copy1, owner1, copy2, owner2):
        return cls.all().filter('copy1 =',copy1).filter('copy2 =',copy2).filter('owner1 =', owner1).filter('owner2 =',owner2).filter('exchangeType =','Directo').fetch(128)

