
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
nansenBook = Book(title=u'Hacia el polo. Relato de la expedici�n del Fram de 1893 a 1896.', author=u'Fridtjof Nansen',genre=u'Aventuras', year=1898, image=db.Link('http://ecx.images-amazon.com/images/I/41a79DegDuL._SS400_.jpg')).put()
vasiliBook = Book(title=u'Vida y Destino', author=u'Vasili Grossman',genre=u'Novela', year=1992, image=db.Link('http://ecx.images-amazon.com/images/I/51yjW-RGG8L._SL500_AA240_.jpg')).put()
beevorBook = Book(title=u'Berl�n. La ca�da: 1945', author=u'Anthony Beevor',genre=u'Hist�rico', year=2002, image=db.Link('http://ecx.images-amazon.com/images/I/5123tJLTXXL._SL500_AA240_.jpg')).put()
krohgBook = Book(title=u'Albertine', author=u'Christian Krohg',genre=u'Novela', year=1886, image=db.Link('http://www.gyldendal.no/var/ezwebin_site/storage/images/gyldendal/videregaaende/studieforberedende-og-fellesfag/tilleggslitteratur/albertine/401110-3-nor-NO/Albertine_productimage.jpg')).put()
franzBook = Book(title=u'La Metamorfosis', author=u'Franz Kafka',genre=u'Novela', year=1916, image=db.Link('http://ecx.images-amazon.com/images/I/51u8ROM1UVL._SL500_AA240_.jpg')).put()
zeppelinBook = Book(title=u'El Martillo de los Dioses', author=u'Stephen Davis',genre=u'Biograf�a', year=1985, image=db.Link('http://ecx.images-amazon.com/images/I/51Hyq1G6NbL._SL500_AA240_.jpg')).put()
nerudaBook = Book(title=u'Veinte Poemas de Amor y una canci�n desesperada', author=u'Pablo Neruda',genre=u'Poes�a', year=1920, image=db.Link('http://ecx.images-amazon.com/images/I/41sgNu8ZQxL._SL500_AA240_.jpg')).put()
aleixandreBook = Book(title=u'Poesias Completas', author=u'Vicente Aleixandre',genre=u'Poes�a', year=2001, image=db.Link('http://ecx.images-amazon.com/images/I/41ukWMygI-L._SL500_AA240_.jpg')).put()
lorcaBook = Book(title=u'Bodas de Sangre', author=u'Federico Garc�a Lorca',genre=u'Poes�a', year=1933, image=db.Link('http://ecx.images-amazon.com/images/I/31mDUO0psIL._SL500_AA240_.jpg')).put()
coronelBook = Book(title=u'El Coronel no tiene quien le escriba', author=u'Gabriel Garc�a M�rquez',genre=u'Novela', year=1961, image=db.Link('http://ecx.images-amazon.com/images/I/41Y6EsHIUSL._SL500_AA240_.jpg')).put()
esclavaBook = Book(title=u'La Isla bajo el Mar', author=u'Isabel Allende',genre=u'Novela', year=2009, image=db.Link('http://ecx.images-amazon.com/images/I/41peJahqUNL._SL500_AA240_.jpg')).put()
stalingradoBook = Book(title=u'Stalingrado', author=u'Anthony Beevor',genre=u'Hist�rico', year=1998, image=db.Link('http://ecx.images-amazon.com/images/I/11F68Y4TQHL._SL500_AA240_.jpg')).put()
civBook = Book(title=u'La Civilizaci�n Romana', author=u'Pierre Grimal',genre=u'Hist�rico', year=2003, image=db.Link('http://ecx.images-amazon.com/images/I/51Zts5pWQiL._SL500_AA240_.jpg')).put()
decadenBook = Book(title=u'Historia de la decadencia y ca�da del imperio romano', author=u'Edward Gibbon',genre=u'Hist�rico', year=2003, image=db.Link('http://ecx.images-amazon.com/images/I/510povnCJ0L._SL500_AA240_.jpg')).put()
mesopBook = Book(title=u'Mesopotamia: Asirios, sumerios y babilonios', author=u'Enrico Ascalone',genre=u'Hist�rico', year=2006, image=db.Link('http://ecx.images-amazon.com/images/I/41-W3cYN4rL._SL500_AA240_.jpg')).put()
rivertonBook = Book(title=u'La casa de Riverton', author=u'Kate Morton',genre=u'Rom�ntico', year=2008, image=db.Link('http://ecx.images-amazon.com/images/I/51ROn1gUmNL._SL500_AA240_.jpg')).put()
cieloBook = Book(title=u'Tres metros sobre el cielo', author=u'Federico Moccia',genre=u'Rom�ntico', year=2006, image=db.Link('http://ecx.images-amazon.com/images/I/511TxpLpVYL._SL500_AA240_.jpg')).put()
austenBook = Book(title=u'Orgullo y Prejuicio', author=u'Jane Austen',genre=u'Rom�ntico', year=1810, image=db.Link('http://ecx.images-amazon.com/images/I/513SR9ZPHBL._SL500_AA240_.jpg')).put()
deseoBook = Book(title=u'Deseo y Enga�o', author=u'Nicole Jordan',genre=u'Rom�ntico', year=2008, image=db.Link('http://ecx.images-amazon.com/images/I/51cxReM6ETL._SL500_AA240_.jpg')).put()
tokyoBook = Book(title=u'Tokyo Blues(Norwegian wood)', author=u'Haruki Murakami',genre=u'Rom�ntico', year=2007, image=db.Link('http://www.labitacoradeltigre.com/edu-images/tokio_blues.jpg')).put()
quienBook = Book(title=u'�Quien te lo ha contado?', author=u'Marian Keyes',genre=u'Rom�ntico', year=2003, image=db.Link('http://ecx.images-amazon.com/images/I/411BFxU58pL._SL500_AA240_.jpg')).put()

