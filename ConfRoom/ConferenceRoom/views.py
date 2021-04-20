from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from ConferenceRoom.models import ConfRoom
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages


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


def room_view(request, id):
    if request.method == 'GET':
        room = ConfRoom.objects.get(id=id)
        return render(request, template_name='room_view.html', context={'room': room})


class RoomModify(View):
    def get(self, request, id):
        room_mod = ConfRoom.objects.get(id=id)
        return render(request, template_name='room_modify.html', context={'room_mod': room_mod})

    def post(self, request, id):
        room_mod = ConfRoom.objects.get(id=id)
        room_mod_name = request.POST.get('room_name')
        room_mod_capacity = request.POST.get('room_capacity')
        room_mod_capacity = int(room_mod_capacity)
        mod_projector_availability = request.POST.get('projector_availability') == 'on'
        if not room_mod_name or room_mod_capacity < 0:
            return HttpResponse('Provided information is incorrect!')
        elif ConfRoom.objects.filter(name=room_mod_name):
            return HttpResponse('This room already exists!')
        else:
            room_mod_ = ConfRoom.objects.get(id=id)
            room_mod_.name = room_mod_name
            room_mod_.capacity = room_mod_capacity
            room_mod_.projector_availability = mod_projector_availability
            room_mod_.save()
            messages.success(request, 'Room has been modified')
            return HttpResponseRedirect('/room/list/')

def room_delete(request, id):
    if request.method == 'GET':
        room_del = ConfRoom.objects.get(id=id)
        room_del.delete()
        response = HttpResponseRedirect('/room/list/')
        return response


def room_reserve(request, id):
    if request.method == 'GET':
        room_res = ConfRoom.objects.get(id=id)
        return render(request, template_name='room_reserve.html', context={'room_res': room_res})
