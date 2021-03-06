
from google.appengine.ext import db
from google.appengine.api import users
from models import *
import datetime
import urllib



testUser   = users.User(email='test@example.com')
nilsenUser = users.User(email='nilsen@example.com')
billyUser  = users.User(email='billy@gates.com')
userUser   = users.User(email='user@example.com')
lolUser    = users.User(email='lol@example.com')
patryUser  = users.User(email='patrypons@example.com')

db.delete(UserAvatar.all().fetch(512))
UserAvatar(user=testUser,   avatar=db.Blob(urllib.urlopen("http://s3.ryanparman.com/images/blue-avatar.jpg").read())).put()
UserAvatar(user=nilsenUser, avatar=db.Blob(urllib.urlopen("http://lh3.ggpht.com/-xZQnCl3y_nA/TrUEXriz-SI/AAAAAAAAFKk/ObneIl5PWqk/bloggerPlus.jpg").read())).put()
UserAvatar(user=patryUser,  avatar=db.Blob(urllib.urlopen("http://media.comicvine.com/uploads/4/48211/907038-mafalda_icon.jpg").read())).put()
UserAvatar(user=billyUser,  avatar=db.Blob(urllib.urlopen("http://revistafortuna.com.mx/contenido/wp-content/uploads/2011/04/bill-gates-motor.jpg").read())).put()
UserAvatar(user=userUser ,  avatar=db.Blob(urllib.urlopen("http://safopage.files.wordpress.com/2010/04/user.png").read())).put()
UserAvatar(user=lolUser,    avatar=db.Blob(urllib.urlopen("http://images.mirror.co.uk/upl/m4/oct2009/0/9/image-1-for-olympic-history-gallery-553113648.jpg").read())).put()


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
prisioneroBook = Book(title=u'El Prisionero del Cielo', author=u'Carlos Ruiz Zaf�n',genre=u'Novela', year=2010, image=db.Link('http://ecx.images-amazon.com/images/I/51eLBni5-IL._SL500_AA240_.jpg')).put()
imperioBook = Book(title=u'El Imperio eres t�', author=u'Javier Moro',genre=u'Novela', year=2010, image=db.Link('http://ecx.images-amazon.com/images/I/51I5FIliVKL._SL500_AA240_.jpg')).put()
arenaBook = Book(title=u'Tiempo de Arena', author=u'Inma Chac�n',genre=u'Novela', year=2011, image=db.Link('http://ecx.images-amazon.com/images/I/51yM1aYLaoL._SL500_AA240_.jpg')).put()
libertadBook = Book(title=u'Libertad', author=u'Jonathan Franzen',genre=u'Novela', year=2011, image=db.Link('http://ecx.images-amazon.com/images/I/41jYTLPzJoL._SL500_AA240_.jpg')).put()

