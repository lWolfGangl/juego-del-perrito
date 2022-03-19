import pygame
import random
import numpy as np

class agente:
    def __init__(self, ventana):
        self.x = (160) #posicion en el eje x
        self.y = (20) # posicion en el eje y
        self.color=(120, 255, 120) # color verde claro
        self.idle=0 # 0 avanza 1=detenido
        self.last_turn_ = 0  #: 0 si su última acción no fue un giro, 1 si fue un giro a la izquierda, 2 si lo
        self.orientacion_ = 1  # 0 si está orientado hacia el norte, 1 si lo está hacia el este, 2 si lo está
        self.dirty_=True #se usa para identificar suciedad debajo del agente
        self.forma=0 #Determina la forma del agente forma del agente Forma 1 apunta hacia arriba, forma 2 hacia el oeste... forma 4
        self.M=np.zeros((20, 20), dtype=int) # 0= unknow 1 = grown 2=wall (y,x) es el orden que usa numpy v = +y > = +x
        self.ventana = ventana #Variable necesaria para mostrar el agente en el mapa
        self.steps=0 #cuenta la cantidad de pasos sin detectar un terreno desconocido, si llega a 150 activa el idle
        self.manchaseliminadas=0 #cuenta la cantidad de manchas q ha eliminado

    #muestra la forma en el mapa
    def dibujar(self,forma):
        #triangulo q apunta hacia la orientacion
        if forma==0:
            pygame.draw.polygon(self.ventana, self.color,[(self.x , self.y+10), (self.x+5, self.y ), (self.x + 10, self.y+10)])
        if forma==1:
            pygame.draw.polygon(self.ventana, self.color,
                                [(self.x, self.y), (self.x + 10, self.y + 5), (self.x, self.y + 10)])
        if forma==2:
            pygame.draw.polygon(self.ventana, self.color,[(self.x , self.y), (self.x+5, self.y+10 ), (self.x + 10, self.y)])
        if forma==3:
            pygame.draw.polygon(self.ventana, self.color,
                                [(self.x + 10, self.y), (self.x, self.y + 5), (self.x + 10, self.y + 10)])
        #esta forma es el circulo que se usa para borrar una mancha
        if forma==4:
            self.color=(255,255,255)
            pygame.draw.circle(self.ventana, self.color, (self.x+5, self.y+5),5)

    #muestra el mapa mental del Agente
    def mostrarMapa(self):
        print("")
        print (self.M)

    #Esta funcion es la base de t0do el comportamiento del Agente
    def Think(self):
        #Si el agente avanzo mas de 150 pasos se detiene e imprime un mensaje
        if agent.steps > 150:
            print('La maquina elimino ',agent.manchaseliminadas,' manchas')
            self.actIDLE()
        # Si el agente no esta parado...
        if self.idle!=1:
            #Avanza
            self.actforward()
            #Si detecta suciedad
            if (self.detectGrown()==True):
                #Limpia
                self.actSUCK()
            #Si detecta un muro delante suyo
            if(self.detectWall()==True):
                #Si hay un muro a la derecha, gira a la izquierda
                if (self.detectWallRight()==True):
                    self.actTURN_L()
                #Si hay un muro a la izquerda, gira a la derecha
                elif (self.detectWallLeft()==True):
                    self.actTURN_R()
                #Si no, gira de forma aleatoria
                else:
                    if (random.choice((0,1))==0):
                        self.actTURN_L()
                    else:
                        self.actTURN_R()
            #Si no detecta muro entonces
            else:
                if (self.detectMapForward()==True):

                    if(self.detectWallRight() == True):
                        self.actTURN_L()
                    elif (self.detectWallLeft() == True):
                        self.actTURN_R()
                    else:
                        if (self.detectMapleft()==True):
                            self.actTURN_L()
                        elif (self.detectMapRight()==True):
                            self.actTURN_R()
                        else:
                            if (random.choice((0, 1, 2)) == 0):
                                self.actforward()
                            else:
                                if (random.choice((0, 1))==0):
                                    self.actTURN_R()
                                else:
                                    self.actTURN_L()

    def detectMapForward(self):
        if (self.orientacion_==0 and self.M[int(self.y/10)-1,int(self.x/10)]==1):
            return True
        elif (self.orientacion_==1 and self.M[int(self.y/10),int(self.x/10)+1]==1):
            return True
        elif (self.orientacion_==2 and self.M[int(self.y/10)+1,int(self.x/10)]==1):
            return True
        elif (self.orientacion_==3 and self.M[int(self.y/10),int(self.x/10)-1]==1):
            return True
        else:
            return False

    def detectMapleft(self):
        if (self.orientacion_==0 and self.M[int(self.y/10),int(self.x/10)-1]==0):
            return True
        elif (self.orientacion_==1 and self.M[int(self.y/10)-1,int(self.x/10)]==0):
            return True
        elif (self.orientacion_==2 and self.M[int(self.y/10),int(self.x/10)+1]==0):
            return True
        elif (self.orientacion_==3 and self.M[int(self.y/10)+1,int(self.x/10)]==0):
            return True
        else:
            return False

    def detectMapRight(self):
        if (self.orientacion_ == 0 and self.M[int(self.y / 10), int(self.x / 10) + 1] == 0):
            return True
        elif (self.orientacion_ == 1 and self.M[int(self.y / 10) + 1, int(self.x / 10)] == 0):
            return True
        elif (self.orientacion_ == 2 and self.M[int(self.y / 10), int(self.x / 10) - 1] == 0):
            return True
        elif (self.orientacion_ == 3 and self.M[int(self.y / 10) - 1, int(self.x / 10)] == 0):
            return True
        else:
            return False


    def detectGrown(self):
        if (self.M[int(self.y/10),int(self.x/10)]==1):
            self.steps+=1
        else:
            self.steps=0

        self.M[int(self.y/10),int(self.x/10)]=1
        self.detectWallRight()
        self.detectWallLeft()
        #print(int(self.y/10),int(self.x/10))
        for i in range(len(manchas)):
            if (self.x == manchas[i].x and self.y == manchas[i].y):
                return True
        return False

    #Detecta el muro que tiene delante
    def detectWall(self):
        for i in range(len(estructura)):
            if self.orientacion_==0 and self.x==estructura[i].x and self.y-10==estructura[i].y:
                print('Muro detectado...')
                self.M[int(self.y / 10)-1, int(self.x / 10)] = 2
                return True
            elif self.orientacion_==1 and self.x+10==estructura[i].x and self.y==estructura[i].y:
                print('Muro detectado...')
                self.M[int(self.y / 10), int(self.x / 10)+1] = 2
                return True
            elif self.orientacion_==2 and self.x==estructura[i].x and self.y+10 ==estructura[i].y:
                print('Muro detectado...')
                self.M[int(self.y / 10)+1, int(self.x / 10)] = 2
                return True
            elif self.orientacion_==3 and self.x-10==estructura[i].x and self.y==estructura[i].y:
                print('Muro detectado...')
                self.M[int(self.y / 10), int(self.x / 10)-1] = 2
                return True
        return False

    def detectWallLeft(self):
        for i in range(len(estructura)):
            if self.orientacion_==0 and self.x==estructura[i].x+10 and self.y==estructura[i].y:
                self.M[int(self.y / 10), int(self.x / 10) - 1] = 2
                return True
            elif self.orientacion_==1 and self.x==estructura[i].x and self.y==estructura[i].y+10:
                self.M[int(self.y / 10)-1, int(self.x / 10) ] = 2
                return True
            elif self.orientacion_==2 and self.x==estructura[i].x-10 and self.y==estructura[i].y:
                self.M[int(self.y / 10), int(self.x / 10) + 1] = 2
                return True
            elif self.orientacion_==3 and self.x==estructura[i].x and self.y==estructura[i].y-10:
                self.M[int(self.y / 10) + 1, int(self.x / 10)] = 2
                return True
        return False

    def detectWallRight(self):
        for i in range(len(estructura)):
            if self.orientacion_ == 0 and self.x == estructura[i].x - 10 and self.y == estructura[i].y:
                self.M[int(self.y / 10), int(self.x / 10) + 1] = 2
                return True
            elif self.orientacion_ == 1 and self.x == estructura[i].x and self.y == estructura[i].y -10:
                self.M[int(self.y / 10)+1, int(self.x / 10) ] = 2
                return True
            elif self.orientacion_ == 2 and self.x == estructura[i].x + 10 and self.y == estructura[i].y:
                self.M[int(self.y / 10), int(self.x / 10) - 1] = 2
                return True
            elif self.orientacion_ == 3 and self.x == estructura[i].x and self.y == estructura[i].y + 10:
                self.M[int(self.y / 10)-1, int(self.x / 10) ] = 2
                return True
        return False



    # Acción de moverse a la casilla de delante
    def actforward(self):
        if (self.detectWall()==1):
            print ("accion de avanzar cancelada")
            return
        self.color=(120, 255, 120)
        if self.orientacion_ == 0:
            self.y -= 10
            self.forma = 0
        elif self.orientacion_ == 1:
            self.x += 10
            self.forma = 1
        elif self.orientacion_ == 2:
            self.y += 10
            self.forma = 2
        elif self.orientacion_ == 3:
            self.x -= 10
            self.forma = 3


    def actTURN_R(self):
        if self.orientacion_==0:
            self.orientacion_=1
            self.wallleft = 0
        elif self.orientacion_==1:
            self.orientacion_=2
            self.wallleft = 0
        elif self.orientacion_==2:
            self.orientacion_=3
            self.wallleft = 0
        elif self.orientacion_==3:
            self.orientacion_=0
            self.wallleft = 0
        self.wallleft = 0


    def actTURN_L(self):
        if self.orientacion_ == 0:
            self.orientacion_ = 3
            self.wallright = 0
        elif self.orientacion_ == 1:
            self.orientacion_ = 0
            self.wallright = 0
        elif self.orientacion_ == 2:
            self.orientacion_ = 1
            self.wallright = 0
        elif self.orientacion_ == 3:
            self.orientacion_ = 2
            self.wallright = 0
        self.wallright = 0

    # Acción de limpiar una unidad de suciedad de la casilla actual.
    def actSUCK(self):
        for i in range(len(manchas)):
            if (agent.x==manchas[i].x and agent.y==manchas[i].y):
                manchas[i].eliminar()
                self.manchaseliminadas+=1
                self.forma=4
                print('Mancha eliminada')
                self.dirty_=False

    def actIDLE(self):
        self.idle=1


