# -*- coding: utf-8 -*-

# En este fichero se define toda la lógica de aplicación. Las instancias de los
# modelos son persistentes.

from google.appengine.ext import db


# Ficha del libro, la obra en sí
class Book(db.Model):
    title  = db.StringProperty(required=True)
    author = db.StringProperty()
    genre = db.StringProperty(choices=set(["Novela","Aventuras","Poesía","Narrativa","Histórico","Ciencia Ficción","Romántico","Ensayo"]))
    year = db.StringProperty()
    
# El ejemplar del libro
class Copy(db.Model):
    book = db.ReferenceProperty(Book)
    user = db.UserProperty()
    copyState = db.StringProperty(choices=set(["Excelente","Bueno","Deteriorado","Muy viejo"]))
    offerState = db.StringProperty(choices=set(["No disponible","En oferta",
                                                "Con solicitud","Esperando confirmacion",
                                                "Esperando recepción", "Prestado",
                                                "Intercambiado","Vendido"]))
    pages = db.IntegerProperty()
    edition = db.IntegerProperty()
    language = db.StringProperty()
    format = db.StringProperty(choices=set(["Bolsillo","Tapa dura","Tapa blanda","Coleccionista"]))
    publishing = db.StringProperty()
    limitOfferDate = db.DateProperty()
    salePrice = db.FloatProperty()
    offerType = db.StringProperty(choices=set(["Intercambio","Venta","Prestamo","Ninguno"]))
    # Método de clase que devuelve todos los ejemplares que posee un usuario
    @classmethod
    def allCopiesOf(cls, user):
        return cls.all().filter('user =', user).fetch(128)
    # Método de clase que devuelve todos los ejemplares que posee un usuario que están en oferta y tienen alguna solicitud
    @classmethod
    def allCopiesWithRequests(cls, user):
        return cls.all().filter('user =', user).filter('offerState =', "Con solicitud").fetch(128) + cls.all().filter('user =', user).filter('offerState =', "Esperando confirmacion").fetch(128) + cls.all().filter('user =', user).filter('offerState =', "Esperando recepcion").fetch(128) + cls.all().filter('user =', user).filter('offerState =', "Prestado").fetch(128)
        

# Solicitud sobre un libro
class Request(db.Model):
    copy = db.ReferenceProperty(Copy)
    user = db.UserProperty()
    state = db.StringProperty(choices=set(["Sin contestar","Negociando","Aceptada","Rechazada"]))
    # Método de clase que devuelve todas las solicitudes que ha realizado un usuario
    @classmethod
    def allRequestsOf(cls, user):
        return cls.all().filter('user =', user).fetch(128)
    
    # Método de clase que devuelve todas las solicitudes que se han recibido sobre un libro
    @classmethod
    def allRequestsFor(cls, copy):
        return cls.all().filter('copy =', copy).fetch(128)
    
