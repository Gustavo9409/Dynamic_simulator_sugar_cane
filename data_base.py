# Installed Libs
import mysql.connector
import datetime;
from mysql.connector import errorcode
from time import sleep, clock

#Database class
class data_base_instance:
	
	# Parameters for acces to data base
	def connect(self):
		
		self.config = {
			'user': 'root',
			'password': '1234',
			'host': 'localhost',
			'database': 'Dynamic_sim_DB',
			}

	# Read data to data base with search conditions
	def read_data(self,table,fields,condition1,condition2):
		result=[]

		if condition1==None or condition2==None:
			query="SELECT "+fields+" FROM "+table
		else:
			query="SELECT "+fields+" FROM "+table+" WHERE "+str(condition1)+"='"+str(condition2)+"'"

		if condition1=="LAST":
			query="SELECT "+fields+" FROM "+table+" WHERE id in (SELECT MAX(id) from "+table+" GROUP BY "+condition2+")"

		try:
			connection = mysql.connector.connect(**self.config)
			cursor = connection.cursor()
			cursor.execute(query)


			reader=cursor.fetchall()
			for data in reader:
				result.append(data)

			cursor.close()
			connection.close()

		except mysql.connector.Error as e:
			print "ERROR %d IN connection: %s" % (e.args[0], e.args[1])

		return result


	# Insert data to data base 
	def insert_data(self,table,fields,value):

		values=str(value)[1:-1]

		query="INSERT INTO "+table+"("+fields+") VALUES ("+values+")"

		try:
			connection = mysql.connector.connect(**self.config)
			cursor = connection.cursor()
			cursor.execute(query)		
			connection.commit()
			cursor.close()
			connection.close()
			
		except mysql.connector.Error as e:
			print "ERROR %d IN connection: %s" % (e.args[0], e.args[1])


	# Update table data in the data base
	def update_data(self,table,fields,values,condition1,condition2):
		connection = mysql.connector.connect(**self.config)
		query="UPDATE "+table+" SET "
		query2=""
		if len(condition1)>1:
			query3=" WHERE ("+str(condition1[0])+"='"+str(condition2[0])+"' and "+str(condition1[1])+"='"+str(condition2[1])+"')"
		else:
			query3=" WHERE "+str(condition1[0])+"='"+str(condition2[0])+"'"
		for k,field_data in enumerate(fields):
			if k<(len(fields)-1):
				
				query2=field_data+"='"+str(values[k])+"', "+query2

			elif k==(len(fields)-1):

				query2=query2+field_data+"='"+str(values[k])+"'"

		queryT=query+query2+query3

		cursor = connection.cursor()
		cursor.execute(queryT)
		connection.commit()
		cursor.close()
		connection.close()

	# Delete table data in the data base with a condition
	def delete_data(self,table,field,condition):
		connection = mysql.connector.connect(**self.config)
		cursor =connection.cursor()
		cursor.execute("DELETE FROM "+table+" WHERE "+field+"='"+str(condition)+"'")
		connection.commit()
		cursor.close()
		connection.close()

	# Clear data for specific table
	def clear_table(self,table):
		connection = mysql.connector.connect(**self.config)
		cursor_table = connection.cursor()
		cursor_table.execute("DELETE FROM "+table+" WHERE 1=1")
		connection.commit()
		cursor_table.execute("ALTER TABLE "+table+" AUTO_INCREMENT = 1")
		connection.commit()
		cursor_table.close()
		connection.close()

	# Clear data for all tables
	def clear_all(self):
		connection = mysql.connector.connect(**self.config)
		cursor = connection.cursor()
		cursor.execute("SELECT table_name FROM information_schema.tables where table_schema='Dynamic_sim_DB';")
		tables = cursor.fetchall()
		for table_name in tables:
			cursor.execute("DELETE FROM "+str(table_name[0])+" WHERE 1=1")
			connection.commit()
			cursor.execute("ALTER TABLE "+str(table_name[0])+" AUTO_INCREMENT = 1")
			connection.commit()
		cursor.close()
		connection.close()