db.delete(Copy.all().fetch(512))
justinCopy1 = Copy(user=testUser, book=justinBook, offerType="Intercambio", offerState="Con solicitud",language="Frances",pages=250,edition=8).put()
kafkaCopy1  = Copy(user=testUser, book=kafkaBook, offerType="Venta", offerState="Con solicitud",language="Ingles",pages=550,edition=9).put()
panCopy1    = Copy(user=testUser, book=panBook, offerType="Prestamo",offerState="Con solicitud",language="Frances",pages=220,edition=5).put()
nansenCopy1 = Copy(user=testUser, book=nansenBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=457,edition=4).put()
vasiliCopy1 = Copy(user=testUser, book=vasiliBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=1098,edition=2).put()
beevorCopy1 = Copy(user=testUser, book=beevorBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=896,edition=1).put()
krohgCopy1 = Copy(user=testUser, book=krohgBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=250,edition=10).put()
franzCopy1 = Copy(user=testUser, book=franzBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=356,edition=7).put()
zeppelinCopy1 = Copy(user=testUser, book=zeppelinBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=250,edition=3).put()
nerudaCopy1 = Copy(user=testUser, book=nerudaBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=35,edition=3).put()
aleixandreCopy1 = Copy(user=testUser, book=aleixandreBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=735,edition=1).put()
lorcaCopy1 = Copy(user=testUser, book=lorcaBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=135,edition=5).put()
coronelCopy1 = Copy(user=testUser, book=coronelBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=335,edition=6).put()
esclavaCopy1 = Copy(user=testUser, book=esclavaBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=447,edition=4).put()
stalingradoCopy1 = Copy(user=testUser, book=stalingradoBook, offerType="Intercambio", offerState="En oferta",language="Castellano",pages=735,edition=3).put()
civCopy1 = Copy(user=testUser, book=civBook, offerType="Intercambio", offerState="En oferta",language="Castellano",pages=441,edition=2).put()
decadenCopy1 = Copy(user=testUser, book=decadenBook, offerType="Intercambio", offerState="En oferta",language="Castellano",pages=435,edition=2).put()
mesopCopy1 = Copy(user=testUser, book=mesopBook, offerType="Intercambio", offerState="En oferta",language="Castellano",pages=335,edition=8).put()
rivertonCopy1 = Copy(user=testUser, book=rivertonBook, offerType="Intercambio", offerState="En oferta",language="Castellano",pages=457,edition=8).put()

jtCopy1    = Copy(user=nilsenUser, book=jtBook, offerType="Prestamo",offerState="En oferta",language="Frances",pages=250,edition=1).put()
cienCopy1 = Copy(user=nilsenUser, book=cienBook, offerType="Venta", offerState="En oferta",language="Frances",pages=255,edition=6).put()
mistCopy1  = Copy(user=nilsenUser, book=mistBook, offerType="Intercambio", offerState="En oferta",language="Frances",pages=200,edition=4).put()
austenCopy1 = Copy(user=nilsenUser, book=austenBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=457,edition=8).put()
deseoCopy1 = Copy(user=nilsenUser, book=deseoBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=457,edition=5).put()
tokyoCopy1 = Copy(user=nilsenUser, book=tokyoBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=457,edition=9).put()
quienCopy1 = Copy(user=nilsenUser, book=quienBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=457,edition=2).put()
cieloCopy1 = Copy(user=nilsenUser, book=cieloBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=457,edition=1).put()
prisioneroCopy1 = Copy(user=nilsenUser, book=prisioneroBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=457,edition=3).put()
imperioCopy1 = Copy(user=nilsenUser, book=imperioBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=457,edition=3).put()
arenaCopy1 = Copy(user=nilsenUser, book=arenaBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=457,edition=2).put()
libertadCopy1 = Copy(user=nilsenUser, book=libertadBook, offerType="Intercambio", offerState="Con solicitud",language="Castellano",pages=457,edition=7).put()
libertadCopy2 = Copy(user=lolUser, book=libertadBook, offerType="Intercambio", offerState="En oferta",language="Castellano",pages=457,edition=10).put()

db.delete(Request.all().fetch(512))
db.delete(HistoricalRequest.all().fetch(512))
nilsenRequest = Request(user=nilsenUser,copy=justinCopy1, state="Sin contestar").put()
Request(user=billyUser,copy=justinCopy1, state="Sin contestar").put()
Request(user=lolUser,copy=justinCopy1, state="Sin contestar").put()
HistoricalRequest(appliant=nilsenUser, copy=justinCopy1, initialUser=testUser, state="Sin contestar", initialOfferType="Intercambio").put()
HistoricalRequest(appliant=billyUser, copy=justinCopy1, initialUser=testUser, state="Sin contestar", initialOfferType="Intercambio").put()
HistoricalRequest(appliant=lolUser, copy=justinCopy1, initialUser=testUser, state="Sin contestar", initialOfferType="Intercambio").put()

