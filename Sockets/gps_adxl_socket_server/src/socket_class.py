import socket
import threading
import time
from  main_gps_adxl import *

'''
## "hilo_cliente" se encarga de de recibir los mensajes desde
## la conexión socket
# @ socket: Recibe el socket desde la clase "Cliente_socket"
'''
class hilo_cliente(threading.Thread):
	def __init__ (self, socket):
		threading.Thread.__init__(self)
		self.socket = socket
		self.SIZE = 2048
		self._dataRecv = ""
		self.oldData = ""


	def run(self):
		# La recep
		while True:
			try:
				data = self.socket.recv(self.SIZE) #, self.socket.MSG_WAITALL)
				dataRecv = data.decode('UTF-8')
				if dataRecv == '':
					continue
				else:
					self.set_datarecv(dataRecv)
					#print(f"datos serial: {dataRecv}")
			except Exception as error:
				print(error)

	def set_datarecv(self, data):
			self._dataRecv = data
			#print(f"set dcc {self._dataRecv}")

	def get_datarecv(self):
		# print(f"get dcc {self._dataRecv}")
		return self._dataRecv


## Cliente para una conexión socket con módulo
## wi-fi ESP-01 configurado con la documentación DCC-EX
## https://dcc-ex.com/support/wifi-at-version.html
# @ ip: str - Dirección IP de la central DCC
# @ port: int - Puerto de comunicación 2560 para DCC
# @ n_cliente: int - Número de cliente
class Cliente_socket():
	def __init__ (self, ip, port, n_cliente):
		self.ip = ip
		self.port = port
		self.n_cliente = n_cliente
		self.FORMAT = 'UTF-8'
		self.h1 = ""

	## Inicia la conexión con socket
	# return: str - "info_connection"	
	def iniciar(self):
		try:
			print(f"Connecting to {self.ip} port: {self.port}")
			self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.client.settimeout(8)
			
			# Se utiliza ""connect_ex" para tener una confirmación de la conexión
			OkConn = self.client.connect_ex((self.ip, self.port))

			# Si la conexión se realiza con exito (0) inicia "hilo_cliente"
			if OkConn == 0 :
				info_connection = f"[CONNECTED] to ESP8266 {self.ip}:{self.port}"

				# files_dcc().Save_Log(f"{info_connection}")
				self.h1 = hilo_cliente(self.client)
				self.h1.start()
			else:
				info_connection = f"Connection timeout error {self.ip}:{self.port}"

			print(info_connection)
			return info_connection

		
		except Exception as er:
			error =  f"Excepcion al conectar: class cliente dcc: {er}"
			print(f"iniciar Excepcion: {error}")
			return error

	
	def clientSendData(self, data):
		try:
			self.client.send(data.encode(self.FORMAT))
		except Exception as error:
			return ("Error sending data:", error)

	def get_client_data(self):
		# print(f"datos get client {self.h1.get_datarecv()}")
		return self.h1.get_datarecv()
	


	def clientStop(self):
		try:
			self.client.shutdown(socket.SHUT_RDWR)
			return "Socket closed"
		except Exception:
			return "Socket closed"
		self.client.close()


if __name__ == '__main__':
	cliente = Cliente_socket("192.168.1.36", 1314, 1)
	cliente.iniciar()
