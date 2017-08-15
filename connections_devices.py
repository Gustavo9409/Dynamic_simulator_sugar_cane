from global_data import *

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtCore import pyqtSignal

## Identify connections for "Convergencia" , "Divergencia" and "Tags"
def identify_connections():
	if hasattr(Devices,"array_connections"):
		for connections in Devices.array_connections:

			# if connections[1][:-1]=="Convergencia":
			# 	if connections[3]=="Entrada 1":
			# 		print(connections[1]+" Entrada1: "+connections[2]+" del "+connections[0])
			# 	if connections[3]=="Entrada 2":
			# 		print(connections[1]+" Entrada2: "+connections[2]+" del "+connections[0])

			if connections[1][:-1]=="TAG(Salida)":

				for items in Devices.panel_items:
					if items.name_block==connections[1]:
						label_Out_tag=str(items.label.toPlainText())
						print(label_Out_tag)

						for connections_ in Devices.array_connections:
							if connections_[0][:-1]=="TAG(Entrada)":
								for items in Devices.panel_items:
									if str(items.label.toPlainText())==label_Out_tag and items.name_block!=connections[1]:
										 
										new_connection=[connections[0],connections_[1],connections[2],connections_[3]]
										editor=items.editor
										editor.array_connections.append(new_connection)
										Devices.array_connections=editor.array_connections

										Devices.array_connections.remove(connections)
										Devices.array_connections.remove(connections_)

										print Devices.array_connections
				

# timer = QtCore.QTimer()
# timer.timeout.connect(identify_connections)
# timer.start(50)

