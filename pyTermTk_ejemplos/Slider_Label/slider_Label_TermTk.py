from TermTk import TTkUtil, TTkUiLoader, TTk, TTkContainer, pyTTkSlot


class Slider(TTkContainer): 
    def __init__(self):

        # Datos generados usando ttkDesigner
        TTkUiLoader.loadDict(TTkUtil.base64_deflate_2_obj(
    "eJx1Ultv0zAUTpa0adfdGUzbJNQn1L2MjWcugoqL8MoKjbYHxIOXWLWFY1dxMjakIR774Efz9/gtHNvZBSESWT4X2+f7vnN+xr9+R4H7rsxAJ+ekVEwKo1tP9g/2D4yO" +
    "qpoZm2plHCtl9FKafh1KUWEmSGl0e4ZLXCh3JP6AC2L04ghyp0zk8pvRnbFUrLJPfjEDtIBCouMJ+06c+xjtEN0dMdE/ZXlFDQrgMnjvCJvSyrrdEb5oku+DILR5CDR5" +
    "H0lOmGJnnJi5Tl4LDFZuzVRKnrKZ0YHRyRjnORNTVzTwP9HtI3wp68roLlBq7Fq3ubeAEG3RHZpcAYm3RBakKi+b64C7Mkp3Msp4XhLLzR13LzXM7cUB7f4V6tn6PRQT" +
    "umytbbRC6CoK6BqsdceGbvjt3pxuzul9+oBu2ZMRCu1P6Dbd0e1XssxB+7lupawC4nplwhlE+o/6R/iMcGiSr9h/w/FUWZ2CTk1371CiDz2TLbQITGgfingGHaeFfeSa" +
    "QMTPDhvotn0e+qa1VlEI0MP/QddxSi5A3hDGqDWUXMK4xLufDwpQ/CVnU1EQAU2Oax2VoA50O8okt3sCvpphYVCoE4g1dn0rsid8i1Hxwxt5FxqMIUquMUZ0HfYN9OMO" +
    "ut5xyQAAdsOJlnTrBPOauPIwg6yoC2/jC29nujeBGeKkP6nIzELrjvH0xqvpU+jiM1jPodQLCJB/Q7iudS+TQpDMllXG667bigjHZ6g7JckIO/dOW4FMGBq6phzhkTwn" +
    "+YCJag+kVFyCusuKVA65DzuNjumQjmF9pJ/ohKaAZP8PrFNMwg=="), self)

        # TTkLabel
        self.lb01 = self.getWidgetByName("lb1")

        # TTkSlider
        self.sl01 = self.getWidgetByName("sl1")

        # TTkSlider conectado con slot
        self.sl01.sliderMoved.connect(self.values)

    # Funcion Slot
    @pyTTkSlot()
    def values(self):
        # Valor de la posicion de TTkSlider en TTkLabel
        self.lb01.setText(str(self.sl01.value()))


root=TTk()
root.layout().addWidget(Slider())
root.mainloop()
