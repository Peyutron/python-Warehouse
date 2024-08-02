from TermTk import TTkUtil, TTkUiLoader, TTk, TTkContainer, pyTTkSlot



class ListSelect_Label(TTkContainer):
    def __init__(self):

        # Genera una lista con fruta
        self.lista = ["Manzana", "Platano", "Melocotón", "Pera" ]
        
        # Data generated using ttkDesigner
        TTkUiLoader.loadDict(TTkUtil.base64_deflate_2_obj(
    "eJx1Uktv1DAQTkh2s0uhvEoPwKHHFY/Vwj9ALWrVsKhSI3pAHLzJaG3h2KvYoS1SJY57mOP0/zJOwuOCLcvfPP19k/xMby/vRN26oRlm36FxyhrC0bv5Yr4gTHyrKIRG" +
    "pRbOEd4rim+H1nihDDSE441oRO26lPSTqIHw7pJjF8pU9pJwcmad8qHlV5rlaZ4ApufqB3Tmi3wXcLpU5uBCVV5SHnExWyeg1tIHc7oUV0PwNIriEGfHEO892Wfl1EoD" +
    "bTH7YASjKsDCWl2oDWFEmJ2JqlJm3T0a9Rtw/FFc29YTTlnSgFsc6x6xIDmSz2R2wyKOwdbgm+uhnHl7cjgppdJVA522Lp+f5VbKeQp1MznFRLu3JHd68SnI+wHt5RnI" +
    "B3kkH/J51MmQj/vryVbubeVTuY+756ChDKM7WNoKKI9xcmSOBiNqMWl4wDyjpLQ63BnbbiNMyMzYN+C2ZzbpRK5A/0Nt9Zda/Ida/Jta/F9qaQFXLHEfR4dWW/4L0udf" +
    "FjUP8r1Wa1OD4W+XtvIlt3nF5zW3esNEoG1xp7TG9LIcj62d/wKW+9J7"), self)

        # TTkList
        self.ls01 = self.getWidgetByName("ls1")
        
        # TTkList conecta con el slot al hacer click en el texto
        self.ls01.textClicked.connect(lambda : self.Current_Selection())

        # TTkLabel
        self.lb01 = self.getWidgetByName("lb1")

        # LLama a la función donde se cargarán los elementos de la lista
        self.Print_Listbox(self.lista)

    @pyTTkSlot(str)
    def Current_Selection(self):
        data = ""
        for i in self.ls01.selectedLabels():
            data += i
            self.lb01.setText(data)


    # Imprime los elemtos de la lista en TTkList
    def Print_Listbox(self, items):
        for item in items:
            self.ls01.addItem(item)




root=TTk()
root.layout().addWidget(ListSelect_Label())
root.mainloop()
