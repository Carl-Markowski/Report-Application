from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.views import generic
#from .forms import ProjectForm, PortfolioForm

def index(request):
    return render (request, 'report_app/index.html')

class TeacherListView(generic.ListView):
    model = Teacher
class TeacherDetailView(generic.DetailView):
    model = Teacher



