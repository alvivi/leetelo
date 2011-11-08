
from google.appengine.ext import db
from google.appengine.api import users
from models import *

testUser   = users.User(email='test@example.com')
nilsenUser = users.User(email='nilsen@example.com')
billyUser  = users.User(email='billy@gates.com')
userUser   = users.User(email='user@example.com')
lolUser    = users.User(email='lol@example.com')

db.delete(Book.all().fetch(512))
justinBook = Book(title=u'Justin Bieber: mi historia', author=u'Justin Bieber y María José Espinoza Saavedra').put()
mistBook   = Book(title=u'The Mist', author=u'Stephen King').put()
kafkaBook  = Book(title=u'Kafka en la orilla', author=u'Haruki Murakami').put()
cienBook   = Book(title=u'Cien años de soledad', author=u'Gabriel García Márquez').put()
akiraBook  = Book(title=u'Akira', author=u'Katsuhiro Otomo').put()
panBook    = Book(title=u'Pan', author=u'Knut Hamsun').put()
jtBook     = Book(title=u'Canción de hielo y fuego 1: Juego de tronos', author=u'George R.R. Martin').put()


db.delete(Copy.all().fetch(512))
justinCopy1 = Copy(user=testUser, book=justinBook, offerType="Intercambio", offerState="Con solicitud").put()
kafkaCopy1  = Copy(user=testUser, book=kafkaBook, offerType="Venta", offerState="Con solicitud").put()
mistCopy1  = Copy(user=testUser, book=mistBook, offerType="Intercambio", offerState="Esperando recepcion").put()
kafkaCopy1    = Copy(user=testUser, book=kafkaBook, offerType="Intercambio",offerState="En oferta").put()
cienCopy1 = Copy(user=testUser, book=cienBook, offerType="Venta", offerState="Esperando recepcion").put()
akiraCopy1  = Copy(user=testUser, book=akiraBook, offerType="Venta", offerState="Con solicitud").put()
panCopy1    = Copy(user=testUser, book=panBook, offerType="Prestamo",offerState="Con solicitud").put()
jtCopy1    = Copy(user=testUser, book=jtBook, offerType="Prestamo",offerState="Esperando recepcion").put()
justinCopy2 = Copy(user=nilsenUser, book=justinBook, offerType="Ninguno").put()
kafkaCopy2  = Copy(user=nilsenUser, book=kafkaBook, offerType="Ninguno").put()
panCopy2    = Copy(user=nilsenUser, book=panBook, offerType="Intercambio").put()
cienCopy1   = Copy(user=billyUser, book=cienBook, offerType="Intercambio").put()
akiraCopy1  = Copy(user=userUser, book=akiraBook, offerType="Intercambio").put()
cienCopy2   = Copy(user=billyUser, book=cienBook, offerType="Intercambio").put()
akiraCopy2  = Copy(user=userUser, book=akiraBook, offerType="Intercambio").put()


db.delete(Request.all().fetch(512))
Request(user=nilsenUser,copy=justinCopy1, state="Sin contestar").put()
Request(user=billyUser,copy=justinCopy1, state="Negociando").put()
Request(user=nilsenUser,copy=kafkaCopy1, state="Sin contestar").put()
Request(user=billyUser,copy=justinCopy1, state="Sin contestar").put()
Request(user=lolUser,copy=justinCopy1, state="Sin contestar").put()

Request(user=nilsenUser,copy=akiraCopy1, state="Sin contestar").put()
Request(user=billyUser,copy=akiraCopy1, state="Sin contestar").put()
Request(user=lolUser,copy=akiraCopy1, state="Sin contestar").put()

Request(user=nilsenUser,copy=panCopy1, state="Sin contestar").put()
Request(user=billyUser,copy=panCopy1, state="Sin contestar").put()
Request(user=testUser,copy=panCopy2, state="Sin contestar").put()
Request(user=testUser,copy=cienCopy1, state="Sin contestar").put()
Request(user=testUser,copy=akiraCopy1, state="Sin contestar").put()
Request(user=lolUser,copy=panCopy1, state="Sin contestar").put()

Request(user=nilsenUser,copy=cienCopy1, state="Aceptada").put()
Request(user=nilsenUser,copy=jtCopy1, state="Aceptada").put()
Request(user=nilsenUser,copy=mistCopy1, state="Aceptada", exchangeCopy=justinCopy2, exchangeType="Directo").put()
Request(user=testUser,copy=akiraCopy2, state="Sin contestar").put()
Request(user=testUser,copy=cienCopy2, state="Sin contestar").put()