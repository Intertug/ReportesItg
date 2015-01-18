from django.shortcuts import render, render_to_response
from django.db import connection
from reports.models import *
from datetime import datetime

rmGlobal = "mistral"
tipoGlobal = "mecanico"
horometroVelMayorGlobal = 400.0

#Generadores de Templates

def getReportes(request):
	return render_to_response("reportes.html", locals())

def getDia(request):

	if 'fecha' in request.GET:
		date = request.GET['fecha']
	else:
		date = datetime.now()
	
	#consumo = genConsumoDia(request)
	consumo = genDia(request, date)

	return render_to_response("dia.html", locals())

def getMes(request):

	consumo = genMes()

	return render_to_response("mes.html", locals())

#Generadores de consulta

def genMes():

	cursor = connection.cursor()
	cursor.execute('select fechahora, codvariable, valor from datos where month(fechahora) = month(curdate());')
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

	auxprp000 = []
	auxprp001 = []
	auxprp002 = []
	auxprs000 = []
	auxprs001 = []
	auxprs002 = []
	auxbow001 = []
	auxbow002 = []
	auxgep001 = []
	auxgep002 = []
	auxges001 = []
	auxges002 = []

	for dia in range(30):
		for r in rows:
			if str(r[0]) >= "2015-01-" + str(dia) and str(r[0]) < "2015-01-" + str(dia + 1):
				if r[1] == "PRP000":
					if r[2] > 400:
						auxprp000.append(r[2])
				elif r[1] == "PRP001":
					auxprp001.append(r[2])
				elif r[1] == "PRP002":
					auxprp002.append(r[2])
				elif r[1] == "PRS000":
					if r[1] > 400:
						auxprs000.append(r[2])
				elif r[1] == "PRS001":
					auxprs001.append(r[2])
				elif r[1] == "PRS002":
					auxprs002.append(r[2])
				elif r[1] == "BOW001":
					auxbow001.append(r[2])
				elif r[1] == "BOW002":
					auxbow002.append(r[2])
				elif r[1] == "GEP001":
					auxgep001.append(r[2])
				elif r[1] == "GEP002":
					auxgep002.append(r[2])
				elif r[1] == "GES001":
					auxges001.append(r[2])
				elif r[1] == "GES002":
					auxges002.append(r[2])

		prp000.append(auxprp000)
		prp001.append(auxprp001)
		prp002.append(auxprp002)
		prs000.append(auxprs000)
		prs001.append(auxprs001)
		prs002.append(auxprs002)
		bow001.append(auxbow001)
		bow002.append(auxbow002)
		gep001.append(auxgep001)
		gep002.append(auxgep002)
		ges001.append(auxges001)
		ges002.append(auxges002)

		auxprp000 = []
		auxprp001 = []
		auxprp002 = []
		auxprs000 = []
		auxprs001 = []
		auxprs002 = []
		auxbow001 = []
		auxbow002 = []
		auxgep001 = []
		auxgep002 = []
		auxges001 = []
		auxges002 = []								


	return prp000

def genDia(request, date):

	cursor = connection.cursor()
	cursor.execute('select codvariable, valor from datos where dayofyear(fechahora) = dayofyear("'+str(date)+'");')
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


