from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from ConferenceRoom.models import ConfRoom


def main_page(request):
    return render(request, template_name='base_template.html')


def new_room(request):
    if request.method == "GET":
        return render(request, template_name='new_room.html')
    else:
        room_name = request.POST.get('room_name')
        room_capacity = request.POST.get('room_capacity')
        room_capacity = int(room_capacity)
        # projector_availability = request.POST.get('projector')
        if not room_name or room_capacity < 0:
            return HttpResponse('Information you have provided is incorrect')
        elif ConfRoom.objects.get(name=room_name):
            return HttpResponse('Conference room already exists')
        else:
            room_new = ConfRoom.objects.create(name=room_name, capacity=room_capacity)
            room_new.save()
            return HttpResponse('Conference room has been saved')