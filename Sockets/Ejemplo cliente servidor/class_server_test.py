import socket
import threading
	

## Clase para probar conexión Socket
# @ ip: String -> Dirección IP del servidor 
# @ port: Int -> Puerto de comunicación
class serverSocket():
	def __init__(self, ip, port):
		
		# IP y puerto
		self.ip = ip	
		self.port = port

		# Tamaño del bufer
		self.SIZE = 2048	
		
		# Formato
		self.FORMAT = "UTF-8"
		
		# Lista de clientes 
		self.lista_clientes = []

		# Hilos de comunicación
		self.hilos = []

	# Función para iniciar el servidor
	def iniciar(self):
		hostname = socket.gethostname()
		self.ip = socket.gethostbyname(hostname)
		print(f"[START] Server starting at {self.ip}")
		
		# Declaramos el objeto server:
		# socket.AF_INET -> Direccion IPv4 (0.0.0.0)
		# socket.SOCK_STREAM -> Tipo de socket
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	
		# Enlaza el socket con la dirección IP y el puerto de comunicación
		server.bind((self.ip, self.port))

		# Habilita el servidor para aceptar las conexiones
		# El valor 5 establece el número de conexiones que se 
		# conectan al servidor, en este caso 5 clientes.
		server.listen(5)
		print("[LISTENING] Waiting for connections... ")

		# Bucle donde se realiza la conexión cliente - servidor
		while True:

			# Acepata la conexión y retorna 
			# @	cliente -> Nuevo objeto socket usado para enviar y recibir 
			# 				información en la conexión 
			# @ addr -> es la dirección vinculada al socket en el extremo 
			# 				de la conexión.
			cliente, addr = server.accept()
			
			# Para que cada conexión sea independiente cada cliente
			# tendra su propio hilo "thread"
			# Crea un objeto hilo desde la clase "Hilo_cliente" con los
			# parametros:
			# cliente -> Dado por server.accept()
			# addr -> Dado por server.accept()
			# self.lista_clientes -> Lista con los clientes conectados
			hilo = Hilo_server(cliente, addr, self.lista_clientes)

			# Inicia el hilo
			hilo.start()

			# Añade hilo y cliente a sus respectivas listas
			self.hilos.append(hilo)
			self.lista_clientes.append(cliente)
			print(f"Clientes conectados:")
			for cli in self.lista_clientes:
				print(f"[CLIENTE] {cli}\n")
			

## Hilo del cliente donde se manejan los datos recibidos por el cliente. 
# @ cliente: clientsocket -> desde server.accept() 
# @ addr: datos de la conexión desde server.accept()
# @ clientes: list -> lista donde guardamos los clientes conectados
class Hilo_server(threading.Thread):

	def __init__(self, cliente, addr, clientes):
		threading.Thread.__init__(self)
		self.cliente = cliente
		self.addr = addr
		self.clientes = clientes
		self.SIZE = 2048
		self.FORMAT = "UTF-8"

	# Mientras el hilo este activo
	def run(self):
		count = 0
		print(f"[NEW CONNECTION] {self.addr[0]}")

		# Bucle en el que se recibiran los datos
		while True:
			try:
				# Almacena los datos El valor devuelto es un objeto bytes que representa los datos recibidos. 
				# self.SIZE -> Especifica la cantidad máxima de datos que se recibirán a la vez. 
				# data -> Tipo byte
				data = self.cliente.recv(self.SIZE)

				# Si hay datos en la recepción:
				if data:
					
					# Decodifica los datos en "UTF-8"
					data = data.decode("UTF-8")

					# Imprime la respuesta en pantalla en formato String
					print(self.addr[0], " > ", str(data), "\n")

					# Manda una respuesta al cliente
					respuesta = f"[OK] datos recibidos {count}"
					print(f"Server > {respuesta}")
					
					# Envía los datos al cliente
					self.cliente.send(bytes(respuesta, self.FORMAT))
					count += 1

				# Cierra la conexión y borra al cliente de la lista
				else:
					print(f"{self.addr[0]} connection lost, removed from list.")
					print(f"\n{self.cliente} is removed from list\n")
					self.clientes.remove(self.cliente)
					self.cliente.close()

			# Si hay una excepción imprime el error y sale del bucle
			except Exception as er:
				print("\nData error", er)
				break



## Inicia el programa principal
if __name__ == '__main__':
	# Inicia el socket con los parametros IP y puerto
	# Si no especificamos una dirección IP y usamos un 
	# String vacío, socket usará la IP de la maquina.
	server = serverSocket("", 1314)

	# Inicia el servidor
	server.iniciar()
