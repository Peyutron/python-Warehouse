from TermTk import TTkUtil, TTkUiLoader, TTk, TTkContainer, pyTTkSlot



class ClassFilePicker(TTkContainer):
    def __init__(self):

        
        # Data generated using ttkDesigner
        TTkUiLoader.loadDict(TTkUtil.base64_deflate_2_obj(
    "eJyFlMtP20AQhx3ycEJAtIUGFaTKx9BDBD1UqmirQsqjmISoROVQVdXGXjIrHG9kr3lUQuoxkea4/X87axtEQbSxLO/M7OP7zczmV+l3pWylv2vdRPucR7GQocby69Z6" +
    "a11jUSVCm1DZC1gca5zr98/aMlRMhDzSWBmziI3idEqpy0Zc42yHYici9OWFxmpPxkKZLb/rpltyZziWjsVPnpoDd5VjrSNC50T4CrRr0WKy9rkYgjJmrcMu8+CBZRVM" +
    "nBx5PPPYX0UsBgHXE7R3QkYj3wz7UgZ9MdZoabR7zPdFOEwPtbKHY+WQXclEaayRpHycYCXIRiQIyrAC9jWJ2ONyxFV0lS8nbqVjrHogAj/iRls6Pd0pV24WNqGGpf6F" +
    "CDXUM/kFDvNmtOkuc1hwLXhC79NUCDzLPosTWJrAc2jAsplZdAvm4fACVrCyLSOf0j7Bcl8o0gwNnMsOdHYDNoxNTqxqAqt38OFlRv3WXSRqcGjXjLaa6h7w4Ba2GAw2" +
    "ctYCpShjbZjTF1ybWAuPsZJMfkmptLvSORUEhuW2DCQ1SGn12/qIcrwViGE44qEpa4LFiFJE9S16MjBfm+x4zELtFtAmXz5OMtBFAt2lXbcTpWTYE94Z5eCGeb5/Ok49" +
    "P+SYh7f0N5lecouGvk70xUcz/QZrR7Q4Q4e1CdbawL0z00x6inZqUFtNsdRj1IpYaJHUNhunjY11w+Z8EiyQQ/KTpegaaZzfCgLHxGKn+WqN5m15Hh8rpyN9njZ3ui63" +
    "EtikVnhH73tK84cb7fDxoc6YnfNcZ+O+zpl/66R3bQK7U9ibwj58hoO/4eHwPjR0iejoUTysU2lM6Xd8oW5LUlXk4aknr0Y5p9xw5//b91g/pP8Wp5uMBlTmKS7dMZ1j" +
    "xSJlrrLJ3xfOfOcoDK5o1mwnCZRwzFw9eUjLH7pYkmDdk2HIPVPHmG5x0voDJL2grQ=="), self)



        # Conectamos el Filepicker con el evento "abrirArchivo"
        self.getWidgetByName("Tfpicker_open").filePicked.connect(self.abrirArchivo)
        
        # Texto que se mostrará en el widget Filepicker "Tfpicker_save"
        self.getWidgetByName("Tfpicker_save").setText("Save file as...")
        
        # Conectamos el Filepicker con el evento "guardarArchivo"
        self.getWidgetByName("Tfpicker_save").filePicked.connect(self.guardarArchivo)

        # TTkLabel
        self.lb01 = self.getWidgetByName("lb1")
        self.lb01.setText("No hay datos")

        # TTkLabel
        self.text_edit = self.getWidgetByName("textedit")
        self.text_edit.setText("No hay datos")

    # Rutina generica para abrir/leer un archivo
    pyTTkSlot(str)
    def abrirArchivo(self, fileName):
        
        with open(fileName) as fp:
            # Pone el la ruta y el nombre en el widget "lb1"
            self.lb01.setText(f"Open: {fileName}")
            
            # Pone el contenido del archivo en el "textedit"
            self.text_edit.setText(fp.read())

    

    # Rutina generica para guardar el contenido del widget "textedit"
    pyTTkSlot(str)
    def guardarArchivo(self, fileName):

        # Guarda el contenido del widget "textedit" a un 
        # archivo con el nombre asignado
        with open(fileName, 'w') as fp:
            self.lb01.setText(f"saved: {fileName}")
            fp.write(self.text_edit.toPlainText())


if __name__ == '__main__':
    root=TTk()
    root.layout().addWidget(ClassFilePicker())
    root.mainloop()
