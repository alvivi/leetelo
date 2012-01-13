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
        return cls.all().filter('user =', user).filter('offerState !=', 'En oferta').filter('offerState !=', 'No disponible').fetch(128)

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