Request(user=nilsenUser,copy=kafkaCopy1, state="Negociando").put()
Request(user=billyUser,copy=kafkaCopy1, state="Sin contestar").put()
Request(user=lolUser,copy=kafkaCopy1, state="Sin contestar").put()
HistoricalRequest(appliant=nilsenUser, copy=kafkaCopy1, initialUser=testUser, state="Sin contestar", initialOfferType="Venta").put()
HistoricalRequest(appliant=nilsenUser, copy=kafkaCopy1, initialUser=testUser, state="Negociando", initialOfferType="Venta").put()
HistoricalRequest(appliant=billyUser, copy=kafkaCopy1, initialUser=testUser, state="Sin contestar", initialOfferType="Venta").put()
HistoricalRequest(appliant=lolUser, copy=kafkaCopy1, initialUser=testUser, state="Sin contestar", initialOfferType="Venta").put()

Request(user=nilsenUser,copy=panCopy1, state="Negociando").put()
Request(user=billyUser,copy=panCopy1, state="Sin contestar").put()
Request(user=lolUser,copy=panCopy1, state="Sin contestar").put()
HistoricalRequest(appliant=nilsenUser, copy=panCopy1, initialUser=testUser, state="Sin contestar", initialOfferType="Prestamo").put()
HistoricalRequest(appliant=nilsenUser, copy=panCopy1, initialUser=testUser, state="Negociando", initialOfferType="Prestamo").put()
HistoricalRequest(appliant=billyUser, copy=panCopy1, initialUser=testUser, state="Sin contestar", initialOfferType="Prestamo").put()
HistoricalRequest(appliant=lolUser, copy=panCopy1, initialUser=testUser, state="Sin contestar", initialOfferType="Prestamo").put()


#requests de testuser
Request(user=testUser,copy=austenCopy1, state="Sin contestar").put()
Request(user=testUser,copy=deseoCopy1, state="Sin contestar").put()
Request(user=testUser,copy=tokyoCopy1, state="Sin contestar").put()
Request(user=testUser,copy=quienCopy1, state="Sin contestar").put()
Request(user=testUser,copy=cieloCopy1, state="Sin contestar").put()
Request(user=testUser,copy=prisioneroCopy1, state="Sin contestar").put()
Request(user=testUser,copy=imperioCopy1, state="Sin contestar").put()
Request(user=testUser,copy=arenaCopy1, state="Sin contestar").put()
Request(user=testUser,copy=libertadCopy1, state="Sin contestar").put()
HistoricalRequest(appliant=testUser, copy=austenCopy1, initialUser=nilsenUser, state="Sin contestar", initialOfferType="Intercambio").put()
HistoricalRequest(appliant=testUser, copy=deseoCopy1, initialUser=nilsenUser, state="Sin contestar", initialOfferType="Intercambio").put()
HistoricalRequest(appliant=testUser, copy=tokyoCopy1, initialUser=nilsenUser, state="Sin contestar", initialOfferType="Intercambio").put()
HistoricalRequest(appliant=testUser, copy=quienCopy1, initialUser=nilsenUser, state="Sin contestar", initialOfferType="Intercambio").put()
HistoricalRequest(appliant=testUser, copy=cieloCopy1, initialUser=nilsenUser, state="Sin contestar", initialOfferType="Intercambio").put()
HistoricalRequest(appliant=testUser, copy=prisioneroCopy1, initialUser=nilsenUser, state="Sin contestar", initialOfferType="Intercambio").put()
HistoricalRequest(appliant=testUser, copy=imperioCopy1, initialUser=nilsenUser, state="Sin contestar", initialOfferType="Intercambio").put()
HistoricalRequest(appliant=testUser, copy=arenaCopy1, initialUser=nilsenUser, state="Sin contestar", initialOfferType="Intercambio").put()
HistoricalRequest(appliant=testUser, copy=libertadCopy1, initialUser=nilsenUser, state="Sin contestar", initialOfferType="Intercambio").put()



