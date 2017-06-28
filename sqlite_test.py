import mysql.connector
from mysql.connector import errorcode
import os
global cursor
global con
global flag
import threading
from time import sleep, clock
from Data_base import data_base_instance
global cerrado
cerrado=0
flag=0
global stop
stop=True
db=data_base_instance()

def Thread_time():
	global flag
	global con
	global cursor
	global cerrado
	global stop
	flag2=0
	print("ACA223")
	while True:
		# sleep(1)
		
		if stop==True:
			# x=db.read_data("TIME_EXEC","TS",None,None)
			fields="TS"
			table="TIME_EXEC"
			query="SELECT "+fields+" FROM "+table
			db.cursor.execute(query)
			reader=db.cursor.fetchall()
			result=[]
			for data in reader:
				result.append(data)
			for data in result:
				print ("Ts: "+data[0])
				if data[0]=='1.8':
					print ("FINAL")
					# db.disconnect()
					flag2=1
					# break
			if flag2==1:
				break

			flag=flag+1
		else:
			print"ACA"
		# con.close()

s="TS"
c=[1.8]
d=[3,4]
db.connect()
# db.delete("Empresa","Nombre","3")
# # db.update_data("EMPRESA",s,d,c)

# x=db.read_data("TS,TIME","TIME_EXEC","TS","0.5")
# s1t=x[0]
# s2t=x[1]
# print (x)

db.cursor.execute("SELECT table_name FROM information_schema.tables where table_schema='Dynamic_sim_DB';")
tables = db.cursor.fetchall()
for table_name in tables:
	db.cursor.execute("DELETE FROM "+str(table_name[0])+" WHERE 1=1")
	db.connection.commit()
	db.cursor.execute("ALTER TABLE "+str(table_name[0])+" AUTO_INCREMENT = 1")
	db.connection.commit()

table="TIME_EXEC"
fields="TS"
valus=[1.7]
values=str(valus)[1:-1]
query="INSERT INTO "+table+"("+fields+") VALUES ("+values+")"
db.cursor.execute(query)
db.connection.commit()
# db.clear_all()
# print("ACA")
# db.insert_data("TIME_EXEC",s,[1.7])
# print("ACA")
# db.disconnect()

# dir_script=str(os.getcwd())
# con=sqlite.connect(dir_script+"\Data_base_dynamic_sim.s3db", check_same_thread=False)
# cursor=con.cursor()
# cerrado=0


# # cursor.execute("INSERT INTO EMPRESA (NOMBRE) VALUES('sLITE SA')")
# # cursor.execute("INSERT INTO EMPRESA (NOMBRE) VALUES('Gus SA')")

# con.commit()
Time_exec_thread =threading.Thread(target = Thread_time)
#Time_exec.setDaemon(True)
Time_exec_thread.start()

while True:
	print ("principal "+str(flag))
	# sleep(1)
	if flag>=10000:
		# stop=False
		print ("AJAM")
		# sleep(0.05)
		table="TIME_EXEC"
		fields="TS"
		valus=[1.8]
		values=str(valus)[1:-1]
		query="INSERT INTO "+table+"("+fields+") VALUES ("+values+")"
		db.cursor.execute(query)
		db.connection.commit()
		# db.insert_data("TIME_EXEC","TS",[1.8])
		
		# sleep(0.05)
		# stop=True
		break
	