#!/usr/bin/python
# -*- coding: utf-8 -*-


import mysql.connector
from mysql.connector import errorcode
import sys

config = {
'user': 'root',
'password': '1234',
'host': 'localhost',
'database': 'Dynamic_sim_DB',
}

print("|*|*|*|* PRUEBA BASE DE DATOS CON MYSQL *|*|*|*| \n")
print("Configuración de conección: ")
print("User: root ")
print("Password: 1234 ")
print("Host: localhost ")
print("Database: Dynamic_sim_DB \n")
try:

	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()


except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Something is wrong with your user name or password")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database does not exist")
	else:
		print(err)
else:
	cursor.execute("SELECT VERSION()")
	print ("---- Version de Base de Datos ----")
	for (version) in cursor:
		print version[0]
	cursor.execute("SELECT table_name FROM information_schema.tables where table_schema='Dynamic_sim_DB';")
	tables = cursor.fetchall()
	print ("\n####### TABLAS EN BASE DE DATOS #######\n")
	for table_name in tables:
		print table_name[0]
	cursor.close()
	cnx.close()
	


