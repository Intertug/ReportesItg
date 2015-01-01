# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Datos(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    rm = models.CharField(max_length=15, blank=True)
    fechahora = models.DateTimeField(blank=True, null=True)
    codvariable = models.CharField(max_length=10, blank=True)
    valor = models.FloatField(blank=True, null=True)
    transaccion = models.IntegerField(blank=True, null=True)
    respuesta = models.CharField(max_length=10, blank=True)

    class Meta:
        managed = False
        db_table = 'datos'


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Generador(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    rm = models.CharField(max_length=15, blank=True)
    side = models.CharField(max_length=10, blank=True)
    fechahora = models.DateTimeField(blank=True, null=True)
    percentload = models.FloatField(blank=True, null=True)
    enginespeed = models.FloatField(blank=True, null=True)
    totalhours = models.FloatField(blank=True, null=True)
    totalfuel = models.FloatField(blank=True, null=True)
    coolanttemperature = models.FloatField(blank=True, null=True)
    fuelpressure = models.FloatField(blank=True, null=True)
    fuelrate = models.FloatField(blank=True, null=True)
    manifoldtemperature = models.FloatField(blank=True, null=True)
    batterypotential = models.FloatField(blank=True, null=True)
    disponible1 = models.FloatField(blank=True, null=True)
    disponible2 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'generador'


class Gps(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    rm = models.CharField(max_length=15, blank=True)
    fechahora = models.DateTimeField(blank=True, null=True)
    latitud = models.FloatField(blank=True, null=True)
    latitudns = models.CharField(db_column='latitudNS', max_length=1, blank=True)  # Field name made lowercase.
    longitud = models.FloatField(blank=True, null=True)
    longitudew = models.CharField(db_column='longitudEW', max_length=1, blank=True)  # Field name made lowercase.
    velocidad = models.FloatField(blank=True, null=True)
    direccion = models.FloatField(blank=True, null=True)
    pdop = models.FloatField(blank=True, null=True)
    hdop = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gps'


class Propulsor(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    rm = models.CharField(max_length=15, blank=True)
    side = models.CharField(max_length=10, blank=True)
    fechahora = models.DateTimeField(blank=True, null=True)
    percentload = models.FloatField(blank=True, null=True)
    enginespeed = models.FloatField(blank=True, null=True)
    airfilter2differentialpressure = models.FloatField(blank=True, null=True)
    exhaustgasrighttemperature = models.FloatField(blank=True, null=True)
    exhaustgaslefttemperature = models.FloatField(blank=True, null=True)
    fuelfiltersuctiondifferentialpressure = models.FloatField(blank=True, null=True)
    prefilteroilpressure = models.FloatField(blank=True, null=True)
    totalidlefuelused = models.FloatField(blank=True, null=True)
    totalidlehours = models.FloatField(blank=True, null=True)
    totalhours = models.FloatField(blank=True, null=True)
    totalfuel = models.FloatField(blank=True, null=True)
    coolanttemperature = models.FloatField(blank=True, null=True)
    intercoolertemperature = models.FloatField(blank=True, null=True)
    fuelpressure = models.FloatField(blank=True, null=True)
    oilpressure = models.FloatField(blank=True, null=True)
    fuelrate = models.FloatField(blank=True, null=True)
    airfilter1differentialpressure = models.FloatField(blank=True, null=True)
    electricpotentialvoltage = models.FloatField(blank=True, null=True)
    transmissionoilpressure = models.FloatField(blank=True, null=True)
    transmissionoiltemperature = models.FloatField(blank=True, null=True)
    fuelfilterdifferentialpressure = models.FloatField(blank=True, null=True)
    oilfilterdifferentialpressure = models.FloatField(blank=True, null=True)
    oiltemperature = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'propulsor'
