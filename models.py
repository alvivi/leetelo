# -*- coding: utf-8 -*-

# En este fichero se define toda la lógica de aplicación. Las instancias de los
# modelos son persistentes.

from google.appengine.ext import db


# Ficha del libro, la obra en sí
class Book(db.Model):
    title  = db.StringProperty(required=True)
    author = db.StringProperty()


# El ejemplar del libro
class Copy(db.Model):
    book = db.ReferenceProperty(Book)
    user = db.UserProperty()

    # Método de clase que devuelve todos los ejemplares que posee un usuario
    @classmethod
    def allCopiesOf(cls, user):
        return cls.all().filter('user =', user).fetch(64)

