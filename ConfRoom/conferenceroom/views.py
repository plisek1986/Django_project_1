from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
# Create your views here.

def main_page(request):
    return render(request, template_name='base_template.html')