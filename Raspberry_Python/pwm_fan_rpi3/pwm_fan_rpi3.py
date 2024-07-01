import RPi.GPIO as IO
import time
import subprocess

IO.setwarnings(False)	# No mostrar alertas GPIO
IO.setmode(IO.BCM)		# Número de pin BCM - El PIN8 es 'GPIO14'
IO.setup(14, IO.OUT)	# Inicializa GPIO14 como pin de salida
fan = IO.PWM(14,50)		# Establece GPIO14 como salida PWM a 50Hz
fan.start(0)			# Inicia la señal PWM iniciada al 0% (apagado)

mode = 1	# mode=0: Proportional; mode=1: Stepped

perfiles = ([40, 60, 80],	# Without heatsink
			[30, 50, 70],	# With heatsink
			[30, 40, 60],	# Active heatsink
			[ 0,  0,  0]	# Custom
			)	
perfil = 0 # Choose perfil number

speed_min = 0
speed_max = 100

def showMode():
	if mode == 0:
		print("Proportional Mode - perfil {}\n".format(perfil))
	elif mode == 1:
		print("Steeped Mode - perfil {}\n".format(perfil))

## Función para leer la temperatura con subprocess
def getTemp():
	output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output= True)
	temp_str = output.stdout.decode()
	try:
		return float(temp_str.split('=')[1].split('\'')[0])
	except (IndexError, ValueError):
		raise RuntimeError('no se puede obtener temperatura')

def renormalize(n, range1, range2):
	delta1 = range1[1] - range1[0]
	delta2 = range2[1] - range2[0]

	return (delta2 * (n -range1[0]) /delta1) + range2[0]


## Función velocidad proporcional del ventilador
def Proportional(n_perfil):
	temp = getTemp()
	if temp < perfiles[0][0]:                      # Constrain temperature to set range limits
		temp = perfiles[n_perfil][0]
	elif temp > perfiles[n_perfil][2]:
			temp = perfiles[n_perfil][2]
	pwm = int(renormalize(temp, [perfiles[n_perfil][0], perfiles[n_perfil][2]], [speed_min, speed_max]))
	print("temp: {}ºC, pwm: {}".format(temp, pwm))	# Debug only
	fan.ChangeDutyCycle(pwm) # Set fan duty based on temperature, from minSpeed to maxSpeed
	time.sleep(5)

## Función selocidad del ventilador por pasos
def Stepped(n_perfil):
	temp = getTemp()
	print("tem: {}ºC".format(str(temp)))	# Debug only
	if temp > perfiles[n_perfil][2]:
		fan.ChangeDutyCycle(100)
	elif temp  > perfiles[n_perfil][1]:
		fan.ChangeDutyCycle(50)
	elif temp > perfiles[n_perfil][0]:
		fan.ChangeDutyCycle(25)
	time.sleep(5)

showMode()
while True:
	if mode == 0:
		Proportional(perfil)
	elif mode == 1:
		Stepped(perfil)
