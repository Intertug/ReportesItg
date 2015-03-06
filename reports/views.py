from django.shortcuts import render, render_to_response
from django.db import connection
from reports.models import *
from datetime import datetime, timedelta, date
from monthdelta import MonthDelta

remolcadores = {"Baru Inti": 34, "Baru Pacifico": 33, "Mistral": 28, "Vali": 23, "Carex": 5}

#Generadores de Templates

def getReports(request):
	'''
	Crea la vista para la pagina de entrada
	'''

	return render_to_response("reportesitg.html", locals())	

def getDay(request):
	'''
	crea la vista por defecto del dia actual, si no 
	crea la vista de la consulta para un dia dado
	'''

	if 'date1' in request.GET and request.GET['date1'] != '':
		date = str(request.GET['date1'])
	else:
		date = str(datetime.now()).split(' ')[0]

	try:
		#Convertimos la fechas de los input en dates de python
		oneday = timedelta(days=1) #Creamos un delta de 1 dia
		dateone = datetime.strptime(date, "%Y-%m-%d")
		nextday = dateone+oneday #Le sumamos un dia a la fecha
	
		#Convertimos las fechas a string con formato AAAA-MM-DD
		dateone = dateone.isoformat()[:10]
		nextday = nextday.isoformat()[:10]
	except ValueError:
		raise ValueError("Incorrect data format, should be YYYY-MM-DD")

	tomorrow = nextday.split('-')
	tomorrow = tomorrow[0] + tomorrow[1] + tomorrow[2]
	today = dateone.split('-')
	today = today[0] + today[1] + today[2]
	#sacamos  el id del remolcador
	if request.GET['vessel'] in remolcadores:
		nombre = request.GET['vessel']
		vessel = remolcadores[nombre]

	datereporter = datetime.now();
	vesselname = request.GET['vessel']
	consumo = genDia(today, tomorrow, vessel)

	return render_to_response("day.html", locals())

def getMonth(request):
	'''
	crea la vista por defecto del mes actual, si no 
	crea la vista de la consulta para un mes dado
	'''

	if 'year' in request.GET and 'month' in request.GET:
		if(request.GET['year'] != ''):
			year = request.GET['year']
		else:
			datewtime	= str(datetime.now()).split('-')
			year		= datewtime[0]
		if(request.GET['month'] != ''):
			month = request.GET['month']
		else:
			datewtime	= str(datetime.now()).split('-')
			month 		= datewtime[1]
	else:
		datewtime	= str(datetime.now()).split('-')
		year		= datewtime[0]
		month 		= datewtime[1]

	date = str(year)+'-'+str(month)

	try:
		#Convertimos la fechas de los input en dates de python
		onemonth = MonthDelta(1) #Creamos un delta de 1 mes
		dateone = datetime.strptime(date, "%Y-%m")
		nextmonth = dateone+onemonth #Le sumamos un dia a la fecha
	
		#Convertimos las fechas a string con formato AAAA-MM
		dateone = dateone.isoformat()[:7]
		nextmonth = nextmonth.isoformat()[:7]
	except ValueError:
		raise ValueError("Incorrect data format, should be YYYY-MM")

	if 'vessel2' in request.GET:
		vessel = request.GET['vessel2']

	if request.GET['vessel2'] in remolcadores:
		nombre = request.GET['vessel2']
		vessel = remolcadores[nombre]

	datereporter = datetime.now();
	vesselname = request.GET['vessel2']
	consumo = genMes(dateone, vessel)

	return render_to_response("month.html", locals())

#Generadores de consulta

def getRange(request):

	if 'dateone' in request.GET and 'datetwo' in request.GET and 'vessel' in request.GET:
		if(request.GET['dateone'] == '' or request.GET['datetwo'] == '' or request.GET['vessel'] == ''):
			return render_to_response("reportesitg.html")
		dateone = request.GET['dateone']
		datetwo = request.GET['datetwo']
		vessel = request.GET['vessel']
		try:
			#Convertimos la fechas de los input en dates de python
			oneday = timedelta(days=1) #Creamos un delta de 1 dia
			dateone = datetime.strptime(dateone, "%Y-%m-%d")
			datetwo = datetime.strptime(datetwo, "%Y-%m-%d")
			nextday = dateone+oneday #Le sumamos un dia a la fecha
		
			#Convertimos las fechas a string con formato AAAA-MM-DD
			dateone = dateone.isoformat()[:10]
			nextday = nextday.isoformat()[:10]
			datetwo = datetwo.isoformat()[:10]
		except ValueError:
			raise ValueError("Incorrect data format, should be YYYY-MM-DD")

	datereporter = date.today() #Fecha en que se realizo el reporte.
	return render_to_response("range.html", locals())

