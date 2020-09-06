from random import randrange

from django.http import Http404
from django.http import HttpResponseNotFound
from django.http import HttpResponseServerError
from django.shortcuts import render
from django.views import View

from tours.data import departures
from tours.data import tours


class MainView(View):
    def get(self, request):
        random_tours = []
        title = "Stepik travel"
        tour_count = 6
        all_tours = len(tours)
        while len(random_tours) < tour_count:
            id = randrange(1, all_tours)
            if tours[id] not in random_tours:
                tours[id]['id'] = id
                random_tours.append(tours[id])
        context = {
            "tours": random_tours,
            "departures": departures,
            "title": title

        }
        return render(request, "index.html", context=context)


class DepartureView(View):
    def get(self, request, departure):
        if departure not in departures:
            raise Http404
        tours_departure = []
        price = []
        nights = []
        title = "Stepik travel"
        for id in tours:
            if tours[id]["departure"] == departure:
                tours[id]['id'] = id
                tours_departure.append(tours[id])
        for tour in tours_departure:
            price.append(tour["price"])
        for tour in tours_departure:
            nights.append(tour["nights"])
        context = {
            "departures": departures,
            "departure": departures[departure],
            "tours": tours_departure,
            "tour_count": len(tours_departure),
            "price_max": max(price),
            "price_min": min(price),
            "nights_max": max(nights),
            "nights_min": min(nights),
            "title": title
        }
        return render(request, "departure.html", context=context)


class TourView(View):

    def get(self, request, id):
        if id not in tours:
            raise Http404

        title = tours[id]['title']

        context = {
            "tour": tours[id],
            "depart": departures[tours[id]['departure']],
            "departures": departures,
            "title": title

        }
        return render(request, "tour.html", context=context)


def custom_handler404(request, exception):
    return HttpResponseNotFound('<center><h2>Ой, что то сломалось... Простите извините!</h2></center>')


def custom_handler500(request):
    return HttpResponseServerError('Внутрення ошибка сервера')