#requests de nilsenuser
Request(user=nilsenUser,copy=nansenCopy1, state="Sin contestar").put()
Request(user=nilsenUser,copy=vasiliCopy1, state="Sin contestar").put()
Request(user=nilsenUser,copy=beevorCopy1, state="Sin contestar").put()
Request(user=nilsenUser,copy=krohgCopy1, state="Sin contestar").put()
Request(user=nilsenUser,copy=franzCopy1, state="Sin contestar").put()
Request(user=nilsenUser,copy=zeppelinCopy1, state="Sin contestar").put()
Request(user=nilsenUser,copy=nerudaCopy1, state="Sin contestar").put()
Request(user=nilsenUser,copy=aleixandreCopy1, state="Sin contestar").put()
Request(user=nilsenUser,copy=lorcaCopy1, state="Sin contestar").put()
Request(user=nilsenUser,copy=coronelCopy1, state="Sin contestar").put()
Request(user=nilsenUser,copy=esclavaCopy1, state="Sin contestar").put()
HistoricalRequest(appliant=nilsenUser, copy=nansenCopy1, initialUser=testUser, state="Sin contestar", initialOfferType="Intercambio").put()
HistoricalRequest(appliant=nilsenUser, copy=vasiliCopy1, initialUser=testUser, state="Sin contestar", initialOfferType="Intercambio").put()
HistoricalRequest(appliant=nilsenUser, copy=beevorCopy1, initialUser=testUser, state="Sin contestar", initialOfferType="Intercambio").put()
HistoricalRequest(appliant=nilsenUser, copy=krohgCopy1, initialUser=testUser, state="Sin contestar", initialOfferType="Intercambio").put()
HistoricalRequest(appliant=nilsenUser, copy=franzCopy1, initialUser=testUser, state="Sin contestar", initialOfferType="Intercambio").put()
HistoricalRequest(appliant=nilsenUser, copy=zeppelinCopy1, initialUser=testUser, state="Sin contestar", initialOfferType="Intercambio").put()
HistoricalRequest(appliant=nilsenUser, copy=nerudaCopy1, initialUser=testUser, state="Sin contestar", initialOfferType="Intercambio").put()
HistoricalRequest(appliant=nilsenUser, copy=aleixandreCopy1, initialUser=testUser, state="Sin contestar", initialOfferType="Intercambio").put()
HistoricalRequest(appliant=nilsenUser, copy=lorcaCopy1, initialUser=testUser, state="Sin contestar", initialOfferType="Intercambio").put()
HistoricalRequest(appliant=nilsenUser, copy=coronelCopy1, initialUser=testUser, state="Sin contestar", initialOfferType="Intercambio").put()
HistoricalRequest(appliant=nilsenUser, copy=esclavaCopy1, initialUser=testUser, state="Sin contestar", initialOfferType="Intercambio").put()

db.delete(Transaction.all().fetch(512))

