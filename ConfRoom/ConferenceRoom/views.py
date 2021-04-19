from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from ConferenceRoom.models import ConfRoom
from django.views import View
from django.http import HttpResponseRedirect


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
            return HttpResponse('Conference room has been saved')


def room_list(request):
    rooms = ConfRoom.objects.all()
    return render(request, template_name='room_list.html', context={'rooms': rooms})


#
def room_view(request, id):
    if request.method == 'GET':
        room = ConfRoom.objects.get(id=id)
        return render(request, template_name='room_view.html', context={'room': room})


class RoomModify(View):
    def get(self, request, id):
        room_mod = ConfRoom.objects.get(id=id)
        return render(request, template_name='room_modify.html', context={'room_mod': room_mod})


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
