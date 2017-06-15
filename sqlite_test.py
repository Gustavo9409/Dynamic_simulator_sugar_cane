import sqlite3 as sqlite
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
	
	while True:
		# sleep(1)
		
		if stop==True:
			x=db.read_data("TS","TIME_EXEC",None,None)
			for data in x:
				print ("Ts: "+data[0])
				if data[0]=='1.8':
					print ("FINAL")
					# db.disconnect()
					flag2=1
					# break
			# if flag2==1:
				# break

			flag=flag+1
		else:
			print"ACA"
		# con.close()

s=["TS"]
c=[1.8]
d=[3,4]
db.connect()
# db.delete("Empresa","Nombre","3")
# # db.update_data("EMPRESA",s,d,c)

# x=db.read_data("TS,TIME","TIME_EXEC","TS","0.5")
# s1t=x[0]
# s2t=x[1]
# print (x)
db.clear_all()
db.insert_data("TIME_EXEC",s,[1.7])
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
	if flag>=10000:
		# stop=False
		print ("AJAM")
		# sleep(0.05)
		db.insert_data("TIME_EXEC",s,c)
		# sleep(0.05)
		# stop=True
	