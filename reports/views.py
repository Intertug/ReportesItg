from django.shortcuts import render, render_to_response
from django.db import connection
from reports.models import *

# Create your views here.
rm = "mistral"

def getReportes(request):

	return render_to_response("reportes.html", locals())

def getDia(request):

	return render_to_response("dia.html", locals())
