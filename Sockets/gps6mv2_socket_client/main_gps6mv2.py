## Clase para tomar los datos desde "class_server_adxl345"
## Interface con Tkinter

from class_cliente_gps6mv2 import *

import tkinter as tk
from tkinter import ttk
import threading
import time
import logging
from datetime import datetime



# Crear el area de dibujo:
class mainGPS6MV2(tk.Tk):
	def __init__(self):
		super().__init__()

		self.start_connection = False
		self._countdatareceived = 0
		
		self.top_speed = 0.00
		self.top_old_speed = 0.00 
		
		self.lbspeedmeterString = tk.StringVar()

		self.txt_ip_string = tk.StringVar()
		self.lb_connection_string = tk.StringVar()
		self.btn_connection_string = tk.StringVar()
		
		#--------------
		self.lb_all_data_in_string = tk.StringVar()
		self.lb_satellites_string = tk.StringVar()
		self.lb_hdop_string = tk.StringVar()  
		self.lb_lattitude_string = tk.StringVar()
		self.lb_longitude_string = tk.StringVar() 
		self.lb_age_string = tk.StringVar() 
		self.lb_date_string = tk.StringVar()
		self.lb_time_string = tk.StringVar()
		self.lb_altitude_string = tk.StringVar()
		self.lb_course_string = tk.StringVar()		
		self.lb_speed_string = tk.StringVar()
		self.lb_top_speed_string = tk.StringVar()

		self.mainInterface()
		self.frameConnection()
		self.frameInfoNEO6MV2()

	## Interfaz principal con widget canvas
	## Activa el hilo para la comunicación con la clase class_cliente_adxl345
	## Geometría: 1015x645
	def mainInterface(self):

		self.title("GPS 6MV2 Interface")
		self.geometry('480x410')

		self.screen = tk.LabelFrame(self, text="Datos GPS")
		self.screen.grid(row= 0, column=0, rowspan=4, padx=10, pady=10, sticky=tk.N+tk.S+tk.W+tk.E)
			
				
		# Activa el hilo para la comunicación
		try:
			self.thread_connection = threading.Thread(target=lambda : self.connection(), daemon=True)
       	
			# Inicia hilo conexión
			self.thread_connection.start()
		except Exception as error:
			print(str(error)) 

	## LabelFrame que contiene los widgets del apartado de comunicación
	## Entry, Button, Label
	def frameConnection(self):

		self.frame_info_connection = tk.LabelFrame(self, text="Socket connection", fg="blue")
		self.frame_info_connection.grid(row= 0, column=1, pady=25, sticky=tk.N+tk.W+tk.E)
		
		self.entry_ip = ttk.Entry(master=self.frame_info_connection, 
										textvariable=self.txt_ip_string, 
										width=20
										)
		self.entry_ip.grid(row=0, column=0, padx=10, pady=5, sticky=tk.N+tk.W)
		self.txt_ip_string.set("192.168.4.1")
		
		self.btnStartSocket = ttk.Button(master=self.frame_info_connection, 
											textvariable=self.btn_connection_string,
											command=lambda: self.wifi_conection(self.txt_ip_string.get())
											)
		self.btnStartSocket.grid(row=1, column=0, padx=10, pady=5, sticky=tk.N+tk.W)
		self.btn_connection_string.set("Start Conn")

		self.btnLogData = ttk.Button(master=self.frame_info_connection, 
											text="Log",
											command=lambda: self.Save_Log(0))
		self.btnLogData.grid(row=1, column=1, padx=10, pady=5, sticky=tk.N+tk.W)		
		
		self.lbConnection = ttk.Label(master=self.frame_info_connection, 
										textvariable=self.lb_connection_string, 
										width=20)
		self.lbConnection.grid(row=2, column=0, padx=10, ipady=5, sticky=tk.W)
		self.lb_connection_string.set("Not connected")

	
	## LablelFrame que contiene los widgets para mostrar la información 
	## del sensor GPS6MV2
	## Label, Buttons
	def frameInfoNEO6MV2(self):
			self.frame_info_GPS = tk.LabelFrame(self, text="NEO6MV2 received data", fg="blue")
			self.frame_info_GPS.grid(row=2, column=1, padx=10, pady=10, sticky=tk.N+tk.W)
			
			self.lb_all_data_in = ttk.Label(master=self.frame_info_GPS, 
											textvariable=self.lb_all_data_in_string,
											font=('Helvetica bold', 8),
											width=65)
			self.lb_all_data_in.grid(row=0, column=0, columnspan=2, padx=5, pady=2, sticky=tk.W)
			
			self.lb_satellites = ttk.Label(master=self.frame_info_GPS, 
										textvariable=self.lb_satellites_string, 
										width=18)
			self.lb_satellites.grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)

			self.lb_hdop = ttk.Label(master=self.frame_info_GPS, 
										textvariable=self.lb_hdop_string, 
										width=30)
			self.lb_hdop.grid(row=1, column=1, pady=2, sticky=tk.W)

			self.lb_lattitude = ttk.Label(master=self.frame_info_GPS, 
										textvariable=self.lb_lattitude_string, 
										width=18)
			self.lb_lattitude.grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)

	
			self.lb_longitude = ttk.Label(master=self.frame_info_GPS, 
										textvariable=self.lb_longitude_string, 
										width=18)
			self.lb_longitude.grid(row=2, column=1, pady=2, sticky=tk.W)

			self.lb_date = ttk.Label(master=self.frame_info_GPS, 
										textvariable=self.lb_date_string, 
										width=15)
			self.lb_date.grid(row=4, column=0, padx=5, pady=2, sticky=tk.W)
			
			self.lb_time = ttk.Label(master=self.frame_info_GPS, 
										textvariable=self.lb_time_string, 
										width=18)
			self.lb_time.grid(row=4, column=1, pady=2, sticky=tk.W)
			
			self.lb_altitude = ttk.Label(master=self.frame_info_GPS, 
										textvariable=self.lb_satellites_string, 
										width=20)
			self.lb_altitude.grid(row=5, column=0, padx=5, pady=2, sticky=tk.W)
			
			self.lb_course = ttk.Label(master=self.frame_info_GPS, 
										textvariable=self.lb_course_string, 
										width=18)
			self.lb_course.grid(row=5, column=1, pady=2, sticky=tk.W)

			self.lb_speed = ttk.Label(master=self.frame_info_GPS, 
										textvariable=self.lb_speed_string, 
										width=15
										)
			self.lb_speed.grid(row=6, column=0, padx=5, pady=2, sticky=tk.W)
			
			self.lb_age = ttk.Label(master=self.frame_info_GPS, 
										textvariable=self.lb_age_string, 
										width=15
										)
			self.lb_age.grid(row=6, column=1, pady=2, sticky=tk.W)

			self.lb_top_speed = ttk.Label(master=self.frame_info_GPS, 
											textvariable=self.lb_top_speed_string, 
											font=('Helvetica bold', 10),
											width=20
											)
			self.lb_top_speed.grid(row=7, column=0, padx=5, pady=2, sticky=tk.W)


			self.bt_reset_speed = ttk.Button(master=self.frame_info_GPS, 
											text="Reset",
											command=lambda: self.reset_top_speed()
											)
									
			self.bt_reset_speed.grid(row=7, column=1, padx=5, pady=5, sticky=tk.N+tk.W)

			self.lb_all_data_in_string.set("Datain: sat, hdop, lat, long, age, date, time, altitude, course, speed")
			self.lb_satellites_string.set("N Satellites: No data")
			self.lb_hdop_string.set("Hdop: 00")
			self.lb_lattitude_string.set("Latitude: 0.000000")
			self.lb_longitude_string.set("Longitude: 0.000000")
			self.lb_date_string.set("Date: 00/00/0000")
			self.lb_time_string.set("Time: 00:00:00")
			self.lb_age_string.set("Age: 0")
			self.lb_altitude_string.set("Altitude: 0.00m")
			self.lb_course_string.set("Course: 0.0")
			self.lb_speed_string.set("Speed: 0.00KM/h")
			self.lb_top_speed_string.set("Top speed: 0.00KM/h")


    ## Identifica el encabezado de dataRecv. Puede tener diferentes
    ## encabezados y de esa mandar el contenido a la función específica.
    # @ dataRecv - String: Cadena que contiene el encabezado y los datos.
	def manage_dataRecv_header(self, dataRecv):
		
		dataRecv = dataRecv.split(">")
		for data in dataRecv:
			if 'gps' in data:
				#print(f"DATA GPS: {dataRecv}")
				self.decode_gps_data(data.replace("<gps", ""))

    ## Inicia la conexión con el socket
    ## La IP se toma desde el widget "self.txtIP" en la función "self.frameConnection(self)".
    ## Recuerda que tanto el Puerto del cliente como del socket server tienen que ser el mismo.  
	def wifi_conection(self, ip_to_connect):
		info = ""
		if self.start_connection == False:
			try:

				#self.connectionScocket =  Cliente_socket("192.168.1.36", 1314, 1)
				self.connectionScocket =  Cliente_socket(ip_to_connect, 1314, 1)

				# Inicia el cliente de comunicación y guarda la respuesta en "info"
				info = self.connectionScocket.iniciar()

                
				# Si "info" contiene la palabra CONECTADO, continua
				if "CONNECTED" in info:
                    
					# Flag de socket activo = True
					self.start_connection = True
					self.__connAlive = True
					self.btn_connection_string.set("Stop Conn")
					self.lb_connection_string.set("Connection ON")
					time.sleep(0.5)

				else:
					# Si la conexión falla mbconectar checked = False
					self.start_connection = False

                   
			except Exception as error:
				print(f"no se encontro el servidor, {error}, info: {info}", False)
				return

		else:
			# Para la comunicación llamando a clientStop en class_cliente_dcc
			#confirmation = self.cliente.clientStop()
			
			# Flag de socket activo = False

			if "closed" in self.connectionScocket.clientStop():
				self.start_connection = False
				self.btn_connection_string.set("Start Conn")
				self.lb_connection_string.set("Connection OFF")

			else:
				self.lb_connection_string.set("Is not closed...")
			

	## Primera función que maneja el hilo.
	## Esta función recoje los datos desde "class_cliente_adxl345"
	## Esta condicionada por "self.__connAlive", True o False
	def connection(self):
		recvDataOld = ""
		while True:
			# Si el socket esta activo:
			if self.start_connection:
				try:
					# Obtenemos los datos del cliente
					recvData = self.connectionScocket.get_client_data()
				
					# Si hay datos dentro de dccData:
					if recvData != recvDataOld:

						recvDataOld = recvData

						self.manage_dataRecv_header(recvData.replace("\n", ""))
				except Exception:
					return		


	## Elimina los caracteres que no se usan y separa los valores del String.
	# @ gps_datas: String - Datos recibidos por hilo en la función "connection".
	def decode_gps_data(self, gps_datas):
		self.lb_all_data_in_string.set("Data:" + gps_datas)

		for ids, gps_data in enumerate(gps_datas.split(" ")):
			if ids == 0: 
				self.lb_satellites_string.set(f"N Satellites: {gps_data}")
			elif ids == 1:
				self.lb_hdop_string.set(f"Hdop: {gps_data}")
			elif ids == 2:
				self.lb_lattitude_string.set(f"Latitude: {gps_data}")
			elif ids == 3:
				self.lb_longitude_string.set(f"Longitude: {gps_data}")
			elif ids == 4:
				self.lb_age_string.set(f"Age: {gps_data}")
			elif ids == 5:
				self.lb_date_string.set(f"Date: {gps_data}")
			elif ids == 6:
				self.lb_time_string.set(f"Time {gps_data}")
			elif ids == 7:
				self.lb_altitude_string.set(f"Altitude: {gps_data}M")
			elif ids == 8:
				self.lb_course_string.set(f"Course: {gps_data}")
			elif ids == 9:
				self.manage_speed_data(gps_data)
				
			
				
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
		except Exception:
			speed = 0.00		

				
	def reset_top_speed(self):
		self.top_old_speed = 0.00
		self.lb_top_speed_string.set("Top speed: 0.00KM/h")


	## Guarda los datos de los sensores en un archivo de texto
	# @ option: int - Selecciona el tipo de datos al guardar
	##	0 - All
	##	1 - Top speed
	def Save_Log(self, option):
		now = datetime.now()
		date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

		if option == 0:
			logging.basicConfig(filename='gps_info.log', encoding='utf-8', level=logging.INFO)
			saveLog = f"{date_time} {self.lb_lattitude_string.get()} {self.lb_longitude_string.get()} {self.lb_altitude_string.get()}"
		elif option == 1:
			saveLog = f"{date_time} Top speed: {self.lb_top_speed_string.get()}"
		
		logging.info(saveLog)


if __name__ == '__main__':

	root = mainGPS6MV2()
	root.mainloop()
