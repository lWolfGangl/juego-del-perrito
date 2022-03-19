import pygame
import random
class agente:
	def __init__(self,ventana):
		self.x=100
		self.y=100
		self.last_turn_=0 	#: 0 si su última acción no fue un giro, 1 si fue un giro a la izquierda, 2 si lo
							#ue hacia la derecha
		self.orientacion_=0 #0 si está orientado hacia el norte, 1 si lo está hacia el este, 2 si lo está
							#hacia el sur y 3 si lo está hacia el oeste.
		self.ventana=ventana
	def dibujar(self):
		pygame.draw.polygon(self.ventana,(120,255,120),[(self.x-5, self.y), (self.x, self.y-10), (self.x+5, self.y)])
	#def Think(self):
	#def actFORWARD(self): #Acción de moverse a la casilla de delante
	#def actTURN_L(self): # Acción de girar 90º hacia la izquierda sin avanzar ninguna casilla.

	#def actTURN_R(self): #Acción de girar 90º hacia la derecha sin avanzar ninguna casilla.

	#def actSUCK(self): # Acción de limpiar una unidad de suciedad de la casilla actual.

	#def actIDLE(self): #No produce ninguna acción. El agente permanece inmóvil.
class suciedad:
	def __init__(self,ventana):
		self.x=random.randrange(40)*10
		self.y=random.randrange(40)*10
		self.mancha=1 	#: 0 si su última acción no fue un giro, 1 si fue un giro a la izquierda, 2 si lo
		self.ventana=ventana
		self.colorr=random.randint(20,80)
		self.colorg = random.randint(20, 80)
		self.colorb = random.randint(20, 80)
	def dibujar(self):
		pygame.draw.rect(self.ventana,(self.colorr,self.colorg,self.colorb),(self.x,self.y,10,10))

def refrescar(ventana):
	ventana.fill((0,0,0))
	for i in range(NumManchas):
		manchas[i].dibujar()
	agent.dibujar()
def main():
	global agent,manchas,NumManchas
	NumManchas=50
	manchas=[]
	ventana =pygame.display.set_mode((400,400))
	ventana.fill((0,0,0))
	for i in range(NumManchas):
		manchas.append(suciedad(ventana))
	agent=agente(ventana)
	run=True
	while run:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				run=False
		refrescar(ventana)
		pygame.display.update()
		pygame.time.delay(100)


if __name__=='__main__':
	main()
	pygame.quit()
