'''

This script is intended for a possible change of database from Mysql to Sqlite for its portable properties

'''

import sqlite3 as sqlite
import os
from time import sleep, clock

global connection
connection=None


dir_script=str(os.getcwd())
 
class data_base_instance:

	def connect(self):
		pass
		# global cursor_modify_data
		# global cursor_read_data
		# cursor_modify_data=connection.cursor()
		# cursor_read_data=connection.cursor()

	def read_data(self,table,fields,condition1,condition2):
		global read_data
		result=[]

		if condition1==None or condition2==None:
			query="SELECT "+fields+" FROM "+table
		else:
			query="SELECT "+fields+" FROM "+table+" WHERE "+str(condition1)+"='"+str(condition2)+"'"

		if condition1=="LAST":
			query="SELECT "+fields+" FROM "+table+" WHERE id in (SELECT MAX(id) from "+table+" GROUP BY "+condition2+")"

			# query="SELECT "+fields+" FROM "+table+" WHERE id=(SELECT max(id) FROM "+table+")"+" GROUP BY "+condition2
			# query="SELECT * FROM "+table+" ORDER BY "+condition2+" DESC LIMIT 1"
		try:
			connection = sqlite.connect(dir_script+"\Dynamic_sim_DB.db", check_same_thread=False)
			cursor2 = connection.cursor()
			cursor2.execute(query)


			reader=cursor2.fetchall()
			for data in reader:
				result.append(data)

			cursor2.close()
			connection.close()

			# cursor2.close()
		# except mysql.connector.Error as e:
		# 	print "ERROR %d IN connection: %s" % (e.args[0], e.args[1])
			# connection.close()
			# connection = mysql.connector.connect(**self.config)
			# cursor2 = connection.cursor()
			# cursor2.execute(query)


			# reader=cursor2.fetchall()
			# for data in reader:
			# 	result.append(data)

			# cursor2.close()


		return result

	def insert_data(self,table,fields,value):
		global insert_data


		insert_data=True

		values=str(value)[1:-1]

		query="INSERT INTO "+table+"("+fields+") VALUES ("+values+")"
		# sleep(0.0005)
		try:
			connection =sqlite.connect(dir_script+"\Dynamic_sim_DB.db", check_same_thread=False)
			cursor2 = connection.cursor()
			cursor2.execute(query)		
			connection.commit()
			cursor2.close()
			connection.close()
			# cursor2.close()
		except mysql.connector.Error as e:
			print "ERROR %d IN connection: %s" % (e.args[0], e.args[1])
			# connection.close()
			# connection = mysql.connector.connect(**self.config)
			# cursor2 = connection.cursor()
			# cursor2.execute(query)		
			# connection.commit()
			# cursor2.close()

		
	def update_data_run_time(self,table,fields,values,condition1,condition2):
		connection = sqlite.connect(dir_script+"\Dynamic_sim_DB.db", check_same_thread=False)
		cursor2 = connection.cursor()
		cursor2.execute("UPDATE "+table+" SET "+fields+"= '"+str(values)+"' WHERE "+str(condition1)+"='"+str(condition2)+"'")
		connection.commit()
		# cursor2.close()
		


	def update_data(self,table,fields,values,condition1,condition2):
		connection = sqlite.connect(dir_script+"\Dynamic_sim_DB.db", check_same_thread=False)
		query="UPDATE "+table+" SET "
		query2=""
		query3=" WHERE "+str(condition1)+"='"+str(condition2)+"'"
		for k,field_data in enumerate(fields):
			if k<(len(fields)-1):
				
				query2=field_data+"='"+str(values[k])+"', "+query2

			elif k==(len(fields)-1):

				query2=query2+field_data+"='"+str(values[k])+"'"

		queryT=query + query2+query3
		# print(queryT)
		cursor2 = connection.cursor()
		cursor2.execute(queryT)
		connection.commit()
		cursor2.close()
		connection.close()
		# cursor2.close()
		# for field_data,value_data,condition_data in zip(field,value,condition):
		# 	cursor.execute("UPDATE "+table+" SET "+str(field_data)+"= '"+str(value_data)+"' WHERE "+str(field_data)+"='"+str(condition_data)+"'")
		# 	connection.commit()

	def delete_data(self,table,field,condition):
		connection = sqlite.connect(dir_script+"\Dynamic_sim_DB.db", check_same_thread=False)
		cursor =connection.cursor()
		cursor.execute("DELETE FROM "+table+" WHERE "+field+"='"+str(condition)+"'")
		connection.commit()
		cursor.close()
		connection.close()

	def clear_table(self,table):
		connection = sqlite.connect(dir_script+"\Dynamic_sim_DB.db", check_same_thread=False)
		cursor_table = connection.cursor()
		cursor_table.execute("DELETE FROM "+table+" WHERE 1=1")
		connection.commit()
		cursor_table.execute("ALTER TABLE "+table+" AUTO_INCREMENT = 1")
		connection.commit()
		cursor_table.close()
		connection.close()

	def clear_all(self):
		connection=sqlite.connect(dir_script+"\Dynamic_sim_DB.db", check_same_thread=False)
		cursor_modify_data=connection.cursor()
		cursor_modify_data.execute("SELECT name FROM sqlite_master WHERE type='table';")
		tables = cursor_modify_data.fetchall()
		for table_name in tables:
			cursor_modify_data.execute("DELETE FROM "+str(table_name[0])+" WHERE 1=1")
			connection.commit()
		connection.close()
