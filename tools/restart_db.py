
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
justinCopy1 = Copy(user=testUser, book=justinBook, offerState="Con solicitud").put()
kafkaCopy1  = Copy(user=testUser, book=kafkaBook, offerState="Con solicitud").put()
panCopy1    = Copy(user=testUser, book=panBook).put()
justinCopy2 = Copy(user=nilsenUser, book=justinBook).put()
kafkaCopy2  = Copy(user=nilsenUser, book=kafkaBook).put()
panCopy2    = Copy(user=nilsenUser, book=panBook).put()
cienCopy1   = Copy(user=billyUser, book=cienBook).put()
akiraCopy1  = Copy(user=userUser, book=akiraBook).put()


db.delete(Request.all().fetch(512))
Request(user=nilsenUser,copy=justinCopy1).put()
Request(user=billyUser,copy=justinCopy1).put()
Request(user=nilsenUser,copy=kafkaCopy1).put()

