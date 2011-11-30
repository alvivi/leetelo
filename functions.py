# -*- coding: utf-8 -*-

# En este fichero se deja codigo a usar
from models import *

class SearchResults():
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



class ClubResult():
    @classmethod
    def searchAll(result,name,creator,genre,book):
	result = []
	listoftitles =[]
	
	searchlist = Club.all().fetch(100)
	searchlist = ClubResult.searchGenre(searchlist,genre)
	searchlist = ClubResult.searchName(searchlist,name)
	searchlist = ClubResult.searchCreator(searchlist,creator)
	searchlist = ClubResult.searchBook(searchlist,book)
	
	result = searchlist
	return result

    @classmethod
    def searchGenre(resulttemp, list, genre):
	resulttemp = []
	if genre == '------':
	    resulttemp = list

	else:
	    for x in list:
		if genre in x.genre:
		    resulttemp.append(x)


	return resulttemp
    
    @classmethod
    def searchName(resulttemp, list, name):
	resulttemp = []
	if name == '':
	    resulttemp = list

	else:
	    for x in list:
		if name.lower() in x.name.lower():
		    resulttemp.append(x)


	return resulttemp
    
    @classmethod
    def searchCreator(resulttemp, list, author):
	resulttemp = []
	if author == '':
	    resulttemp = list

	else:
	    for x in list:
		if author.lower() in x.author.lower():
		    resulttemp.append(x)


	return resulttemp
    
    @classmethod
    def searchBook(resulttemp, list, book):
	resulttemp = []
	if book == '':
	    resulttemp = list

	else:
	    for x in list:
		if book.lower() in x.book.lower():
		    resulttemp.append(x)


	return resulttemp