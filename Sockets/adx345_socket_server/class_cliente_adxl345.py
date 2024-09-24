import socket
import threading
import time
from main_adxl345 import *


## "hilo_cliente" se encarga de de recibir los mensajes desde
## la conexión socket
# @ socket: Recibe el socket desde la clase "Cliente_socket"
class hilo_cliente(threading.Thread):
	def __init__ (self, socket):
		threading.Thread.__init__(self)
		self.socket = socket
		self.SIZE = 1024
		self._dataReceived = ""


	def run(self):
		while True:
			data = self.socket.recv(self.SIZE) #, self.socket.MSG_WAITALL)
			self._dataReceived = data.decode('UTF-8')
			if self._dataReceived == '':
				continue
			else:
				self.set_threadReceived(self._dataReceived)


	def set_threadReceived(self, data):
		self._dataReceived = data

	def get_threadReceived(self):
		return self._dataReceived


## Cliente para una conexión socket con ESP8266 NodeMCU
# @ ip: str - Dirección IP del servidor socket ESP8266
# @ port: int - Puerto de comunicación server ESP8266 adxl345 (1314)
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
			print(f"Connectando con {self.ip} puerto: {self.port}")
			self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			
			# Se utiliza ""connect_ex" para tener una confirmación de la conexión
			OkConn = self.client.connect_ex((self.ip, self.port))

			# Si la conexión se realiza con exito (0) inicia "hilo_cliente"
			if OkConn == 0 :
				info_connection = f"[CONNECTED] to ESP8266 {self.ip}:{self.port}"

				self.h1 = hilo_cliente(self.client)
				self.h1.start()
			else:
				info_connection = f"iniciar: Error al conectar {self.ip}:{self.port}"

			print(info_connection)
			return info_connection

		
		except Exception as er:
			error =  f"Excepcion al conectar: class cliente dcc: {er}"
			time.sleep(3)
			print(f"iniciar Excepcion: {error}")
			return error

	
	def clientSendData(self, data):
		try:
			self.client.send(data.encode(self.FORMAT))
		except Exception as error:
			return ("error enviando datos:", error)

	def get_client_data(self):
		return self.h1.get_threadReceived()
	


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