class suciedad:
    def __init__(self, ventana):
        self.x = random.randint(1, (dimX/10)-2) * 10
        self.y = random.randint(1, (dimY/10)-2) * 10
        self.ventana = ventana
        self.colorr = random.randint(20, 80)
        self.colorg = random.randint(20, 80)
        self.colorb = random.randint(20, 80)

    def dibujar(self):
        pygame.draw.rect(self.ventana, (self.colorr, self.colorg, self.colorb), (self.x, self.y, 10, 10))

    def eliminar(self):
        self.x=-10
        self.y=-10

class wall:
    def __init__(self, ventana,x,y):
        self.x = x
        self.y = y
        self.ventana = ventana

    def dibujar(self):
        pygame.draw.rect(self.ventana, (75, 54, 33), (self.x, self.y, 10, 10))

def refrescar(ventana):
    ventana.fill((0, 0, 0))
    for i in range(NumManchas):
        manchas[i].dibujar()
    agent.dibujar(getattr(agent, "forma", 0))
    for i in range(len(estructura)):
        estructura[i].dibujar()



def main():
    global agent, manchas, NumManchas,dimX,dimY,estructura
    dimX=200
    dimY=200
    NumManchas = 25
    manchas = []
    estructura = []
    ventana = pygame.display.set_mode((dimX, dimY))
    ventana.fill((0, 0, 0))
    #Esto dibuja la suciedad
    for i in range(NumManchas):
        manchas.append(suciedad(ventana))
    #Aqui se dibujo la estructura (los muros)
    for i in range(dimX):
        for j in range(dimY):
            if i==0 or i==dimX-10 or j==0 or j==dimY-10:
                estructura.append(wall(ventana,i,j))

    agent = agente(ventana)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        print("Posicion del agente (",agent.x/10,",",agent.y/10,") ")
        agent.Think()

        agent.mostrarMapa()
        refrescar(ventana)
        pygame.display.update()
        pygame.time.delay(200)

if __name__ == '__main__':
    main()
    pygame.quit()
