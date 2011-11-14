# -*- coding: utf-8 -*-

# En este fichero se define toda la lógica de aplicación. Las instancias de los
# modelos son persistentes.

from google.appengine.ext import db


# Ficha del libro, la obra en sí
class Book(db.Model):
    title  = db.StringProperty(required=True)
    author = db.StringProperty()
    genre  = db.StringProperty(choices=set([u'Aventuras', u'Biografía', u'Ciencia Ficción', u'Ensayo', u'Histórico', u'Narrativa', u'Novela', u'Poesía', u'Romántico']))
    year   = db.IntegerProperty()

# El ejemplar del libro
class Copy(db.Model):
    book = db.ReferenceProperty(Book)
    user = db.UserProperty()
    copyState = db.StringProperty(choices=set(['Excelente','Bueno','Deteriorado','Muy viejo']))
    offerState = db.StringProperty(choices=set(['No disponible','Disponible','En oferta',
                                                'Con solicitud','Esperando confirmacion',
                                                'Esperando recepcion', 'Prestado',
                                                'Intercambiado','Vendido','Llega1','Llega2']))
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
        return cls.all().filter('user =', user).filter('offerState !=', 'En oferta').fetch(128) + cls.all().filter('user !=', user).filter('offerState =', 'No disponible').fetch(128)



# Solicitud sobre un libro
class Request(db.Model):
    copy = db.ReferenceProperty(Copy,collection_name='owner_copy')
    exchangeCopy = db.ReferenceProperty(Copy,collection_name='exchange_copy')
    user = db.UserProperty()
    state = db.StringProperty(choices=set(['Sin contestar','Negociando','Aceptada','Rechazada']))
    exchangeType = db.StringProperty(choices=set(['Directo','Indirecto']))

    # Método de clase que devuelve todas las solicitudes que ha realizado un usuario
    @classmethod
    def allRequestsOf(cls, user):
        return cls.all().filter('user =', user).fetch(128)

    # Método de clase que devuelve todas las solicitudes que se han recibido sobre un libro
    @classmethod
    def allRequestsFor(cls, copy):
        return cls.all().filter('copy =', copy).fetch(128)

class Sale(db.Model):
    copy = db.ReferenceProperty(Copy)
    vendor = db.UserProperty()
    buyer = db.UserProperty()
    date = db.DateProperty(auto_now=True)

class Loan(db.Model):
    copy = db.ReferenceProperty(Copy)
    owner = db.UserProperty()
    lendingTo = db.UserProperty()
    arrivalDate = db.DateProperty()
    returningDate = db.DateProperty()

class Exchange(db.Model):
    copy1 = db.ReferenceProperty(Copy,collection_name='copy1')
    owner1 = db.UserProperty()
    copy2 = db.ReferenceProperty(Copy,collection_name='copy2')
    owner2 = db.UserProperty()
    exchangeDate = db.DateProperty(auto_now=True)
    exchangeType = db.StringProperty(choices=set(['Directo','Indirecto']))

    @classmethod
    def allExchangesFromUser(cls, user):
        return cls.all().filter('owner2', user).fetch(128)

    @classmethod
    def switchFor(cls, copy, user):
        return cls.all().filter('copy1 =', copy).filter('copy2.user =', user).fetch(128)

    @classmethod
    def getDirectExchange(cls, copy1, owner1, copy2, owner2):
        return cls.all().filter('copy1 =',copy1).filter('copy2 =',copy2).filter('owner1 =', owner1).filter('owner2 =',owner2).filter('exchangeType =','Directo').fetch(128)

class SearchResults(db.Model):


    @classmethod
    def searchAll(result,title,author,genre,publisher,yearFrom,yearTo,optionsExchange,optionsRent,optionsSell):
        result = []
        listoftitles =[]

        q = Book.all()
        q=SearchResults.searchGenre(q,genre)
        q=SearchResults.searchYear(q,yearFrom,yearTo)
        searchlist = q.fetch(100)

        searchlist = SearchResults.searchName(searchlist,title)
        searchlist = SearchResults.searchAuthor(searchlist,author)
        searchlist = SearchResults.searchPublisher(searchlist,publisher)
        searchlist = SearchResults.searchAvailabilityEx(searchlist,optionsExchange)
        searchlist = SearchResults.searchAvailabilityRe(searchlist,optionsRent)
        searchlist = SearchResults.searchAvailabilitySe(searchlist, optionsSell)


        for bk in searchlist:
            if listoftitles.count(bk.title) == 0:
                result.append(bk)
                listoftitles.append(bk.title)

        return result



    @classmethod
    def searchGenre(resulttemp, q, genre):
	if genre == '------':
	    resulttemp = q

	else:
	    q.filter('genre = ',genre)
	    resulttemp = q

	return resulttemp


    @classmethod
    def searchYear(resulttemp, q, yearFrom, yearTo):
	if yearFrom == '':
	    resulttemp = q

	else:
	    resulttemp = q.filter('year >=',yearFrom)


	if yearFrom == '':
	    resulttemp = resulttemp

	else:
	    resulttemp = resulttemp.filter('year <=',yearTo)

	return resulttemp


    @classmethod
    def searchName(resulttemp, list, title):
	resulttemp = []
	if title == '':
	    resulttemp = list

	else:
	    for x in list:
		if title.lower() in x.title.lower():
		    resulttemp.append(x)


	return resulttemp


    @classmethod
    def searchAuthor(resulttemp, list, author):
	resulttemp = []

	if author == '':
	    resulttemp = list

	else:
	    for x in list:
		if author.lower() in x.author.lower():
		    resulttemp.append(x)

	return resulttemp


    @classmethod
    def searchPublisher(resulttemp, list,publisher):
	resulttemp = []

	if publisher == '':
	    resulttemp = list

	else:
	    for x in list:
		Clist = Copy.all().filter('book.title =',x.title)
		Clist = Clist.fetch(100)
		for copy in Clist:
		    if publisher.lower() in copy.publisher.lower():
			resulttemp.append(x)
			break

	return resulttemp

    @classmethod
    def searchAvailabilityEx(resulttemp, list, optionsExchange):
	resulttemp = []

	if optionsExchange == 'on':
	    for x in list:
		Clist = Copy.all().filter('book.title =',x.title)
		Clist = Clist.fetch(100)
		for copy in Clist:
		    if copy.offerType == 'Intercambio':
			resulttemp.append(x)
			break
	else:
	    resulttemp = list

	return resulttemp

    @classmethod
    def searchAvailabilityRe(resulttemp, list, optionsRent):
	resulttemp = []
	if optionsRent == 'on':
	    for x in list:
		Clist = Copy.all().filter('book.title =',x.title)
		Clist = Clist.fetch(100)
		for copy in Clist:
		    if copy.offerType == 'Prestamo':
			resulttemp.append(x)
			break
	else:
	    resulttemp = list

	return resulttemp


    @classmethod
    def searchAvailabilitySe(resulttemp, list, optionsSell):
	resulttemp = []
	if optionsSell == 'on':
	    for x in list:
		Clist = Copy.all().filter('book.title =',x.title)
		Clist = Clist.fetch(100)
		for copy in Clist:
		    if copy.offerType == 'Venta':
			resulttemp.append(x)
			break
	else:
	    resulttemp = list

	return resulttemp
