from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from ConferenceRoom.models import ConfRoom, Reservation
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from datetime import datetime


def main_page(request):
    return render(request, template_name='base_template.html')


class AddRoom(View):
    def get(self, request):
        return render(request, template_name='add_room.html')

    def post(self, request):
        room_name = request.POST.get('room_name')
        room_capacity = request.POST.get('room_capacity')
        room_capacity = int(room_capacity)
        projector_availability = request.POST.get('projector') == 'on'
        if not room_name or room_capacity < 0:
            return HttpResponse('Information you have provided is incorrect')
        elif ConfRoom.objects.filter(name=room_name):
            return HttpResponse('Conference room already exists')
        else:
            room_new = ConfRoom.objects.create(name=room_name, capacity=room_capacity,
                                               projector_availability=projector_availability)
            room_new.save()
            # messages.success(request, 'Room has been added!')
            return HttpResponseRedirect('/room/list/')


def room_list(request):
    rooms = ConfRoom.objects.all()
    return render(request, template_name='room_list.html', context={'rooms': rooms})


def room_view(request, room_id):
    if request.method == 'GET':
        room = ConfRoom.objects.get(id=room_id)
        return render(request, template_name='room_view.html', context={'room': room})


class RoomModify(View):
    def get(self, request, room_id):
        room_mod = ConfRoom.objects.get(id=room_id)
        return render(request, template_name='room_modify.html', context={'room_mod': room_mod})

    def post(self, request, room_id):
        room_mod = ConfRoom.objects.get(id=room_id)
        room_mod_name = request.POST.get('room_name')
        room_mod_capacity = request.POST.get('room_capacity')
        room_mod_capacity = int(room_mod_capacity)
        mod_projector_availability = request.POST.get('projector_availability') == 'on'
        if not room_mod_name or room_mod_capacity < 0:
            return HttpResponse('Provided information is incorrect!')
        elif ConfRoom.objects.filter(name=room_mod_name):
            return HttpResponse('This room already exists!')
        else:
            room_mod.name = room_mod_name
            room_mod.capacity = room_mod_capacity
            room_mod.projector_availability = mod_projector_availability
            room_mod.save()
            messages.success(request, 'Room has been modified')
            return HttpResponseRedirect('/room/list/')


def room_delete(request, room_id):
    if request.method == 'GET':
        room_del = ConfRoom.objects.get(id=room_id)
        room_del.delete()
        response = HttpResponseRedirect('/room/list/')
        return response


class RoomReserve(View):
    def get(self, request, room_id):
        room_res = ConfRoom.objects.get(id=room_id)
        return render(request, template_name='room_reserve.html', context={'room_res': room_res})

    def post(self, request, room_id):
        room_res = ConfRoom.objects.get(id=room_id)
        date = request.POST.get('date')
        comment = request.POST.get('comment')
        # reservations will appear as a dict QuerySet [{'date': datetime.date(2021, 4, 22)}....]
        reservations = room_res.reservation_set.all().values('date')
        #you have to change this dict QuerySet to the list
        reservations = list(reservations)
        today = str(datetime.today())
        #you have iterate on the list of reservations to get value for dates
        dates = (date['date'] for date in reservations)
        if date in dates:
            return HttpResponse('This date is already booked!')
        elif date < today:
            return HttpResponse('Please choose the current or future date!')
        else:
            reservation = Reservation.objects.create(room_id=room_res, date=date, comment=comment)
            reservation.save()
            messages.success(request, 'The room has been booked!')
            return HttpResponseRedirect('/room/list/')
