
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
Copy(user=testUser, book=justinBook).put()
Copy(user=testUser, book=kafkaBook).put()
Copy(user=testUser, book=panBook).put()
Copy(user=nilsenUser, book=justinBook).put()
Copy(user=nilsenUser, book=kafkaBook).put()
Copy(user=nilsenUser, book=panBook).put()
Copy(user=billyUser, book=cienBook).put()
Copy(user=billyUser, book=cienBook).put()
Copy(user=userUser, book=akiraBook).put()

db.delete(Application.all().fetch(512))
Application(book=cienBook, userWants=testUser, userHas=nilsenUser).put()
Application(book=akiraBook, userWants=testUser, userHas=nilsenUser).put()
Application(book=mistBook, userWants=nilsenUser, userHas=testUser).put()
Application(book=jtBook, userWants=nilsenUser, userHas=testUser).put()
Application(book=akiraBook, userWants=lolUser, userHas=userUser).put()