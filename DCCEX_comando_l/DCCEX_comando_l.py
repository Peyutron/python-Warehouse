# import random as rn    # En caso de usar un varlor aleatorio
  
# Comando `l' Comando de DCCEX -> <l DCC REG SPEED FUNCTION>
# La velocidad va desde 0 a 255.
# Desde 0 a 128 va en un sentido y de 128 a 255 va en retroceso
# - Retroceso - 2-127 = speed 1-126, 0 = stop
# - Avance - 130-255 = speed 1-126, 128 = stop

speed = []
# speed.append(rn.randint(100, 200)) # Genera una velocidad test aleatoria
speed = [0,1,2,3,125,126,127,128,129,130,131,254,255] # Velcidad test fija

def main():
  avance = 0  # Inicia la variable avance 
  for s in speed:   # Extraemos los valores uno a uno 
    valor = s 
    if s >= 1 :
      s = s-1
    else:
      s = 0 
    if valor >= 128: # Si la velocidad es mayor de 128 el estado es retroceso
      avance = 1
      if s >= 128:
        s = s - 128
    if s >= 126:
      s = 126    
    print(f"Valor: {valor} Velocidad: {s} Avance: {avance}")
    
if __name__ == '__main__':
  main()
