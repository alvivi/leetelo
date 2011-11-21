
from google.appengine.ext import db
from google.appengine.api import users
from models import *

testUser   = users.User(email='test@example.com')
nilsenUser = users.User(email='nilsen@example.com')
billyUser  = users.User(email='billy@gates.com')
userUser   = users.User(email='user@example.com')
lolUser    = users.User(email='lol@example.com')
patryUser = users.User(email='patriciapons89@gmail.com')

db.delete(Book.all().fetch(512))
justinBook = Book(title=u'Justin Bieber: mi historia', author=u'Justin Bieber',genre=u'Biograf�a', year=2011, image=db.Link('http://img9.planetadelibros.com/usuaris/libros/fotos/49/tam_1/48669_1_JUSTINBIEBER.jpg')).put()
mistBook   = Book(title=u'The Mist', author=u'Stephen King',genre=u'Novela', year=1983, image=db.Link('http://ecx.images-amazon.com/images/I/41ZOgg%2BT6gL._SL500_AA240_.jpg')).put()
kafkaBook  = Book(title=u'Kafka en la orilla', author=u'Haruki Murakami',genre=u'Novela', year=2008, image=db.Link('http://ecx.images-amazon.com/images/I/31oVN6Jg8RL._SL500_AA240_.jpg')).put()
cienBook   = Book(title=u'Cien a�os de soledad', author=u'Gabriel Garc�a M�rquez',genre=u'Novela', year=2003, image=db.Link('http://ecx.images-amazon.com/images/I/51W4LYaTU%2BL._SL500_AA240_.jpg')).put()
akiraBook  = Book(title=u'Akira', author=u'Katsuhiro Otomo',genre=u'Novela', year=1982, image=db.Link('http://ecx.images-amazon.com/images/I/51PhfWmsbzL._SL500_AA240_.jpg')).put()
panBook    = Book(title=u'Pan', author=u'Knut Hamsun',genre=u'Novela', year=2010, image=db.Link('http://ecx.images-amazon.com/images/I/41gf6VVjVcL._SL500_AA240_.jpg')).put()
jtBook     = Book(title=u'Canci�n de hielo y fuego 1: Juego de tronos', author=u'George R.R. Martin',genre=u'Novela', year=1991, image=db.Link('http://ecx.images-amazon.com/images/I/21EScU0DCEL._SL500_AA240_.jpg')).put()


db.delete(Copy.all().fetch(512))
justinCopy1 = Copy(user=testUser, book=justinBook, offerType="Intercambio", offerState="Con solicitud",language="Frances",pages=250,edition=8,genre="Novela").put()
mistCopy1  = Copy(user=nilsenUser, book=mistBook, offerType="Intercambio", offerState="Con solicitud",language="Frances",pages=200,edition=4,genre="Novela").put()
kafkaCopy1  = Copy(user=testUser, book=kafkaBook, offerType="Venta", offerState="Con solicitud",language="Ingles",pages=550,edition=9,genre="Novela").put()
cienCopy1 = Copy(user=nilsenUser, book=cienBook, offerType="Venta", offerState="Con solicitud",language="Frances",pages=255,edition=6,genre="Novela").put()
panCopy1    = Copy(user=testUser, book=panBook, offerType="Prestamo",offerState="Con solicitud",language="Frances",pages=220,edition=5,genre="Novela").put()
jtCopy1    = Copy(user=nilsenUser, book=jtBook, offerType="Prestamo",offerState="Con solicitud",language="Frances",pages=250,edition=1,genre="Novela").put()



db.delete(Request.all().fetch(512))
Request(user=nilsenUser,copy=justinCopy1, state="Sin contestar").put()
Request(user=billyUser,copy=justinCopy1, state="Sin contestar").put()
Request(user=lolUser,copy=justinCopy1, state="Sin contestar").put()

Request(user=nilsenUser,copy=kafkaCopy1, state="Sin contestar").put()
Request(user=billyUser,copy=kafkaCopy1, state="Sin contestar").put()
Request(user=lolUser,copy=kafkaCopy1, state="Sin contestar").put()

Request(user=nilsenUser,copy=panCopy1, state="Sin contestar").put()
Request(user=billyUser,copy=panCopy1, state="Sin contestar").put()
Request(user=lolUser,copy=panCopy1, state="Sin contestar").put()



db.delete(Loan.all().fetch(512))
db.delete(Exchange.all().fetch(512))
db.delete(Sale.all().fetch(512))
