from TermTk import TTkUtil, TTkUiLoader, TTk, TTkContainer, pyTTkSlot


class Slider(TTkContainer):
    def __init__(self):
        self.count = 0
        # Datos generados usando ttkDesigner
        TTkUiLoader.loadDict(TTkUtil.base64_deflate_2_obj(
    "eJxFUs9v0zAUTknatHTTujE4wGWXSeVS2v0FjDGBMINJrcYBcfCSpz4Lx67iZD+Qhjju8I7m/+XFyVgiy9/77e+z/yR/4zgK352fUnoFpVPWeOofzeazuae4qpVvQv1M" +
    "S+c8ba1WP0+sqaQyUHoabGQpCxdSki+yAC65NgtPw3PrVNX0+uGnIhZPgJKl+gXBPBAToNGZMgffVF6hFxE9bayPoNZYNeboTN50wU9R1Gvi7OjirSe9UE5davD3lJ4a" +
    "yShv4MpavVIbT5Gn9FzmuTLrMDRqf6DBZ3lr68rTiLl0uKaBbhEzwT6+xPSOSXwAW0BV3nblfO7KOxpmqHReQuAW8kOrpVY5a9JUTnFEsdMLj+Nm9I7oA263QqSAO6KH" +
    "ExHjLu974jc+u8f9e3yOL2j8tVTA4gbhxBb1L6SuoREkZX1UURctljctzmi8ZH4aDpYVbLzo0ehcrv9bNcWlvW5K4szqUMq220jTpKbs63DdshgGQS5BP5LQlw8kBiLu" +
    "SOyL3gOJHu6G28C9dnukkqzghjXu8SPqn1ht+bEkr77PC5b9WKu1KZinF0mNMxHhG15zbrbgo0Bd0zizxkDWyOA6kWngwAR9D2lYQgbqqjUGjrtJ7WniwgWc2SvIp8pU" +
    "r3mi05YPse2gCkq27sD2LR7iMa93eILv8ZTHzv4B/W0JdA=="), self)

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
