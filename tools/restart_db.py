
from google.appengine.ext import db
from google.appengine.api import users
from models import *

testUser   = users.User(email='test@example.com')
nilsenUser = users.User(email='nilsen@example.com')
billyUser  = users.User(email='billy@gates.com')
userUser   = users.User(email='user@example.com')
lolUser    = users.User(email='lol@example.com')

db.delete(Book.all().fetch(512))
justinBook = Book(title=u'Justin Bieber: mi historia', author=u'Justin Bieber y Mar�a Jos� Espinoza Saavedra',genre=u'Novela').put()
mistBook   = Book(title=u'The Mist', author=u'Stephen King',genre=u'Novela').put()
kafkaBook  = Book(title=u'Kafka en la orilla', author=u'Haruki Murakami',genre=u'Novela').put()
cienBook   = Book(title=u'Cien a�os de soledad', author=u'Gabriel Garc�a M�rquez',genre=u'Novela').put()
akiraBook  = Book(title=u'Akira', author=u'Katsuhiro Otomo',genre=u'Novela').put()
panBook    = Book(title=u'Pan', author=u'Knut Hamsun',genre=u'Novela').put()
jtBook     = Book(title=u'Canci�n de hielo y fuego 1: Juego de tronos', author=u'George R.R. Martin',genre=u'Novela').put()


db.delete(Copy.all().fetch(512))
justinCopy1 = Copy(user=testUser, book=justinBook, offerType="Intercambio", offerState="Con solicitud",language="Frances",pages=250,edition=8,genre="Novela").put()
mistCopy1  = Copy(user=testUser, book=mistBook, offerType="Intercambio", offerState="Con solicitud",language="Frances",pages=200,edition=4,genre="Novela").put()
kafkaCopy1  = Copy(user=testUser, book=kafkaBook, offerType="Venta", offerState="En oferta",language="Ingles",pages=550,edition=9,genre="Novela").put()
cienCopy1 = Copy(user=testUser, book=cienBook, offerType="Venta", offerState="Con solicitud",language="Frances",pages=255,edition=6,genre="Novela").put()
akiraCopy1  = Copy(user=testUser, book=akiraBook, offerType="Venta", offerState="Con solicitud",language="Frances",pages=320,edition=8,genre="Novela").put()
panCopy1    = Copy(user=testUser, book=panBook, offerType="Prestamo",offerState="Con solicitud",language="Frances",pages=220,edition=5,genre="Novela").put()
jtCopy1    = Copy(user=testUser, book=jtBook, offerType="Prestamo",offerState="Con solicitud",language="Frances",pages=250,edition=1,genre="Novela").put()
justinCopy2 = Copy(user=nilsenUser, book=justinBook, offerType="Ninguna").put()
kafkaCopy2  = Copy(user=nilsenUser, book=kafkaBook, offerType="Ninguna").put()
panCopy2    = Copy(user=nilsenUser, book=panBook, offerType="Intercambio").put()


db.delete(Request.all().fetch(512))
Request(user=nilsenUser,copy=justinCopy1, state="Sin contestar").put()
Request(user=billyUser,copy=justinCopy1, state="Sin contestar").put()
Request(user=lolUser,copy=justinCopy1, state="Sin contestar").put()

Request(user=nilsenUser,copy=cienCopy1, state="Sin contestar").put()
Request(user=billyUser,copy=cienCopy1, state="Sin contestar").put()
Request(user=lolUser,copy=cienCopy1, state="Sin contestar").put()

Request(user=nilsenUser,copy=akiraCopy1, state="Sin contestar").put()
Request(user=billyUser,copy=akiraCopy1, state="Sin contestar").put()
Request(user=lolUser,copy=akiraCopy1, state="Sin contestar").put()

Request(user=nilsenUser,copy=panCopy1, state="Sin contestar").put()
Request(user=billyUser,copy=panCopy1, state="Sin contestar").put()
Request(user=lolUser,copy=panCopy1, state="Sin contestar").put()

Request(user=nilsenUser,copy=jtCopy1, state="Sin contestar").put()
Request(user=billyUser,copy=jtCopy1, state="Sin contestar").put()
Request(user=lolUser,copy=jtCopy1, state="Sin contestar").put()

Request(user=nilsenUser,copy=mistCopy1, state="Sin contestar").put()

db.delete(Loan.all().fetch(512))
db.delete(Exchange.all().fetch(512))
db.delete(Sale.all().fetch(512))