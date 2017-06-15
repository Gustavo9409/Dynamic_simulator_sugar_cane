import sqlite3 as sqlite
import os
from time import sleep, clock

global connection
connection=None


dir_script=str(os.getcwd())
 
class data_base_instance:

	def connect(self):
		global connection
		# global cursor_modify_data
		# global cursor_read_data


		connection=sqlite.connect(dir_script+"\Dynamic_sim_DB.db", check_same_thread=False)
		return connection
		# cursor_modify_data=connection.cursor()
		# cursor_read_data=connection.cursor()

	def disconnect(self):
		connection.close()

	def read_data(self,cursor,fields,table,condition1,condition2):
		result=[]
		if condition1==None or condition2==None:
			query="SELECT "+fields+" FROM "+table
		else:
			query="SELECT "+fields+" FROM "+table+" WHERE "+str(condition1)+"='"+str(condition2)+"'"
		# sleep(0.0005)
		cursor.execute(query)
		# sleep(0.0005)
		for data in cursor:
			result.append(data)
		return result

	def insert_data(self,cursor,table,field,value):		
		fields=str(field)[1:-1]
		values=str(value)[1:-1]
		# sleep(0.05)
		cursor.execute("INSERT INTO "+table+" ("+fields+") VALUES("+values+")")
		connection.commit()
		# sleep(0.05)
		

	def update_data(self,cursor,table,field,value,condition):

		for field_data,value_data,condition_data in zip(field,value,condition):
			print (field_data)
			cursor.execute("UPDATE "+table+" SET "+str(field_data)+"= '"+str(value_data)+"' WHERE "+str(field_data)+"='"+str(condition_data)+"'")
			connection.commit()

	def delete_data(self,cursor,table,field,condition):
		cursor.execute("DELETE FROM "+table+" WHERE "+str(field)+"='"+str(condition)+"'")
		connection.commit()

	def clear_all(self):
		cursor_modify_data=connection.cursor()
		cursor_modify_data.execute("SELECT name FROM sqlite_master WHERE type='table';")
		tables = cursor_modify_data.fetchall()
		for table_name in tables:
			cursor_modify_data.execute("DELETE FROM "+str(table_name[0])+" WHERE 1=1")
			connection.commit()