def genMes(dateone, vessel):

	#cursor.execute("select TimeString, DataCode, DataValue from [2160-DAQOnBoardData] where vesselid =  "+ str(vessel) +" and TimeString > '"+str(dateone)+"' and TimeString < '"+ str(datetwo) +"' and (DataCode = 'PRP000' or DataCode = 'PRP001' or DataCode = 'PRP002' or DataCode = 'PRS000' or DataCode = 'PRS001' or DataCode = 'PRS002' or DataCode = 'BOW001' or DataCode = 'BOW002' or DataCode = 'GEP001' or DataCode = 'GEP002' or DataCode = 'GES001' or DataCode = 'GES002');")
	consumos = []
	diaUno = dateone + "-" + "01"
	diaDos = dateone + "-" + "31"
	oneday = timedelta(days=1) #Creamos un delta de 1 dia
	
	while (diaUno <= diaDos):

		#Convertimos la fechas de los input en dates de python
		diaUno = datetime.strptime(diaUno, "%Y-%m-%d")
		tomorrow = diaUno+oneday #Le sumamos un dia a la fecha
	
		#Convertimos las fechas a string con formato AAAA-MM-DD
		diaUno = diaUno.isoformat()[:10]
		tomorrow = tomorrow.isoformat()[:10]

		cursor = connection.cursor()
		cursor.execute('select DataCode, DataValue from [2160-DAQOnBoardData] where vesselid =  '+ str(vessel) +' and TimeString > "'+str(diaUno)+'" and TimeString < "'+ str(tomorrow) +'";')
		rows = cursor.fetchall()
		cursor.close()

		prp000 = []
		prp001 = []
		prp002 = []
		prs000 = []
		prs001 = []
		prs002 = []
		bow001 = []
		bow002 = []
		gep001 = []
		gep002 = []
		ges001 = []
		ges002 = []

		for r in rows:
			if r[0] == "PRP000":
				if r[1] > 400:
					prp000.append(r[1])
			elif r[0] == "PRP001":
				prp001.append(r[1])
			elif r[0] == "PRP002":
				prp002.append(r[1])
			elif r[0] == "PRS000":
				if r[1] > 400:
					prs000.append(r[1])
			elif r[0] == "PRS001":
				prs001.append(r[1])
			elif r[0] == "PRS002":
				prs002.append(r[1])
			elif r[0] == "BOW001":
				bow001.append(r[1])
			elif r[0] == "BOW002":
				bow002.append(r[1])
			elif r[0] == "GEP001":
				gep001.append(r[1])
			elif r[0] == "GEP002":
				gep002.append(r[1])
			elif r[0] == "GES001":
				ges001.append(r[1])
			elif r[0] == "GES002":
				ges002.append(r[1])

		if len(prp002) == 0:
			consumoCombustiblePropBab = 0
		else: 
			consumoCombustiblePropBab = round((max(prp002) - min(prp002)) * 0.2641720512415584, 2)	
		if len(prp000) == 0:
			consumoHorasPropBab = 0
	 	else:
			consumoHorasPropBab = round(len(prp000) * 0.51666 / 60.0, 2)

		if len(prs002) == 0:
			consumoCombustiblePropEst = 0
		else:
			consumoCombustiblePropEst = round((max(prs002) - min(prs002)) * 0.2641720512415584, 2) 
		if len(prs000) == 0:
			consumoHorasPropEst = 0
		else:
			consumoHorasPropEst = round(len(prs000) * 0.51666 / 60.0, 2)

		if len(bow002) == 0:
			consumoCombustibleBow = 0
		else:
			consumoCombustibleBow = round((max(bow002) - min(bow002)) * 0.2641720512415584, 2) 
		if len(bow001) == 0:
			consumoHorasBow = 0
		else:
			consumoHorasBow = round((max(bow001) - min(bow001)), 2)

		if len(gep002) == 0:
			consumoCombustibleGenBab = 0
		else:
			consumoCombustibleGenBab = round((max(gep002) - min(gep002)) * 0.2641720512415584, 2) 
		if len(gep001) == 0:
			consumoHorasGenBab = 0
		else:
			consumoHorasGenBab = round((max(gep001) - min(gep001)), 2)

		if len(ges002) == 0:
			consumoCombustibleGenEst = 0
		else:
			consumoCombustibleGenEst = round((max(ges002) - min(ges002)) * 0.2641720512415584, 2) 
		if len(ges001) == 0:
			consumoHorasGenEst = 0
		else:
			consumoHorasGenEst = round((max(ges001) - min(ges001)), 2)

		total = consumoCombustiblePropBab + consumoCombustiblePropEst + consumoCombustibleBow + consumoCombustibleGenBab + consumoCombustibleGenEst
		consumos.append([consumoCombustiblePropBab, consumoHorasPropBab, consumoCombustiblePropEst, consumoHorasPropEst, consumoCombustibleBow, consumoHorasBow, consumoCombustibleGenBab, consumoHorasGenBab, consumoCombustibleGenEst, consumoHorasGenEst, total])

		diaUno = diaUno + oneday

	return consumos

