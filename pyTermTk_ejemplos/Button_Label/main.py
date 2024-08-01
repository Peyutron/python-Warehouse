from TermTk import TTkUtil, TTkUiLoader, TTk, TTkContainer, TTkButton
from TermTk import pyTTkSlot

class Interfaz_Label(TTkContainer):
	def __init__(self):
		TTkUiLoader.loadDict(TTkUtil.base64_deflate_2_obj(
    "eJx1kktv1DAQgBOSbDa0UB6lqK0Ey217WS0cOPA40BUP1SyqREQlEAdvYu1YzdqrxIEWqRLHrTRH838ZJykFocaKPA97/M3jZ/jrIPCa78wOMf4mykpqZTF6MhqPxhYD" +
    "U0vrXFFW8KqyuJ6mxxOtDJdKlBZ7S17yRdUcCT/whbB4fUq+I6ly/d1i/1BX0riQX+2QheyawPCj/CEa9TO7KTCZSjU4krkByzy6TNo7IedgnJpM+UnnPPA83/nJ0Plb" +
    "S/xJVnJWCLvC+LXiJOVOTLUuUrm06FmMD3meSzVvHvXaJbD3np/q2lhMKKVOrrFXtBIlBBHsQHxGSbwVeiFMedpdJ25jK+xnIIu8FC635ngTqcvcXRxC8o9pzb2/zQIB" +
    "N5z0iCUCNpgHt+i/3WQDd9rt7go2V3APtuC+Oxkw3y0B27CDvX1d5lT7FUapNJQ4bOF6+8TgTcHnlSuM169h968c4EGL/pBFhA4DinqJvF8bQx26QA5m5nEHG1HDWthN" +
    "h73B+gQbXAWLYSpOqKC9i4B7K0wmILJj1xZ7jnGjUIPOawxKKgm1OMh04faY9GrJlWU+xmTr5LrF7Dc9monikrKYXVL6fyh9RxkRpX9lSZ9i1IbCaKILTVMc7n4ZL2gQ" +
    "XhVyrhZC0eyFNTyjtjyn/wXFekkk4n8Tr2tcy7RSInNDXtEk1KPfcuQTkg=="), self)

		self.window = self.getWidgetByName("TTkWindow")
		self.window.setTitle("Titulo ventana")

		self.bt1 = self.getWidgetByName("bt1")
		self.bt1.clicked.connect(lambda : self.cambiar_label("Hola!!!"))

		self.lb1 = self.getWidgetByName("lb1")

	pyTTkSlot(str)
	def cambiar_label(self, data):
		self.lb1.setText(data)
		self.bt1.setText("Pulsado!")



root=TTk()
root.layout().addWidget(Interfaz_Label())
root.mainloop()
