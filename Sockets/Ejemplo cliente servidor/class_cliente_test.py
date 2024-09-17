import socket
import threading
import time


## Cliente para una conexión con servidor socket 
# @ ip: str - Dirección IP del servidor
# @ port: int - Puerto de comunicación 
# @ n_cliente: int - Número de cliente
class clienteSocket():
	def __init__ (self, ip, port, n_cliente):
		self.ip = ip
		self.port = port
		self.n_cliente = n_cliente
		self.FORMAT = 'UTF-8'
		self.h_Cliente = ""

	## Inicia la conexión con socket
	# @ return: str - "info_connection"	
	def iniciar(self):
		try:
			print(f"Conectando con {self.ip}:{self.port}...")
			# Declaramos el socket cliente:
			# socket.AF_INET -> Direccion IPv4 (0.0.0.0)
			# socket.SOCK_STREAM -> Tipo de socket
			self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			
			# Se utiliza "connect_ex" para tener una confirmación de la conexión
			OkConn = self.client.connect_ex((self.ip, self.port))

			# Si la conexión se realiza con exito (0) inicia "hilo_cliente"
			if OkConn == 0 :
				info_connection = f"[CONNECTED] {self.ip}:{self.port}"
				self.h_Cliente = hiloCliente(self.client)
				self.h_Cliente.start()

			# Si la respuesta de "connect_ex" no es 0 retorna mensaje de error
			else:
				info_connection = f"Error al conectar {self.ip}:{self.port}"

			# Retorna la información de la conexión
			return info_connection

		# Si hay un error hace una pausa de 2 segundos y retorna un mensaje de error
		except Exception as er:
			error =  f"Excepcion al conectar: class cliente test: {er}"
			time.sleep(3)
			return error

	## Función para mandar los datos al servidor
	def clientSendData(self, data):
		try:
			self.client.send(data.encode(self.FORMAT))
		except Exception as error:
			return ("error enviando datos:", error)

	## Función que retorna los datos recibidos desde
	## el hilo de cliente
	def get_client_data(self):
		return self.h_Cliente.get_datasRecv()
	

	# Apaga el cliente
	def clientStop(self):
		try:
			self.client.shutdown(socket.SHUT_RDWR)
			self.client.close()
			print("Socket closed")
		except Exception:
			print("Socket closed")
		

## "hilo_cliente" se encarga de de recibir los mensajes desde
## la conexión socket
# @ socket: Recibe el socket desde la clase "Cliente_socket"
class hiloCliente(threading.Thread):
	def __init__ (self, socket):
		threading.Thread.__init__(self)
		self.socket = socket
		self.SIZE = 2048
		self.FORMAT = 'UTF-8'

		
		# Variable privada donde se almacenan los datos recibidos y 
		# serán manejados con getter y setter
		self._dataReceived = ""


	def run(self):
		# La recepción de datos del servidor
		while True:

			# Almacena los datos El valor devuelto es un objeto bytes que representa los datos recibidos. 
			# self.SIZE -> Especifica la cantidad máxima de datos que se recibirán a la vez. 
			# data -> Tipo byte
			data = self.socket.recv(self.SIZE)
			self._dataReceived = data.decode(self.FORMAT)
			
			# Si no hay datos continua 
			if self._dataReceived == '':
				continue
			
			# Si hay datos, pasamos los datos al setter
			else:
				self.set_datasRecv(self._dataReceived)
				
	# Setter para los datos recibidos usado por el hilo
	def set_datasRecv(self, data):
		self._dataReceived = data


	# Getter para obtener los datos desde la
	# clase "socketCliente(ip, port, n_cliente)"
	def get_datasRecv(self):
		return self._dataReceived



## Inicia el programa cliente
if __name__ == '__main__':
	# Establece conexión con el servidor
	cliente = clienteSocket("192.168.0.25", 1314, 1)

	# Inicia la conexión con el servidor
	estado = cliente.iniciar()
	
	# Imprime en pantalla el estado del servidor
	print(estado)

	# Si el estado contiene la palabra "CONNECTED"
	if "CONNECTED" in estado:

		# Envía un mensaje al servidor comunicando que estamos conectados
		cliente.clientSendData("Cliente conectado...")
		
		# Inicia un bucle con la respuesta del resta del servidor
		while True:

			# imprime los datos desde el cliente
			print(cliente.get_client_data())

			cliente.clientSendData(cliente.get_client_data())
			
			# Espera 2 segundos para volver a leer los datos
			time.sleep(2)