def genDia(dateone, tomorrow, vessel):

	cursor = connection.cursor()
	cursor.execute('select DataCode, DataValue from [2160-DAQOnBoardData] where vesselid =  '+ str(vessel) +' and TimeString > "'+str(dateone)+'" and TimeString < "'+ str(tomorrow) +'";')
	rows = cursor.fetchall()
	cursor.close()

	prp000 = []
	prp001 = []
	prp002 = []
	prs000 = []
	prs001 = []
	prs002 = []
	bow001 = []
	bow002 = []
	gep001 = []
	gep002 = []
	ges001 = []
	ges002 = []

	for r in rows:
		if r[0] == "PRP000":
			if r[1] > 400:
				prp000.append(r[1])
		elif r[0] == "PRP001":
			prp001.append(r[1])
		elif r[0] == "PRP002":
			prp002.append(r[1])
		elif r[0] == "PRS000":
			if r[1] > 400:
				prs000.append(r[1])
		elif r[0] == "PRS001":
			prs001.append(r[1])
		elif r[0] == "PRS002":
			prs002.append(r[1])
		elif r[0] == "BOW001":
			bow001.append(r[1])
		elif r[0] == "BOW002":
			bow002.append(r[1])
		elif r[0] == "GEP001":
			gep001.append(r[1])
		elif r[0] == "GEP002":
			gep002.append(r[1])
		elif r[0] == "GES001":
			ges001.append(r[1])
		elif r[0] == "GES002":
			ges002.append(r[1])

	if len(prp002) == 0:
		consumoCombustiblePropBab = 0
	else: 
		consumoCombustiblePropBab = round((max(prp002) - min(prp002)) * 0.2641720512415584, 2)	
	if len(prp000) == 0:
		consumoHorasPropBab = 0
 	else:
		consumoHorasPropBab = round(len(prp000) * 0.51666 / 60.0, 2)

	if len(prs002) == 0:
		consumoCombustiblePropEst = 0
	else:
		consumoCombustiblePropEst = round((max(prs002) - min(prs002)) * 0.2641720512415584, 2) 
	if len(prs000) == 0:
		consumoHorasPropEst = 0
	else:
		consumoHorasPropEst = round(len(prs000) * 0.51666 / 60.0, 2)

	if len(bow002) == 0:
		consumoCombustibleBow = 0
	else:
		consumoCombustibleBow = round((max(bow002) - min(bow002)) * 0.2641720512415584, 2) 
	if len(bow001) == 0:
		consumoHorasBow = 0
	else:
		consumoHorasBow = round((max(bow001) - min(bow001)), 2)

	if len(gep002) == 0:
		consumoCombustibleGenBab = 0
	else:
		consumoCombustibleGenBab = round((max(gep002) - min(gep002)) * 0.2641720512415584, 2) 
	if len(gep001) == 0:
		consumoHorasGenBab = 0
	else:
		consumoHorasGenBab = round((max(gep001) - min(gep001)), 2)

	if len(ges002) == 0:
		consumoCombustibleGenEst = 0
	else:
		consumoCombustibleGenEst = round((max(ges002) - min(ges002)) * 0.2641720512415584, 2) 
	if len(ges001) == 0:
		consumoHorasGenEst = 0
	else:
		consumoHorasGenEst = round((max(ges001) - min(ges001)), 2)

	total = consumoCombustiblePropBab + consumoCombustiblePropEst + consumoCombustibleBow + consumoCombustibleGenBab + consumoCombustibleGenEst
	consumos = (consumoCombustiblePropBab, consumoHorasPropBab, consumoCombustiblePropEst, consumoHorasPropEst, consumoCombustibleBow, consumoHorasBow, consumoCombustibleGenBab, consumoHorasGenBab, consumoCombustibleGenEst, consumoHorasGenEst, total)

	return consumos