def genConsumoDia(request):

	if 'fecha' in request.GET:
		fecha = request.GET['fecha']

		consumoFuelBaborProp = genConsumoGalones(llenarMatriz(genReporteDiaConsulta(fecha, 'PRP002')))
		
		if tipoGlobal != "mecanico":
			consumoHorasBaborProp = genConsumo(llenarMatriz(genReporteDiaConsulta(fecha, 'PRP001')))
			consumoHorasEstriborProp = genConsumo(llenarMatriz(genReporteDiaConsulta(fecha, 'PRS001')))
		else:
			consumoHorasBaborProp = genConsumoHoras(llenarMatriz(genHorometroDiaConsulta(fecha, 'PRP000')))
			consumoHorasEstriborProp = genConsumoHoras(llenarMatriz(genHorometroDiaConsulta(fecha, 'PRS000')))

		consumoFuelEstriborProp = genConsumoGalones(llenarMatriz(genReporteDiaConsulta(fecha, 'PRS002')))

		consumoFuelBowProp = genConsumoGalones(llenarMatriz(genReporteDiaConsulta(fecha, 'BOW002')))
		consumoHorasBowProp = genConsumo(llenarMatriz(genReporteDiaConsulta(fecha, 'BOW001')))

		consumoFuelBaborGen = genConsumoGalones(llenarMatriz(genReporteDiaConsulta(fecha, 'GEP002')))
		consumoHorasBaborGen = genConsumo(llenarMatriz(genReporteDiaConsulta(fecha, 'GEP001')))

		consumoFuelEstriborGen = genConsumoGalones(llenarMatriz(genReporteDiaConsulta(fecha, 'GES002')))
		consumoHorasEstriborGen = genConsumo(llenarMatriz(genReporteDiaConsulta(fecha, 'GES001')))

	else:
		consumoFuelBaborProp = genConsumoGalones(llenarMatriz(genReporteDia('PRP002')))
		
		if tipoGlobal != "mecanico":
			consumoHorasBaborProp = genConsumo(llenarMatriz(genReporteDia('PRP001')))
			consumoHorasEstriborProp = genConsumo(llenarMatriz(genReporteDia('PRS001')))
		else:
			consumoHorasBaborProp = genConsumoHoras(llenarMatriz(genHorometroDia('PRP000')))
			consumoHorasEstriborProp = genConsumoHoras(llenarMatriz(genHorometroDia('PRS000')))

		consumoFuelEstriborProp = genConsumoGalones(llenarMatriz(genReporteDia('PRS002')))

		consumoFuelBowProp = genConsumoGalones(llenarMatriz(genReporteDia('BOW002')))
		consumoHorasBowProp = genConsumo(llenarMatriz(genReporteDia('BOW001')))

		consumoFuelBaborGen = genConsumoGalones(llenarMatriz(genReporteDia('GEP002')))
		consumoHorasBaborGen = genConsumo(llenarMatriz(genReporteDia('GEP001')))

		consumoFuelEstriborGen = genConsumoGalones(llenarMatriz(genReporteDia('GES002')))
		consumoHorasEstriborGen = genConsumo(llenarMatriz(genReporteDia('GES001')))	

	totalConsumoCombustible = consumoFuelBaborProp + consumoFuelEstriborProp + consumoFuelBowProp + consumoFuelBaborGen + consumoFuelEstriborGen

	matriz = (consumoFuelBaborProp, consumoHorasBaborProp, consumoFuelEstriborProp, consumoHorasEstriborProp, consumoFuelBowProp, consumoHorasBowProp, consumoFuelBaborGen, consumoHorasBaborGen, consumoFuelEstriborGen, consumoHorasEstriborGen, totalConsumoCombustible)

	return matriz

#sentencia a la BD

def genReporteDiaConsulta(fecha, dato):

	cursor = connection.cursor()
	cursor.execute('select valor from datos where rm ="'+str(rmGlobal)+'" and codvariable="'+str(dato)+'" and dayofyear(fechahora) = dayofyear("'+str(fecha)+'");')
	rows = cursor.fetchall()
	cursor.close()

	return rows

def genReporteDia(dato):

	cursor = connection.cursor()
	cursor.execute('select valor from datos where rm ="'+str(rmGlobal)+'" and codvariable="'+str(dato)+'" and dayofyear(fechahora) = dayofyear(curdate());')
	rows = cursor.fetchall()
	cursor.close()

	return rows

def genHorometroDiaConsulta(fecha, dato):

	cursor = connection.cursor()
	cursor.execute('select valor from datos where rm ="'+str(rmGlobal)+'" and codvariable="'+str(dato)+'" and dayofyear(fechahora) = dayofyear("'+str(fecha)+'") and valor > '+str(horometroVelMayorGlobal)+';')
	rows = cursor.fetchall()
	cursor.close()

	return rows

def genHorometroDia(dato):

	cursor = connection.cursor()
	cursor.execute('select valor from datos where rm ="'+str(rmGlobal)+'" and codvariable="'+str(dato)+'" and dayofyear(fechahora) = dayofyear(curdate()) and valor > '+str(horometroVelMayorGlobal)+';')
	rows = cursor.fetchall()
	cursor.close()

	return rows

#Auxiliares 

def llenarMatriz(rows):
	
	matriz = []
	for i in range(len(rows)):
		if rows[i][0] != 0:
			matriz.append(rows[i][0])

	return matriz

def genConsumo(rows):

	if not rows:
		rows = 0
		return rows
	else:
		maximo = max(rows)
		minimo = min(rows)
		consumo = maximo - minimo
		consumo = round(consumo, 2)
		return consumo

def genConsumoHoras(rows):

	if not rows:
		rows = 0
		return rows
	else:
		cont = len(rows)
		valor = (cont * 0.5) / 60.0 
		valor = round(valor, 2)
		return valor

def genConsumoGalones(rows):

	if not rows:
		rows = 0
		return rows
	else:
		maximo = max(rows)
		minimo = min(rows)
		consumo = maximo - minimo
		consumo = consumo * 0.2641720512415584
		consumo = round(consumo, 2)
		return consumo