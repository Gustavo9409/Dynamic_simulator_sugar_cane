import mysql.connector
import datetime;
from mysql.connector import errorcode

from time import sleep, clock

 
class data_base_instance:

	def connect(self):
		

		self.config = {
			'user': 'root',
			'password': '1234',
			'host': 'localhost',
			'database': 'Dynamic_sim_DB',
			}

		# self.connection = mysql.connector.connect(**self.config)
		# self.cursor = self.connection.cursor()
		# return connection

	def disconnect(self):
		connection.close()
		# return connection

	def read_data(self,table,fields,condition1,condition2):
		global read_data
		result=[]

		if condition1==None or condition2==None:
			query="SELECT "+fields+" FROM "+table
		else:
			query="SELECT "+fields+" FROM "+table+" WHERE "+str(condition1)+"='"+str(condition2)+"'"
		try:
			connection = mysql.connector.connect(**self.config)
			cursor2 = connection.cursor()
			cursor2.execute(query)


			reader=cursor2.fetchall()
			for data in reader:
				result.append(data)

			cursor2.close()
			connection.close()

			# cursor2.close()
		except mysql.connector.Error as e:
			print "ERROR %d IN connection: %s" % (e.args[0], e.args[1])
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
			connection = mysql.connector.connect(**self.config)
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
		connection = mysql.connector.connect(**self.config)
		cursor2 = connection.cursor()
		cursor2.execute("UPDATE "+table+" SET "+fields+"= '"+str(values)+"' WHERE "+str(condition1)+"='"+str(condition2)+"'")
		connection.commit()
		# cursor2.close()
		


	def update_data(self,table,fields,values,condition1,condition2):
		connection = mysql.connector.connect(**self.config)
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
		connection = mysql.connector.connect(**self.config)
		cursor =connection.cursor()
		cursor.execute("DELETE FROM "+table+" WHERE "+field+"='"+str(condition)+"'")
		connection.commit()
		cursor.close()
		connection.close()

	def clear_table(self,table):
		connection = mysql.connector.connect(**self.config)
		cursor_table = connection.cursor()
		cursor_table.execute("DELETE FROM "+table+" WHERE 1=1")
		connection.commit()
		cursor_table.execute("ALTER TABLE "+table+" AUTO_INCREMENT = 1")
		connection.commit()
		cursor_table.close()
		connection.close()

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

# db=data_base_instance()
# db.connect()
# tt=[]
# model_value=[]
# time_exec=db.read_data("TIME_EXEC","TIME",None,None)
# time=list(time_exec)
# for data in time:
# 	if data[0]!="stop":
# 		tt.append(float(data[0]))
# output=db.read_data("OUTPUTS_HEATER","Time_exec_id,Out_fluid_temperature","Heaters_id",1)
# Tout=list(output)
# time_array=[]
# for data in Tout:
# 	time_array.append(float(data[0]))
# for data in Tout:
# 	if time_array[0]!=time_array[1]:
# 		model_value.append(float(data[1]))

# print (str(len(tt)))
# print (str(len(model_value)))
# try:
# 	c = a.cursor()
# except mysql.connector.Error as e:
#     print "ERROR %d IN connection: %s" % (e.args[0], e.args[1])
# else:
# 	print("connect")
# b=db.disconnect()
# try:
# 	c = a.cursor()
# except mysql.connector.Error as e:
#     print "ERROR %d IN connection: %s" % (e.args[0], e.args[1])
# else:
# 	print("connect")
# # fields="Name,_Type,Flow,Temperature,Brix,Purity,Insoluble_solids,pH,Pressure,Saturated_vapor"
# result=db.read_data("Flow_inputs",fields,None,None)
# if len(result)>0:
# 		for data in result:
# 			for i,values in enumerate(data):
# 				print values
# db.insert_data("TIME_EXEC","Ts",[0.5])
# db.update_data("TIME_EXEC",["Ts","time"],[0.87,90],"id",1)
# res=db.read_data("TIME_EXEC","Ts,time",None,None)
# print (res)
# db.clear_all()