db.delete(Club.all().fetch(512))
club1 = Club(name=u'aficionados de Justin',description=u'Club de lectores del libro Justin Bieber', author=u'Justin Bieber', genre= [u'Poesia',u'Ciencia Ficcion'],invitaciones = [u'user@example.com'],state=u'Habilitado', book=justinBook,owner = testUser, image= db.Link('http://www.studentsoftheworld.info/sites/star/img/994_JustinBieber[1].png')).put()
club2 = Club(name=u'Tres metros sobre el cielo',description=u'Amantes del libro Tres metros sobre el cielo', author=u'Federico Moccia', genre= [u'Poesia',u'Novela'],invitaciones = [u'nilsen@example.com',u'billy@gates.com'],state=u'Deshabilitado', book=cieloBook, owner = testUser, image=db.Link('http://ecx.images-amazon.com/images/I/511TxpLpVYL._SL500_AA240_.jpg')).put()
club3 = Club(name=u'fans de Haruki Murakami',description=u'Este club va dirigido a los fans de Haruki Murakami', author=u'Haruki Murakami', genre= [u'Poesia',u'Novela'],invitaciones = [u'patrypons@example.com',u'billy@gates.com'],state=u'Habilitado', owner= testUser, image=db.Link('http://2.bp.blogspot.com/__7FN-K-p0ws/TL2YKFVWofI/AAAAAAAAAMA/MK5mIMWJc1o/s1600/hmurakami.jpg')).put()
club4 = Club(name=u'El club de la comedia',description=u'Este club va dirigido a los fans del club de la comedia', author=u'Federico Moccia', genre= [u'Narrativa',u'Biograf�a'],invitaciones = [u'billy@gates.com',u'test@example.com'],state=u'Habilitado', owner = nilsenUser, image=db.Link('http://s3.amazonaws.com/kym-assets/photos/images/original/000/096/044/trollface.jpg?1296494117')).put()
club5 = Club(name=u'Fans de Knut Hamsun',description=u'Este club va dirigido a los fans de Knut Hamsun', author=u'Knut Hamsun', genre= [u'Narrativa',u'Biograf�a'],invitaciones = [u'billy@gates.com',u'test@example.com',u'patrypons@example.com',u'lol@example.com'],state=u'Habilitado', owner = nilsenUser, image=db.Link('http://farm3.static.flickr.com/2711/4437964112_b114fa90b6.jpg')).put()
club6 = Club(name=u'Intrigados por Kafka en la Orilla',description=u'Club para el debate sobre Kafka en la Orilla', author=u'Haruki Murakami', genre= [u'Narrativa',u'Biograf�a'],invitaciones = [u'test@example.com'],state=u'Habilitado', book=kafkaBook, owner = nilsenUser, image=db.Link('http://ecx.images-amazon.com/images/I/31oVN6Jg8RL._SL500_AA240_.jpg')).put()
club7 = Club(name=u'Adictos a la historia',description=u'Club para amantes de la historia',  genre= [u'Historico',u'Biograf�a'],invitaciones = [u'test@example.com'],state=u'Habilitado', owner = nilsenUser, image=db.Link('http://www.satlogo.com/logo/hires/cc/canal_de_historia.png')).put()

db.delete(Club_User.all().fetch(512))
Club_User(user=testUser,club=club1,state=u'Propietario').put()
Club_User(user=userUser,club=club1,state=u'Invitado').put()
Club_User(user=billyUser,club=club1,state=u'Solicitud Aceptada').put()
Club_User(user=patryUser,club=club1,state=u'Solicitud Aceptada').put()
Club_User(user=nilsenUser,club=club1,state=u'Solicitado').put()

Club_User(user=testUser, club= club2, state =u'Propietario').put()
Club_User(user=nilsenUser,club=club2,state=u'Invitacion Aceptada').put()
Club_User(user=billyUser,club=club2,state=u'Invitado').put()

Club_User(user=testUser,club=club3,state=u'Propietario').put()
Club_User(user=patryUser,club=club3,state=u'Invitado').put()
Club_User(user=billyUser,club=club3,state=u'Invitado').put()
Club_User(user=nilsenUser,club=club3,state=u'Solicitado').put()
Club_User(user=userUser,club=club3,state=u'Solicitud Aceptada').put()

Club_User(user=nilsenUser,club=club4,state='Propietario').put()
Club_User(user=billyUser,club=club4,state=u'Invitado').put()
Club_User(user=testUser,club=club4,state=u'Invitado').put()

Club_User(user=nilsenUser,club=club5,state=u'Propietario').put()
Club_User(user=testUser,club=club5,state=u'Solicitado').put()
Club_User(user=billyUser,club=club5,state=u'Invitacion Aceptada').put()
Club_User(user=patryUser,club=club5,state=u'Invitacion Aceptada').put()
Club_User(user=lolUser,club=club5,state=u'Invitacion Aceptada').put()

