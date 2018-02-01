from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.views import View
from django.utils.dateparse import parse_date
from django.db.models import Q

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.

from conference.models import Room, Booking

class Rooms(View):

    def get(self, request):
        if request.GET:
            return HttpResponse('dawaj')

        rooms = Room.objects.all()
        return render_to_response('rooms.html', {
            'rooms': rooms
        })


@method_decorator(csrf_exempt, name='dispatch')
class NewBooking(View):

    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        return render(request, "new_booking.html", {"room": room})

    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        try:
            date = parse_date(request.POST["date"])
        except (ValueError, KeyError):
            return HttpResponseBadRequest("niepoprawna data")

        try:
            Booking.objects.create(room=room, date=date,
                                   comment=request.POST.get("comment", ''))

        except IntegrityError:
            return HttpResponseBadRequest("Sala jest już zajęta. Wybierz inną datę.")
        return HttpResponseRedirect(reverse("rooms"))


error_message_add_rooms = """<a href=room/new/>Powrót</a>"""

@method_decorator(csrf_exempt, name='dispatch')
class AddRooms(View):

    def get(self, request):
        return render_to_response('add_room.html')

    def post(self, request):

        if request.POST['name'] == '':
            return HttpResponse('Nie podałeś nazwy sali: ' + error_message_add_rooms)
        else:
            name = request.POST['name']
        if int(request.POST['num_seats']) < 10:
            return HttpResponse('Sala konferencyjna nie może być mniejsza niż na 10 osób: ' + error_message_add_rooms)
        else:
            num_seats = request.POST['num_seats']
        if request.POST['has_beamer'] not in ['tak', 'nie']:
            return HttpResponse('Te pole przyjmuje tylko wartości tak lub nie: ' + error_message_add_rooms)
        else:
            if request.POST['has_beamer'] == 'tak':
                has_beamer = True
            else:
                has_beamer = False

        #room = Room.objects.create(name=name, num_seats=num_seats, has_beamer=has_beamer)

        for rooms in Room.objects.all():
            if name == rooms.name:
                return HttpResponse('Sala konferencyjna o takiej nazwie już istnieje! ' + error_message_add_rooms)
            else:
                room = Room.objects.create(name=name, num_seats=num_seats, has_beamer=has_beamer)
                room.save()
                return HttpResponse("""Stworzono nową salę konferencyjną:<br>
                                        """ +'<br> <a href=/room/new/>Dodaj nową salę</a>'
                                    + '<br><a href="/rooms/">Lista sal konferencyjnych</a>')


        #dodaj sprawdzenie czy sala o podanej nazwie przypadkiem juz nie istnieje
        #jesli nie to dodaj salę do listy i odnosnik do strony glownej i odnosnik do
        # wyswietlenia danych o sali konferencyjnej

@method_decorator(csrf_exempt, name='dispatch')
class ModifyRoom(View):

    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        return render(request, "modify_room.html", {"room": room})
    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)

        if request.POST['name'] == '':
            return HttpResponse('Nie podałeś nazwy sali: ' + error_message_add_rooms)
        else:
            name = request.POST['name']
        if int(request.POST['num_seats']) < 10:
            return HttpResponse('Sala konferencyjna nie może być mniejsza niż na 10 osób: ' + error_message_add_rooms)
        else:
            num_seats = request.POST['num_seats']
        if request.POST['has_beamer'] not in ['tak', 'nie']:
            return HttpResponse('Te pole przyjmuje tylko wartości tak lub nie: ' + error_message_add_rooms)
        else:
            if request.POST['has_beamer'] == 'tak':
                has_beamer = True
            else:
                has_beamer = False

        room.name = name
        room.num_seats = num_seats
        room.has_beamer = has_beamer
        room.save()

        return HttpResponse("""Zmodyfikowano salę konferencyjną<br>
        <a href="/rooms/">Powrót do listy sal konferencyjnych</a>""")

@method_decorator(csrf_exempt, name='dispatch')
class ShowRoom(View):
    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        return render(request, 'show_room.html', {"room": room})

@method_decorator(csrf_exempt, name='dispatch')
class DeleteRoom(View):

    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        return render(request, 'delete_room.html', {"room": room})
    def post(self, request, room_id):
        if 'leave' in request.POST:
            return HttpResponseRedirect(reverse('rooms'))
        elif 'delete' in request.POST:
            room = get_object_or_404(Room, id=room_id)
            room.delete()
            return HttpResponse("""Usunięto salę: {}<br>
                              <p><a href="/rooms/">Powrót do listy sal konferencyjnych</a></p>""".format(room.name))


class Search(View):
    def get(self, request, name, num_seats, has_beamer):
        name_search = name
        num_seats_search = num_seats
        has_beamer_search= has_beamer

        #return render_to_response('search_room.html')

        return render(request, 'search_room.html', {"name_search": name_search,
                                                    "num_seats_search": num_seats_search,
                                                    "has_beamer_search": has_beamer_search,})