db.delete(Copy.all().fetch(512))
justinCopy1 = Copy(user=testUser, book=justinBook, offerType="Intercambio", offerState="Con solicitud",language="Frances",pages=250,edition=8).put()
mistCopy1  = Copy(user=nilsenUser, book=mistBook, offerType="Intercambio", offerState="Con solicitud",language="Frances",pages=200,edition=4,genre="Novela").put()
kafkaCopy1  = Copy(user=testUser, book=kafkaBook, offerType="Venta", offerState="Con solicitud",language="Ingles",pages=550,edition=9,genre="Novela").put()
cienCopy1 = Copy(user=nilsenUser, book=cienBook, offerType="Venta", offerState="Con solicitud",language="Frances",pages=255,edition=6,genre="Novela").put()
panCopy1    = Copy(user=testUser, book=panBook, offerType="Prestamo",offerState="Con solicitud",language="Frances",pages=220,edition=5,genre="Novela").put()
jtCopy1    = Copy(user=nilsenUser, book=jtBook, offerType="Prestamo",offerState="Con solicitud",language="Frances",pages=250,edition=1,genre="Novela").put()
nansenCopy1 = Copy(user=testUser, book=nansenBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=457,edition=8,genre="Novela").put()
vasiliCopy1 = Copy(user=testUser, book=vasiliBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=1098,edition=8,genre="Novela").put()
beevorCopy1 = Copy(user=testUser, book=beevorBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=896,edition=8,genre="Novela").put()
krohgCopy1 = Copy(user=testUser, book=krohgBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=250,edition=8,genre="Novela").put()
franzCopy1 = Copy(user=testUser, book=franzBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=356,edition=8,genre="Novela").put()
zeppelinCopy1 = Copy(user=testUser, book=zeppelinBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=250,edition=8,genre="Novela").put()
nerudaCopy1 = Copy(user=testUser, book=nerudaBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=35,edition=8,genre="Novela").put()
aleixandreCopy1 = Copy(user=testUser, book=aleixandreBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=735,edition=8,genre="Novela").put()
lorcaCopy1 = Copy(user=testUser, book=lorcaBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=135,edition=8,genre="Novela").put()
coronelCopy1 = Copy(user=testUser, book=coronelBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=335,edition=8,genre="Novela").put()
esclavaCopy1 = Copy(user=testUser, book=esclavaBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=447,edition=8,genre="Novela").put()
stalingradoCopy1 = Copy(user=testUser, book=stalingradoBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=735,edition=8,genre="Novela").put()
civCopy1 = Copy(user=testUser, book=civBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=441,edition=8,genre="Novela").put()
decadenCopy1 = Copy(user=testUser, book=decadenBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=435,edition=8,genre="Novela").put()
mesopCopy1 = Copy(user=testUser, book=mesopBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=335,edition=8,genre="Novela").put()
rivertonCopy1 = Copy(user=testUser, book=rivertonBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=457,edition=8,genre="Novela").put()


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

db.delete(Club.all().fetch(512))
club1 = Club(name=u'aficionados de Justin',description=u'Este club es una prueba', author=u'Justin Bieber'
, genre= [u'Poesia',u'Ciencia Ficcion'],invitaciones = [u'user@example.com',u'lol@example.com'],state=u'Habilitado', book=justinBook,owner = testUser).put()
club2 = Club(name=u'Tres metros sobre el cielo',description=u'Este club va dirigido a los fans de...', author=u'Federico Moccia', genre= [u'Poesia',u'Novela'],invitaciones = [u'nilsen@example.com',u'billy@gates.com'],state=u'Deshabilitado', book=cieloBook, owner = testUser).put()
club3 = Club(name=u'fans de Haruki Murakami',description=u'Este club va dirigido a los fans de...', author=u'Haruki Murakami', genre= [u'Poesia',u'Novela'],invitaciones = [u'patriciapons89@gmail.com',u'billy@gates.com'],state=u'Habilitado', book=cieloBook, owner= testUser).put()


