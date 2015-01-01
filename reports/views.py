from django.shortcuts import render, render_to_response
from django.db import connection
from prints.models import *

# Create your views here.
rm = "mistral"

def getReportes(request):
	