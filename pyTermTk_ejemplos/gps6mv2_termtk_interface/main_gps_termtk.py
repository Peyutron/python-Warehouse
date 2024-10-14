import TermTk as ttk
from TermTk import pyTTkSlot
import threading
from class_cliente import *


class main_gps_TermTk():
    def __init__(self):
        self.start_connection = False
        self.speed_top_old = 0.00

        root = ttk.TTk()
        win = ttk.TTkWindow(parent=root, border=True, title="GPS-6MV2 Interface", pos=(0,0), size=(80,24))
        root.addWidget(win)
    
        self.bt_start_connect = ttk.TTkButton(parent=win, 
                                    border=True, 
                                    text="Connectar", 
                                    pos=(1, 1), 
                                    size=(15, 1),
                                    )
        self.bt_start_connect.clicked.connect(lambda: self.wifi_conection(self.txt_ip.text() ))
        self.bt_start_connect.setFocus()
    
        self.txt_ip = ttk.TTkLineEdit(parent=win, 
                                        border=True, 
                                        text="192.168.4.1", 
                                        pos=(20,1), 
                                        size=(16,1)
                                        )

        self.lb_connection_info = ttk.TTkLabel(parent=win, 
                                border=True,
                                pos=(2, 3), 
                                size=(60, 5)
                                )
        
        self.lb_datain = ttk.TTkLabel(parent=win, 
                                border=True,
                                pos=(2, 6), 
                                size=(60, 5)
                                )
        
        self.lb_satellites = ttk.TTkLabel(
                                parent=win, 
                                border=True, 
                                pos=(2, 8), 
                                size=(2, 7)
                                )
        
        self.lb_hdop = ttk.TTkLabel(
                                parent=win, 
                                border=True, 
                                pos=(30, 8), 
                                size=(10, 2)
                                )
        
        self.lb_location_lat = ttk.TTkLabel(
                                parent=win, 
                                border=True, 
                                pos=(2, 10), 
                                size=(5, 2)
                                )
        
        self.lb_location_lng = ttk.TTkLabel(
                                parent=win, 
                                border=True, 
                                pos=(30, 10), 
                                size=(5, 2)
                                )
        
        self.lb_age = ttk.TTkLabel(
                                parent=win, 
                                border=True, 
                                pos=(2, 12), 
                                size=(2, 2)
                                )
        
        self.lb_date = ttk.TTkLabel(
                                parent=win, 
                                border=True, 
                                pos=(30, 12), 
                                size=(2, 2)
                                )
        
        self.lb_time = ttk.TTkLabel(
                                parent=win, 
                                border=True, 
                                pos=(2, 14), 
                                size=(10, 2)
                                )
    
        self.lb_altitude = ttk.TTkLabel(
                                parent=win, 
                                border=True, 
                                pos=(30, 14), 
                                size=(10, 2)
                                )
        
        self.lb_course = ttk.TTkLabel(
                                parent=win, 
                                border=True, 
                                pos=(2, 16), 
                                size=(10, 2)
                                )
    
        self.lb_speed = ttk.TTkLabel(
                                parent=win, 
                                border=True, 
                                pos=(30, 16), 
                                size=(10, 2)
                                )
        
        self.lb_top_speed = ttk.TTkLabel(
                                parent=win, 
                                border=True, 
                                pos=(2, 18), 
                                size=(10, 2)
                                )
        self.bt_reset_top_speed = ttk.TTkButton(parent=win, 
                                    border=True, 
                                    text="Reset", 
                                    pos=(30, 18), 
                                    size=(15, 1),
                                    )
        self.bt_reset_top_speed.clicked.connect(lambda: self.reset_top_speed())

        self.lb_connection_info.setText("Not connected")
        self.lb_datain.setText("Datain: sat, hdop, lat, long, age, date, time, altitude, course, speed")
        self.lb_satellites.setText("N Satellites: 00")
        self.lb_hdop.setText("Hdop: 00")
        self.lb_location_lat.setText("Lat: 0.000000")
        self.lb_location_lng.setText("Lng: 0.000000")
        self.lb_date.setText("Date: 00/00/0000")
        self.lb_time.setText("Time: 00:00:00")
        self.lb_age.setText("Age: 0")
        self.lb_altitude.setText("Altitude: 0.00m")
        self.lb_course.setText("Course 0.0")
        self.lb_speed.setText("Speed: 0.00KM/h")
        self.lb_top_speed.setText("Top Speed: 0.00KM/h")

        # Activa el hilo para la comunicación
        try:
            self.thread_connection = threading.Thread(target=lambda : self.connection(), daemon=True)
        
            # Inicia hilo conexión
            self.thread_connection.start()
        except Exception as error:
            #print(str(error)) 
            self.lb_connection_info.setText(str(error))

        root.mainloop()
        
        
    
    ## Inicia la conexión con el socket
    ## La IP se toma desde el widget "self.txtIP" en la función "self.frameConnection(self)".
    ## Recuerda que tanto el Puerto del cliente como del socket server tienen que ser el mismo.
    @pyTTkSlot() 
    def wifi_conection(self, ip_to_connect):
        info = ""
        if self.start_connection == False:
            try:
        
                self.connectionScocket =  Cliente_socket(str(ip_to_connect), 1314, 1)
        
                # Inicia el cliente de comunicación y guarda la respuesta en "info"
                info = self.connectionScocket.iniciar()
                self.lb_connection_info.setText(info)
    
        
                # Si "info" contiene la palabra CONECTADO, continua
                if "CONNECTED" in info:
                        
                    # Flag de socket activo = True
                    self.start_connection = True
                    self.bt_start_connect.setText("Stop Conn")
                    self.lb_connection_info.setText("Connection ON")
                    time.sleep(0.5)
    
                else:    
                    # Si la conexión falla mbconectar checked = False
                    self.start_connection = False
                        

            except Exception as error:
                excption_error = (f"no se encontro el servidor, {error}, info: {info}", False)
                self.lb_connection_info.setText(excption_error)
                return
    
        else:
            # Para la comunicación llamando a clientStop en class_cliente
            #confirmation = self.cliente.clientStop()
                
            # Flag de socket activo = False
    
            if "closed" in self.connectionScocket.clientStop():
                self.start_connection = False
                self.bt_start_connect.setText("Start Conn")
                self.lb_connection_info.setText("Connection OFF")
            else:
               self.lb_connection_info.setText("Is not closed...")
    

    
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
                    

    ## Identifica el encabezado de dataRecv. Puede tener diferentes
    ## encabezados y de esa mandar el contenido a la función específica.
    # @ dataRecv - String: Cadena que contiene el encabezado y los datos.
    def manage_dataRecv_header(self, dataRecv):
        dataRecv = dataRecv.split(">")
        for data in dataRecv:
            if 'gps' in data:
                #print(f"DATA GPS: {dataRecv}")
                self.decode_gps_data(data.replace("<gps", ""))


    ## Elimina los caracteres que no se usan y separa los valores del String.
    # @ dataRecv: String - Datos recibidos por hilo en la función "connection".
    def decode_gps_data(self, gps_datas):
            self.lb_datain.setText("Data: " + gps_datas)

            for ids, gps_data in enumerate(gps_datas.split(" ")):
                if ids == 0: 
                    self.lb_satellites.setText(f"N Satellites: {gps_data}")
                elif ids == 1:
                    self.lb_hdop.setText(f"Hdop: {gps_data}")
                elif ids == 2:
                    self.lb_location_lat.setText(f"Latitude: {gps_data}")
                elif ids == 3:
                    self.lb_location_lng.setText(f"Longitude: {gps_data}")
                elif ids == 4:
                    self.lb_age.setText(f"Age: {gps_data}")
                elif ids == 5:
                    self.lb_date.setText(f"Date:  {gps_data}")
                elif ids == 6:
                    self.lb_time.setText(f"Time {gps_data}")
                elif ids == 7:
                    self.lb_altitude.setText(f"Altitude: {gps_data}M")
                elif ids == 8:
                    self.lb_course.setText(f"Course: {gps_data}")
                elif ids == 9:
                    #self.lb_speed.setText(f"Speed: {gps_data}")
                    self.manage_speed_data(gps_data)
                

            #print(f"decodeGPS: {dataRecv}")
            '''
            return "<gps" 
            + String(satellites)
            + " " 
            + String(hdop)
            + " " 
            + String(location_lat)
            + " "
            + String(location_lng)
            + " "
            + String(age)
            + " "
            + String(date)
            + " "
            + String(time)
            + " "
            + String(altitude)
            + " "
            + String(course)
            + " "
            + String(speed)
            + ">";
             '''
    
                    
        ## Maneja los datos de velocidad para mostarlos en canvas y el el TopSpeed
    
    def manage_speed_data(self, speed):
        try:
            speed = float(speed)
            if isinstance(speed, float):
                if float(speed) > 1.5:
                    self.lb_speed.setText(f"Speed: {speed}KM/h")
                    if speed > self.speed_top_old:
                        self.speed_top_old = speed
                        self.lb_top_speed.setText(f"Top speed: {speed}KM/h")
                else:
                    self.lb_speed.setText("Speed: 0.00KM/h")
        except Exception:
            speed = 0.00

    def reset_top_speed(self):
        self.speed_top_old = 0.00
        self.lb_top_speed.setText("Top speed: 0.00KM/h")


if __name__ == '__main__':
    main_gps_TermTk()