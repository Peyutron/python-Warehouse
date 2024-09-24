## Clase para tomar los datos desde "class_server_adxl345"
## Interface: Tkinter

import tkinter as tk
from tkinter import ttk
import threading
import time
from class_cliente_adxl345 import *


# Constantes de calibración

XMIN = float(-10.36)
XMAX = float(9.92)
YMIN = float(-10.70)
YMAX = float(10.20)
ZMIN = float(-7.50)
ZMAX = float( 12.87)


# Clase principal para ADXL axis
class mainADXL(tk.Tk):
	def __init__(self):
		super().__init__()

		self.__connOnOff = False
		self.__connAlive = False
		self._countdatareceived = 0
		self.cvHeight = 600
		self.cvWidth = 600
		self.Xaxis = 0
		self.Yaxis = 0
		self.Zaxis = 0
		self.valxmin = 0
		self.valymin = 0
		self.valzmin = 0
		self.valxmax = 0
		self.valymax = 0
		self.valzmax = 0
		self.listax = []
		self.listay = []
		self.listaz = []
		
		self.showXaxis = True
		self.showYaxis = True
		self.showZaxis = True

		self.txtIPStr = tk.StringVar()
		self.lbConnecionString = tk.StringVar()
		self.btnConnecionString = tk.StringVar()
		
		#--------------
		self.lbDataString = tk.StringVar()
		self.lbDataXString = tk.StringVar()
		self.lbDataYString = tk.StringVar()
		self.lbDataZString = tk.StringVar()
		self.mainInterface()
		self.frameConnection()
		self.frameInfoADXL()
		self.frameSelectLineADXL()


	## Interfaz principal con widget canvas
	## Activa el hilo para la comunicación con la clase class_cliente_adxl345
	## Geometría: 1015x645
	def mainInterface(self):

		self.title("ADXL345 axis")
		self.geometry('1015x645')

		self.screen = tk.LabelFrame(self, text="Coordenadas X Y Z")
		self.screen.grid(row= 0, column=0, rowspan=4, padx=10, pady=10)
			
		self.canvas = tk.Canvas(self.screen, width=self.cvWidth, 
											height=self.cvHeight, background='#000000')
		self.canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

		self.cvlineX = self.canvas.create_line(self.cvWidth/2, self.cvHeight, self.cvWidth/2, 0, fill="#0000FF", width=3) # Blue
		self.cvlineY = self.canvas.create_line(self.cvWidth, self.cvHeight/2, 0, self.cvHeight/2, fill="#008000", width=3) # Green
		self.cvlineZ = self.canvas.create_line(0, self.cvHeight, self.cvWidth, self.cvHeight, fill="#800080", width=3) # Purple
	
		# Activa el hilo para la comunicación
		self.hiloADXL = threading.Thread(target=lambda : self.connection(), daemon=True)
       	
		# Inicia hilo ADXL
		self.hiloADXL.start() 

	## LabelFrame que contiene los widgets del apartado de comunicación
	## Entry, Button, Label
	def frameConnection(self):
		self.infoConnection = tk.LabelFrame(self, text="Socket connection")
		self.infoConnection.grid(row= 0, column=1, pady=25, sticky=tk.N+tk.W+tk.E)
		
		self.txtIP = ttk.Entry(master=self.infoConnection, 
										textvariable=self.txtIPStr, 
										width=20)
		self.txtIP.grid(row=0, column=0, padx=10, pady=5, sticky=tk.N+tk.W)
		self.txtIPStr.set("192.168.1.36")
		
		self.btnStartSocket = ttk.Button(master=self.infoConnection, 
											textvariable=self.btnConnecionString,
											command=lambda: self.conexionWifiOnOff())
		self.btnConnecionString.set("Start Conn")
		self.btnStartSocket.grid(row=1, column=0, padx=10, pady=5, sticky=tk.N+tk.W)

		
		self.lbConnection = ttk.Label(master=self.infoConnection, 
										textvariable=self.lbConnecionString, 
										width=20)
		self.lbConnection.grid(row=2, column=0, padx=10, ipady=5, sticky=tk.W)
		self.lbConnecionString.set("Not connected")

	## LablelFrame que contiene los widgets para mostrar la información del sensor
	## Label
	def frameInfoADXL(self):

		self.infoADXL = tk.LabelFrame(self, text="ADXL345 received data")
		self.infoADXL.grid(row= 1, column=1, padx=10, sticky=tk.N+tk.W+tk.E)

		self.lbDataIn = ttk.Label(master=self.infoADXL, 
									textvariable=self.lbDataString,
									font=('Helvetica bold', 10),
									width=20)
		self.lbDataIn.grid(row=3, column=0, padx=5, sticky=tk.W)
		self.lbDataString.set("No ADXL data")

		self.lbDataX = ttk.Label(master=self.infoADXL, 
									textvariable=self.lbDataXString, 
									width=20)
		self.lbDataX.grid(row=4, column=0, padx=5, sticky=tk.W)
		self.lbDataXString.set("data X:")

		self.lbDataY = ttk.Label(master=self.infoADXL, 
									textvariable=self.lbDataYString, 
									width=20)
		self.lbDataY.grid(row=5, column=0, padx=5, sticky=tk.W)
		self.lbDataYString.set("data Y:")

		self.lbDataZ = ttk.Label(master=self.infoADXL, 
									textvariable=self.lbDataZString, 
									width=20)
		self.lbDataZ.grid(row=6, column=0, padx=5, sticky=tk.W)
		self.lbDataZString.set("data Z:")

	## LabelFrame dentro de "frameInfoADXL" donde se puede seleccionar que lineas
	## se van a representar en el canvas de "mainInterface".
	## CheckButtons
	def frameSelectLineADXL(self):
		self.varcbX = tk.IntVar()
		self.varcbY = tk.IntVar()
		self.varcbZ = tk.IntVar()

		self.frselectLine = tk.LabelFrame(self.infoADXL, text="Show data")
		self.frselectLine.grid(row=7, column=0, padx=10, pady=10, ipadx=10, sticky=tk.N+tk.W+tk.E)
		

		self.cbX = tk.Checkbutton(master=self.frselectLine, 
									text="Show X axis", 
									variable=self.varcbX, 
									onvalue=1, 
									offvalue=0, 
									command=lambda: self.selectLine(1))
		self.cbX.grid(row=0, column=0)
		if self.showXaxis:
			self.cbX.select()

		self.cbY = tk.Checkbutton(master=self.frselectLine, 
									text="Show Y axis", 
									variable=self.varcbY, 
									onvalue=1,
									offvalue=0,									
									command=lambda: self.selectLine(2))
		self.cbY.grid(row=0, column=1)
		if self.showYaxis:
			self.cbY.select()


		self.cbZ = tk.Checkbutton(master=self.frselectLine, 
									text="Show Z axis", 
									variable=self.varcbZ, 
									onvalue=1, 
									offvalue=0,
									command=lambda: self.selectLine(3))
		self.cbZ.grid(row=0, column=2)
		if self.showZaxis:
			self.cbZ.select()

	## Selecciona la linea que se va a mostrar en widget canvas. 
	## llamada desde "self.cbX", "self.cbY" y "self.cbZ" en la 
	## función "frameSelectLineADXL".
	# @ n_cb: Int - Número de linea 1-X, 2-Y y 3Z.
	def selectLine(self, n_cb):
		if n_cb == 1:
			self.showXaxis^=True
		if n_cb == 2:
			self.showYaxis^=True			
		if n_cb == 3:
			self.showZaxis^=True			

	## Modifica el eje X en la pantalla.
	# @ lineX: Int - valor del eje X
	def changeLineX(self, lineX):
		if self.showXaxis:
			lineX = self.mapRange(lineX, XMIN, XMAX, -self.cvWidth/2, self.cvWidth/2)
			lineX = float(lineX)
			lineX = int(lineX)
			self.Xaxis = lineX
			#self.canvas.coords(self.lineX, (100 - lineX), 200, (100 + lineX), 0 )
			self.canvas.coords(self.cvlineX, self.cvHeight, ((self.cvWidth/2) + lineX), 0, ((self.cvHeight/2) - lineX))


			if self.valxmin > lineX:
				self.valxmin = lineX
			if self.valxmax < lineX:
				self.valxmax = lineX

			self.lbDataXString.set(f"X: {lineX} min: {self.valxmin} max: {self.valxmax}")

		else:
			self.canvas.coords(self.cvlineX, 0, 0, 0, 0 )
			self.lbDataXString.set(f"X: NOT SHOW")

	## Modifica el eje Y en la pantalla.
	# @ lineY: Int - valor del eje Y
	def changeLineY(self, lineY):
		if self.showYaxis:	

			lineY = float(lineY)
			lineY = self.mapRange(lineY, YMIN, YMAX, -self.cvHeight/2, self.cvHeight/2)
			lineY = int(lineY)
			self.Yaxis = lineY

			self.canvas.coords(self.cvlineY, 
									0, 
									lineY + self.cvHeight/2,  
									self.cvWidth , 
									lineY + self.cvHeight/2)


			if self.valymin > lineY:
				self.valymin = lineY
			if self.valymax < lineY:
				self.valymax = lineY
	
			self.lbDataYString.set(f"Y: {lineY} min: {self.valymin} max: {self.valymax} ")

		else:
			self.canvas.coords(self.cvlineY, 0, 0, 0, 0 )
			self.lbDataYString.set(f"Y: NOT SHOW")

	## Modifica el eje Z en la pantalla.
	# @ lineZ: Int - valor del eje Z
	def changeLineZ(self, lineZ):
		if self.showZaxis:
			
			lineZ = float(lineZ)
			lineZ = int(self.mapRange(lineZ, ZMIN, ZMAX, -self.cvWidth/2, self.cvWidth/2))
			if lineZ < self.cvWidth/2 or lineZ < -self.cvWidth/2: 
				linez = self.cvWidth;
			self.canvas.coords(self.cvlineZ, 
									0,  
									lineZ + self.cvHeight/2, 
									self.cvWidth, 
									lineZ + self.cvHeight/2)

			if self.valzmin > lineZ:
				self.valzmin = lineZ
			if self.valzmax < lineZ:
				self.valzmax = lineZ
	
			self.lbDataZString.set(f"Z: {lineZ} min: {self.valzmin} max: {self.valzmax} ")
		else:
			self.canvas.coords(self.cvlineZ, 0, 0, 0, 0 )
			self.lbDataZString.set(f"Z: NOT SHOW")

	## Cambia el valor de canvas entre blanco amarillo y rojo.
	## TEST 
	def bgCanvasColor(self):


		if self.Xaxis > self.cvWidth/2 - 130 or self.Yaxis > self.cvWidth/2 + 130 or self.Xaxis < -self.cvWidth/2 + 130 or self.Yaxis < -self.cvHeight/2 + 130:
			self.canvas.configure(bg='red')
		elif self.Xaxis > self.cvWidth/2 - 170 or self.Yaxis > self.cvWidth/2 + 170 or self.Xaxis < -self.cvWidth/2 + 170 or self.Yaxis < -self.cvHeight/2 + 170:
			self.canvas.configure(bg='yellow')
		else:
			self.canvas.configure(bg='black')

	## Elimina los caracteres que no se usan y separa los valores del String.
	# @ dataRecv: String - Datos recibidos por hilo en la función "connection".
	def decodeADXL(self, dataRecv):
		dataRecv = dataRecv.replace("<adxl", "").replace(">", "")
		self.lbDataString.set(dataRecv) 
		datas = dataRecv.split(" ")

		if self._countdatareceived < 4:
			for ids, data in enumerate(datas):
				if ids == 1:
					self.listax.append(float(data))
				elif ids == 2:
					self.listay.append(float(data))					
				elif ids == 3:
					self.listaz.append(float(data))
			self._countdatareceived += 1
		else: 
			self.changeLineX(sum(self.listax) / len(self.listax))
			self.changeLineY(sum(self.listay) / len(self.listay))
			self.changeLineZ(sum(self.listaz) / len(self.listaz))
			self._countdatareceived = 0
			self.listax.clear()
			self.listay.clear()
			self.listaz.clear()

	## Retorna un mapeo de los valores máximos y minimos de un número respecto 
	## a otros valores mánimos y máximos
	# @ return: float - Valor normalizado 
	def mapRange(self, num, inMin, inMax, outMin, outMax):
		return outMin + (float(float(num) - inMin) / float(inMax - inMin) * (outMax - outMin))

    ## Inicia la conexión con el socket
    ## La IP se toma desde el widget "self.txtIP" en la función "self.frameConnection(self)".
    ## Recuerda que tanto el Puerto del cliente como del socket server tienen que ser el mismo.
	def conexionWifiOnOff(self):
		info = ""
		if self.__connOnOff == False:
			try:

				self.connectionScocket =  Cliente_socket(self.txtIPStr.get(), 1314, 1)

				# Inicia el cliente de comunicación y guarda la respuesta en "info"
				info = self.connectionScocket.iniciar()

                
				# Si "info" contiene la palabra CONECTADO, continua
				if "CONNECTED" in info:
                    
					# Flag de socket activo = True
					self.__connOnOff = True
					self.__connAlive = True
					self.btnConnecionString.set("Stop Conn")
					self.lbConnecionString.set("Connection ON")
					time.sleep(1)

				else:
                    
					# Si la conexión falla mbconectar checked = False
					self.__connOnOff = False
					self.__connAlive = False
					self.btnConnecionString.set("Start Conn")
					self.lbConnecionString.set("Connection OFF")
                    

			except Exception as error:
				print(f"no se encontro el servidor, {error}, info: {info}", False)
				return

		else:
			# Para la comunicación llamando a clientStop en class_cliente_dcc
			# confirmation = self.cliente.clientStop()
			
			# Flag de socket activo = False

			if "closed" in self.connectionScocket.clientStop():
				self.__connOnOff = False
				self.__connAlive = False
				self.lbConnecionString.set("Connection OFF")
			else:
				print("NO CLOSED")

	## Función que maneja el hilo.
	## Esta función recoje los datos desde "class_cliente_adxl345"
	## Esta condicionada por "self.__connAlive", True o False
	def connection(self):
		recvDataOld = ""
		while True:

			# Si el socket esta activo:
			if self.__connAlive:

				# Obtenemos los datos del cliente
				recvData = self.connectionScocket.get_client_data()
				#print(f"Connection: {dccData}")
				

				# Si hay datos dentro de recvData:
				if recvData != recvDataOld:
					recvDataOld = recvData
					self.decodeADXL(recvData)
					self.bgCanvasColor()


# Inicia el programa
if __name__ == '__main__':

	root = mainADXL()
	root.mainloop()