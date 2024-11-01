## Clase para tomar los datos desde "src.socket_class"
## Interfaz creada con Tkinter
## Librerías externas:
# - tkinter
# - tkintermapview

# Toma los datos de los sensores ADXL345 y del GPS NEO6MV2
# desde una conexión Wi-Fi en modo cliente o AP
# ESP8266 cliente ->
# ESP8266 AP ->

from src.socket_class import *
from src.ReadFiles import *
import tkinter as tk
from tkinter import ttk
import tkintermapview
import threading
import time

import logging
from datetime import datetime


## Constants:
SCREEN_X_WIDTH = 775
SCREEN_Y_HEIGHT = 625


# Calibration constants:
XMIN: float = -13.00
XMAX: float =  13.00
YMIN: float = -13.00
YMAX: float =  13.00
ZMIN: float = -13.00
ZMAX: float =  13.00

# Map constants
STARTLAT: float = 37.185075 
STARTLON: float = -1.826097

# Crear el area de dibujo:
class main_gps_adxl(tk.Tk):
	def __init__(self):
		super().__init__()

		self.__connOnOff = False
		self.__connAlive = False
		self._countdatareceived = 0
		self.cvHeight = 250
		self.cvWidth = 325
		self.Xaxis = 0.0
		self.Yaxis = 0.0
		self.Zaxis = 0.0
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

		self.top_speed = 0.00
		self.top_old_speed = 0.00
		self.maxLat = -90.0
		self.minLat = 90.0
		self.maxLong = 180.0
		self.minLong = -180.0

		self.coordinates = readwriteJSON.readJSON()

		self.currentLat = self.coordinates[0][0]
		self.currentLon = self.coordinates[0][1]

		self.scaleResizeVar = tk.DoubleVar() 
		
		self.txtIPStr = tk.StringVar()
		self.lbConnecionString = tk.StringVar()
		self.btnConnecionString = tk.StringVar()
		
		#--------------
		self.lb_all_gps_data_in_string = tk.StringVar()
		self.lb_satellites_string = tk.StringVar()
		self.lb_hdop_string = tk.StringVar()  
		self.lb_latitude_string = tk.StringVar()
		self.lb_longitude_string = tk.StringVar() 
		self.lb_age_string = tk.StringVar() 
		self.lb_date_string = tk.StringVar()
		self.lb_time_string = tk.StringVar()
		self.lb_altitude_string = tk.StringVar()
		self.lb_course_string = tk.StringVar()		
		self.lb_speed_string = tk.StringVar()
		self.lb_top_speed_string = tk.StringVar()

		#--------------
		self.lbDataString = tk.StringVar()
		self.lbDataXString = tk.StringVar()
		self.lbDataYString = tk.StringVar()
		self.lbDataZString = tk.StringVar()

		self.mainInterface()
		self.frameConnection()
		self.frameInfoADXL()
		self.frameSelectLineADXL()
		self.frameInfoNEO6MV2()
		self.create_route()

	## Interfaz principal con widget canvas
	## Activa el hilo para la comunicación con la clase class_cliente_adxl345
	## Geometría: 1015x645
	def mainInterface(self):

		self.title("GPS ADXL Interface")
		self.geometry(f'{SCREEN_X_WIDTH}x{SCREEN_Y_HEIGHT}')
		self.resizable(False, False)


		### Define el estilo visual
		style = ttk.Style(self)
		# mainTab.tk.call("source", "assets/theme/forest-light.tcl")
    	# style.theme_use("forest-light")

		self.tk.call("source", "assets/theme/forest-dark.tcl")
		style.theme_use("forest-dark")




		self.graphics_frame = ttk.Frame(self)
		self.graphics_frame.grid(row=0, column=0, rowspan=3)
		self.adxl_canvas = tk.LabelFrame(self.graphics_frame, text="coordinates X Y Z", fg="blue")
		self.adxl_canvas.grid(row= 0, column=0, rowspan=2, padx=10, pady=10, sticky=tk.N+tk.W+tk.E)
		
			
		self.adxl_canvas = tk.Canvas(self.adxl_canvas, width=self.cvWidth, 
											height=self.cvHeight, 
											background='#000000')
		self.adxl_canvas.grid(row=0, column=0, sticky=tk.N+tk.E+tk.W)

		self.lineX = self.adxl_canvas.create_line(self.cvWidth/2, self.cvHeight, self.cvWidth/2, 0, fill="#0000FF", width=3) # Blue
		self.lineY = self.adxl_canvas.create_line(self.cvWidth, self.cvHeight/2, 0, self.cvHeight/2, fill="#008000", width=3) # Green
		self.lineZ = self.adxl_canvas.create_line(0, self.cvHeight, self.cvWidth, self.cvHeight, fill="#800080", width=3) # Purple
	


		## Other Canvas
		self.gps_screen = tk.LabelFrame(self.graphics_frame, text="Track GPS", fg="blue")
		self.gps_screen.grid(row=2, column=0, rowspan=2, columnspan=2, padx=10,  sticky=tk.N+tk.W+tk.E)
		
			
		# create map widget
		self.map_widget = tkintermapview.TkinterMapView(self.gps_screen, width=self.cvWidth, height=self.cvHeight, corner_radius=0)
		self.map_widget.grid(row=0, column=0, columnspan=2, sticky=tk.N+tk.E+tk.W)	
		
		#self.switzerland_marker = self.map_widget.set_address("Cartama", marker=True, text="Spain")
		self.map_widget.set_position(STARTLAT, STARTLON)
		self.map_widget.set_marker(STARTLAT, STARTLON)
		self.map_widget.set_zoom(17)


		self.btnnewpoint = ttk.Button(master=self.gps_screen, 
											text="New point",
											command=lambda: self.new_point_on_map()
											)
									
		self.btnnewpoint.grid(row=1, column=1, pady=5, sticky=tk.N+tk.W)		


		# Activa el hilo para la comunicación
		try:
			self.hiloADXL = threading.Thread(target=lambda : self.connection(), daemon=True)
       	
			# Inicia hilo ADXL
			self.hiloADXL.start()

		except Exception as error:
			print(str(error)) 

	## LabelFrame que contiene los widgets del apartado de comunicación
	## Entry, Button, Label
	def frameConnection(self):

		self.infoConnection = tk.LabelFrame(self, text="Socket connection", fg="blue")
		self.infoConnection.grid(row= 0, column=1, columnspan=2, ipadx=10, pady=10, sticky=tk.N+tk.W)
		
		self.txtIP = ttk.Entry(master=self.infoConnection, 
										textvariable=self.txtIPStr, 
										width=14)
		self.txtIP.grid(row=0, column=0, padx=10, pady=5, sticky=tk.N+tk.W)
		
		self.btnStartSocket = ttk.Button(master=self.infoConnection, 
											textvariable=self.btnConnecionString,
											command=lambda: self.conexionWifiOnOff())
		self.btnStartSocket.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky=tk.N+tk.W)

		self.btnLogData = ttk.Button(master=self.infoConnection,
											width=5,
											text="Log",
											command=lambda: self.Save_Log(0))
		self.btnLogData.grid(row=1, column=1,  pady=5, sticky=tk.N+tk.W+tk.E)		
		
		self.lbConnection = ttk.Label(master=self.infoConnection, 
										textvariable=self.lbConnecionString, 
										width=20)
		self.lbConnection.grid(row=2, column=0, columnspan=2, padx=10, ipady=5, sticky=tk.W)
		
		self.txtIPStr.set("192.168.4.1")
		self.btnConnecionString.set("Start Conn")
		self.lbConnecionString.set("Not connected")

	## LablelFrame que contiene los widgets para mostrar la información 
	## del sensor ADXL345
	## Label
	def frameInfoADXL(self):

		self.infoADXL = tk.LabelFrame(self, text="ADXL345 received data", fg="blue")
		self.infoADXL.grid(row= 1, column=1, sticky=tk.N+tk.W)

		self.lbDataIn = ttk.Label(master=self.infoADXL, 
									textvariable=self.lbDataString,
									font=('Helvetica bold', 10),
									width=35)
		self.lbDataIn.grid(row=3, column=0, padx=5, pady=2, sticky=tk.W)

		self.lbDataX = ttk.Label(master=self.infoADXL, 
									textvariable=self.lbDataXString, 
									width=35)
		self.lbDataX.grid(row=4, column=0, padx=5, pady=2, sticky=tk.W)

		self.lbDataY = ttk.Label(master=self.infoADXL, 
									textvariable=self.lbDataYString, 
									width=25)
		self.lbDataY.grid(row=5, column=0, padx=5, pady=2, sticky=tk.W)

		self.lbDataZ = ttk.Label(master=self.infoADXL, 
									textvariable=self.lbDataZString, 
									width=35)
		self.lbDataZ.grid(row=6, column=0, padx=5, pady=2, sticky=tk.W)
		
		self.lbDataString.set("No ADXL data")
		self.lbDataXString.set("data X:")
		self.lbDataYString.set("data Y:")
		self.lbDataZString.set("data Z:")

	## LabelFrame dentro de "frameInfoADXL" donde se puede seleccionar que lineas
	## se van a representar en el canvas de "mainInterface".
	## CheckButtons
	def frameSelectLineADXL(self):
		self.varcbX = tk.IntVar()
		self.varcbY = tk.IntVar()
		self.varcbZ = tk.IntVar()

		self.frselectLine = tk.LabelFrame(self.infoADXL, text="Show data")
		self.frselectLine.grid(row=7, column=0, padx=5, pady=5, ipadx=10, sticky=tk.N+tk.W+tk.E)
		

		self.cbX = ttk.Checkbutton(master=self.frselectLine, 
									text="Show X axis", 
									variable=self.varcbX, 
									onvalue=1, 
									offvalue=0, 
									command=lambda: self.selectLine(1))
		self.cbX.grid(row=0, column=0)
		if self.showXaxis:
			self.varcbX.set(True)

		self.cbY = ttk.Checkbutton(master=self.frselectLine, 
									text="Show Y axis", 
									variable=self.varcbY, 
									onvalue=1,
									offvalue=0,									
									command=lambda: self.selectLine(2))
		self.cbY.grid(row=0, column=1)
		if self.showYaxis:
			self.varcbY.set(True)


		self.cbZ = ttk.Checkbutton(master=self.frselectLine, 
									text="Show Z axis", 
									variable=self.varcbZ, 
									onvalue=1, 
									offvalue=0,
									command=lambda: self.selectLine(3))
		self.cbZ.grid(row=0, column=2)
		if self.showZaxis:
			self.varcbZ.set(True)

	## LablelFrame que contiene los widgets para mostrar la información 
	## del sensor GPS6MV2
	## Label, Buttons
	def frameInfoNEO6MV2(self):
			self.infoGPS = tk.LabelFrame(self, text="NEO6MV2 received data", fg="blue")
			self.infoGPS.grid(row=2, column=1, pady=5, sticky=tk.N+tk.W+tk.E)
			
			self.lbGPSDataIn = ttk.Label(master=self.infoGPS, 
											textvariable=self.lb_all_gps_data_in_string,
											font=('Helvetica bold', 8),
											width=65)
			self.lbGPSDataIn.grid(row=0, column=0, columnspan=2, padx=5, pady=2, sticky=tk.W)
			
			self.lbGPSsats = ttk.Label(master=self.infoGPS, 
										textvariable=self.lb_satellites_string, 
										width=18)
			self.lbGPSsats.grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)

			self.lbGPShdop = ttk.Label(master=self.infoGPS, 
										textvariable=self.lb_hdop_string, 
										width=18)
			self.lbGPShdop.grid(row=1, column=1, pady=2, sticky=tk.W)

			self.lbGPSlat = ttk.Label(master=self.infoGPS, 
										textvariable=self.lb_latitude_string, 
										width=18)
			self.lbGPSlat.grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
	
			self.lbGPSlon = ttk.Label(master=self.infoGPS, 
										textvariable=self.lb_longitude_string, 
										width=18)
			self.lbGPSlon.grid(row=2, column=1, pady=2, sticky=tk.W)

			self.lbGPSdate = ttk.Label(master=self.infoGPS, 
										textvariable=self.lb_date_string, 
										width=18)
			self.lbGPSdate.grid(row=4, column=0, padx=5, pady=2, sticky=tk.W)
			
			self.lbGPStime = ttk.Label(master=self.infoGPS, 
										textvariable=self.lb_time_string, 
										width=18)
			self.lbGPStime.grid(row=4, column=1, pady=2, sticky=tk.W)
			
			self.lbGPSaltitude = ttk.Label(master=self.infoGPS, 
										textvariable=self.lb_altitude_string, 
										width=18)
			self.lbGPSaltitude.grid(row=5, column=0, padx=5, pady=2, sticky=tk.W)
			
			self.lbGPScourse = ttk.Label(master=self.infoGPS, 
										textvariable=self.lb_course_string, 
										width=18)
			self.lbGPScourse.grid(row=5, column=1, pady=2, sticky=tk.W)

			self.lbGPSspeed = ttk.Label(master=self.infoGPS, 
										textvariable=self.lb_speed_string, 
										width=18)
			self.lbGPSspeed.grid(row=6, column=0, padx=5, pady=2, sticky=tk.W)
			
			self.lbGPSage = ttk.Label(master=self.infoGPS, 
										textvariable=self.lb_age_string, 
										width=18)
			self.lbGPSage.grid(row=6, column=1, pady=2, sticky=tk.W)

			self.lbGPStopspeed = ttk.Label(master=self.infoGPS, 
										textvariable=self.lb_top_speed_string, 
										font=('Helvetica bold', 10),
										width=18)
			self.lbGPStopspeed.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)

			self.btresetspeed = ttk.Button(master=self.infoGPS, 
											text="Reset",
											command=lambda: self.reset_top_speed()
											)
									
			self.btresetspeed.grid(row=7, column=1, padx=5, pady=5, sticky=tk.N+tk.W)


			self.lb_all_gps_data_in_string.set("GPS: 00, 00, 0.000000, 0.000000, age, date, time, altitude, course, 0.00")
			self.lb_satellites_string.set("N Satellites: No data")
			self.lb_hdop_string.set("Hdop: 00")
			self.lb_latitude_string.set("Latitude: 0.000000")
			self.lb_longitude_string.set("Longitude: 0.000000")
			self.lb_date_string.set("Date: 00/00/0000")
			self.lb_time_string.set("Time: 00:00:00")
			self.lb_age_string.set("Age: 0")
			self.lb_altitude_string.set("Altitude: 0.00m")
			self.lb_course_string.set("Course: 0.0")
			self.lb_speed_string.set("Speed: 0.00KM/h")
			self.lb_top_speed_string.set("Top speed: 0.00KM/h")

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
		if not self.showXaxis:
			self.adxl_canvas.coords(self.lineX, 0, 0, 0, 0 )
			self.lbDataXString.set(f"X: NOT SHOW")
		else:
			lineX = self.mapRange(lineX, XMIN, XMAX, -self.cvWidth/2, self.cvWidth/2)
			lineX = float(lineX)
			lineX = int(lineX)
			self.Xaxis = lineX
			self.adxl_canvas.coords(self.lineX, 0, (self.cvHeight/2) + lineX, self.cvWidth, (self.cvHeight/2 - lineX))

			if self.valxmin > lineX:
				self.valxmin = lineX
			if self.valxmax < lineX:
				self.valxmax = lineX

			self.lbDataXString.set(f"X: {lineX} min: {self.valxmin} max: {self.valxmax}")

	## Modifica el eje Y en la pantalla.
	# @ lineY: Int - valor del eje Y
	def changeLineY(self, lineY):
		if not self.showYaxis:	
			self.adxl_canvas.coords(self.lineY, 0, 0, 0, 0 )
			self.lbDataYString.set(f"Y: NOT SHOW")
		else:
			lineY = float(lineY)
			lineY = self.mapRange(lineY, YMIN, YMAX, -self.cvWidth/2, self.cvHeight/2)
			lineY = int(lineY)
			self.Yaxis = lineY
	
			self.adxl_canvas.coords(self.lineY, 0 , (int(lineY)+self.cvHeight/2),  self.cvWidth , int(lineY)+self.cvHeight/2 )

			if self.valymin > lineY:
				self.valymin = lineY
			if self.valymax < lineY:
				self.valymax = lineY
	
			self.lbDataYString.set(f"Y: {lineY} min: {self.valymin} max: {self.valymax} ")

	## Modifica el eje Z en la pantalla.
	# @ lineZ: Int - valor del eje Z
	def changeLineZ(self, lineZ):
		if not self.showZaxis:
			self.adxl_canvas.coords(self.lineZ, 0, 0, 0, 0 )
			self.lbDataZString.set(f"Z: NOT SHOW")
		else:	
			lineZ = float(lineZ)
			lineZ = self.mapRange(lineZ, ZMIN, ZMAX, -self.cvWidth/2, self.cvWidth/2)
			lineZ = int(lineZ)
			self.Zaxis = lineZ

			self.adxl_canvas.coords(self.lineZ, self.cvWidth/2 - lineZ, 0 , self.cvWidth/2 - lineZ, self.cvHeight)
			# self.adxl_canvas.coords(self.lineZ,self.cvWidth - lineZ, self.cvHeight - lineZ, self.cvWidth - lineZ, self.cvHeight - lineZ)
			
			if self.valzmin > lineZ:
				self.valzmin = lineZ
			if self.valzmax < lineZ:
				self.valzmax = lineZ
	
			self.lbDataZString.set(f"Z: {lineZ} min: {self.valzmin} max: {self.valzmax} ")

	## Cambia el color de fondo del canvas ADXL según la posición de los ejes
	## Rojo = 130 ; Amarillo = 170;
	def bgCanvasColorADXL(self):
		RED = 130
		YELLOW = 170

		if self.Xaxis > self.cvWidth/2 - RED or self.Yaxis > self.cvWidth/2 + RED or self.Xaxis < -self.cvWidth/2 + RED or self.Yaxis < -self.cvHeight/2 + RED:
			self.adxl_canvas.configure(bg='red')
		elif self.Xaxis > self.cvWidth/2 - YELLOW or self.Yaxis > self.cvWidth/2 + YELLOW or self.Xaxis < -self.cvWidth/2 + YELLOW or self.Yaxis < -self.cvHeight/2 + YELLOW:
			self.adxl_canvas.configure(bg='yellow')
		else:
			self.adxl_canvas.configure(bg='black')

    ## Identifica el encabezado de dataRecv. Puede tener diferentes
    ## encabezados y de esa mandar el contenido a la función específica.
    # @ dataRecv - String: Cadena que contiene el encabezado y los datos.
	def manage_dataRecv_header(self, dataRecv):
		
		dataRecv = dataRecv.split(">")
		for data in dataRecv:
			if 'gps' in data:
				#print(f"DATA GPS: {dataRecv}")
				self.decode_gps_data(data.replace("<gps", ""))
			elif 'adxl' in data:
				#print(f"DATA ADXL: {data}")
				self.decode_ADXL(data.replace("<adxl", ""))
	
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

				#self.connectionScocket =  Cliente_socket("192.168.4.1", 1314, 1)
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
					time.sleep(0.5)

				else:
					# Si la conexión falla mbconectar checked = False
					self.lbConnecionString.set("Connection error")
					self.__connOnOff = False
					self.__connAlive = False
                    

			except Exception as error:
				print(f"no se encontro el servidor, {error}, info: {info}", False)
				return

		else:
			# Para la comunicación llamando a clientStop en class_cliente_dcc
			#confirmation = self.cliente.clientStop()
			
			# Flag de socket activo = False

			if "closed" in self.connectionScocket.clientStop():
				self.__connOnOff = False
				self.__connAlive = False
				self.btnConnecionString.set("Start Conn")
				self.lbConnecionString.set("Connection OFF")
			else:
				print("NO CLOSED")

			
			# Pone en el texo de respuesta en el label de comunicación
			# self.printConection(confirmation, True)

	## Primera función que maneja el hilo.
	## Esta función recoje los datos desde "class_cliente_adxl345"
	## Esta condicionada por "self.__connAlive", True o False
	def connection(self):
		recvDataOld = ""
		while True:
			# Si el socket esta activo:
			if self.__connAlive:
				# Obtenemos los datos del cliente
				recvData = self.connectionScocket.get_client_data()
				#print(f"Connection: {recvData}")
				

				# Si hay datos dentro de dccData:
				if recvData != recvDataOld:

					recvDataOld = recvData

					self.manage_dataRecv_header(recvData.replace("\n", ""))
					# self.bgCanvasColorADXL()
					
                    
	
	## Elimina los caracteres que no se usan y separa los valores del String.
	# @ gps_datas: String - Datos recibidos por hilo en la función "connection".
	# @ hdop -> Incertidumbre en la posición horizontal que se nos dá del usuario
	# @ age -> Age of data definido como el tiempo que ha transcurrido desde la última carga de los parámetros
	def decode_gps_data(self, gps_datas):
		self.lb_all_gps_data_in_string.set(f"GPS: {gps_datas}")
		# print(f"gps: {gps_datas}")
		if "check" in gps_datas:
			error = f"check wiring error!!! {gps_datas}"
			self.lb_all_gps_data_in_string.set(error)
			return

		for ids, gps_data in enumerate(gps_datas.split(" ")):
			if ids == 0: 
				self.lb_satellites_string.set(f"N Satellites: {gps_data}")
			elif ids == 1:
				self.lb_hdop_string.set(f"Hdop: {gps_data}")
			elif ids == 2:
				self.lb_latitude_string.set(f"Latitude: {gps_data}")
			elif ids == 3:
				self.lb_longitude_string.set(f"Longitude: {gps_data}")
			elif ids == 4:
				self.lb_age_string.set(f"Age: {gps_data}ms")
			elif ids == 5:
				self.lb_date_string.set(f"Date: {gps_data}")
			elif ids == 6:
				self.lb_time_string.set(f"Time {gps_data}")
			elif ids == 7:
				self.lb_altitude_string.set(f"Altitude: {gps_data}M")
			elif ids == 8:
				self.lb_course_string.set(f"Course: {gps_data}º {self.cardinals_points(gps_data)}")
			elif ids == 9:
				self.manage_speed_data(gps_data)


	##
	##
	def cardinals_points(self, course):
		directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
		direction = int((float(course) + 11.25) / 22.5)
		return directions[direction % 16]

	## Elimina los caracteres que no se usan y separa los valores del String.
	# @ dataRecv: String - Datos recibidos por hilo en la función "connection".
	def decode_ADXL(self, dataRecv):
		self.lbDataString.set(dataRecv) 
		datas = dataRecv.split(" ")
		if self._countdatareceived < 3:
			try:
				for ids, data in enumerate(datas):
					if ids == 1:
						self.listax.append(float(data))
						#self.changeLineX(data)
					elif ids == 2:
						#self.changeLineY(data)
						self.listay.append(float(data))					
					elif ids == 3:
						#self.changeLineZ(data)
						self.listaz.append(float(data))
				self._countdatareceived += 1
			except Exception as error:
				print(f"decode_ADXL: {error}")
				return
		else:
			try:

				self.changeLineX(sum(self.listax) / len(self.listax))
				self.changeLineY(sum(self.listay) / len(self.listay))
				self.changeLineZ(sum(self.listaz) / len(self.listaz))

			except Exception as ex:
				print(f"decodeADXL else: {ex}")
				return
			self._countdatareceived = 0
			self.listax.clear()
			self.listay.clear()
			self.listaz.clear()
				
	## Maneja los datos de velocidad para mostarlos en canvas y el el TopSpeed
	def manage_speed_data(self, speed):
		try:
			speed = float(speed)
			if isinstance(speed, float):
				if float(speed) > 1.5:
					self.lb_speed_string.set(f"Speed: {speed}KM/h")
					if speed > self.top_old_speed:
						self.top_old_speed = speed
						self.lb_top_speed_string.set(f"Top speed: {speed}KM/h")
						self.Save_Log(1)
		except Exception:
			speed = 0.00	
	
	## Reinicia la velocidad máxima y la guarda en el archivo log
	def reset_top_speed(self):
		
		self.top_old_speed = 0.0
		self.lb_top_speed_string.set("Top speed: 0.00KM/h")

	def drawRoute(self):
		self.map_widget.set_polygon(self.coordinates,
                                   # command=polygon_click,
                                   name="Route NEO6MV2")
	
	def new_point_on_map(self):
		lat = float(self.lb_latitude_string.get().replace("Latitude: ", ""))
		lon = float(self.lb_longitude_string.get().replace("Longitude: ", ""))
		
		if (lat == 0.0) or (lon == 0.0):
			print("Latitude or Longitude cannot be 0.0")
		else:
			self.coordinates.append([lat, lon])
			readwriteJSON.saveJSON(self.coordinates)
			print(self.coordinates)
			self.create_route()

	def create_route(self):
		self.drawRoute()
	
	## Guarda los datos de los sensores en un archivo de texto
	# @ option: int - Selecciona el tipo de datos al guardar
	##	0 - All
	##	1 - TopSpeed
	def Save_Log(self, option):
		
		now = datetime.now()
		date_time = now.strftime(" %m/%d/%Y %H:%M:%S")
		logging.basicConfig(filename='src/log/gps_info.log', encoding='utf-8', level=logging.INFO)

		if option == 0:
			saveLog = f"{date_time} {self.lb_latitude_string.get()} {self.lb_longitude_string.get()} X: {self.Xaxis} Y: {self.Yaxis} Z: {self.Zaxis}"
		elif option == 1:
			saveLog = f"{date_time} TopSpeed: {self.lb_top_speed_string.get()}"
		
		logging.info(saveLog)

		# datagulugulu = f"https://www.google.es/maps/@{lat},{lon},1245m/data=!3m1!1e3?hl=es&entry=ttu&g_ep=EgoyMDI0MDkyMy4wIKXMDSoASAFQAw%3D%3D"
		# logging.info(datagulugulu)

if __name__ == '__main__':

	root = main_gps_adxl()
	root.mainloop()