Club_User(user=lolUser,club=club6,state=u'Propietario').put()
Club_User(user=testUser,club=club6,state=u'Invitado').put()

Club_User(user=nilsenUser,club=club7,state=u'Propietario').put()
Club_User(user=testUser,club=club7,state=u'Invitacion Aceptada').put()

db.delete(Comment.all().fetch(512))
comment1 = Comment(user=patryUser, text=u'OseAaA, EsTa SuuuuupeR WeNnNoooOooO!!!').put()
comment2 = Comment(user=nilsenUser, text=u'De mayor quiero ser como �l.').put()

db.delete(ClubComment.all().fetch(512))
ClubComment(club=club1, comment=comment1).put()
ClubComment(club=club1, comment=comment2).put()

db.delete(BookComment.all().fetch(512))
db.delete(UserComment.all().fetch(512))

db.delete(Alert.all().fetch(512))
Alert( date=datetime.date(year=2011,day=5,month=1), user=testUser, type='Solicitud: Finalizada', description='Notificacion de prueba, y nunca deberia de salir').put()
Alert( date=datetime.date(year=2012,day=5,month=1), user=testUser, type='Club: Aceptado', description='Notificacion de prueba, anadida manualmente en la DB...' ).put()
Alert( date=Alert.setDate(), user=testUser, type='Club: Rechazado', description='Notificacion de prueba, anadida manualmente en la DB...' ).put()
Alert( date=Alert.setDate(), user=testUser, type='Solicitud: Finalizada', description='Notificacion de prueba, anadida manualmente en la DB...').put()
Alert( date=Alert.setDate(), user=nilsenUser, type='Club: Solicitud', description="Usuario test@example.com quiere unirse al club Fans de Knut Hamsun", relatedClub=club5).put()

db.delete(RequestComment.all().fetch(512))
commentReqNilsen = Comment(user=nilsenUser, text=u'O me lo das o te pego una paliza.').put()
RequestComment(comment=commentReqNilsen, request=nilsenRequest).put()



db.delete(ClubEvent.all().fetch(512))
db.delete(ClubEventAssit.all().fetch(512))

gritos = ClubEvent(club=club1, name=u'Ensayo de gritos', comment=u'Como siempre. ToDoOo Por JustIn!', place=u'Donde siempre',  date=datetime.datetime.strptime("01/02/2012", "%d/%m/%Y")).put()
concierto = ClubEvent(club=club1, name=u'Concierto Valencia!!', comment=u'Por fin vieneeee!!', place=u'Plaza de toros', date=datetime.datetime.strptime("01/01/2011", "%d/%m/%Y")).put()
lectura = ClubEvent(club=club1, name=u'Lectura en grupo', comment=u'Para que todos puedan opinar con otros fans sobre esta magn�fica obra de arte', place=u'Aula libre', date=datetime.datetime.strptime("01/04/2012", "%d/%m/%Y")).put()
lectura2 = ClubEvent(club=club1, name=u'Lectura en grupo II', comment=u'Visto el �xito del primer evento hemos decidido crear otro!', place=u'Aula libre', date=datetime.datetime.strptime("02/04/2012", "%d/%m/%Y")).put()

ClubEventAssit(event=gritos, user=nilsenUser).put();
ClubEventAssit(event=gritos, user=billyUser).put();

ClubEventAssit(event=concierto, user=nilsenUser).put();
ClubEventAssit(event=concierto, user=testUser).put();
ClubEventAssit(event=concierto, user=patryUser).put();
ClubEventAssit(event=concierto, user=userUser).put();

ClubEventAssit(event=lectura, user=nilsenUser).put();
ClubEventAssit(event=lectura, user=testUser).put();
ClubEventAssit(event=lectura, user=patryUser).put();
ClubEventAssit(event=lectura, user=userUser).put();




