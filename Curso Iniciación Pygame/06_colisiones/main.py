'''
Generamos la codificación para los enemigos y las colisiones

'''

# ----------------------------------------------------------------
# Codigo Principal (main.py) ... Aqui se aloja la clase Game
# 
# Funciones:
#           instancias()
#           buclePrincipal()
#               update()
#               draw()
#               check_event()           
# ----------------------------------------------------------------

import pygame
import sys
from prg2 import *

class Game:
    def __init__(self): # fuinción constructora 
        pygame.init()
        pygame.mixer.init()

        self.ROJO = (255, 0, 0)   
        self.VERDE = (0, 255, 0)
        self.AMARILLO = (255, 255, 0)
        self.NEGRO = (0, 0, 0)
        self.fondoGRIS = (70, 70, 70)

        self.RESOLUCION = (800, 600)
        self.FPS = 60 

        self.enJuego = True

        self.arrayEstrellasRetro = []

        self.pantalla = pygame.display.set_mode(self.RESOLUCION)
        self.reloj = pygame.time.Clock()

        # cargamos las imagenes de fondo
        self.fondoEstrellas = pygame.image.load('../images/fondo_estrellas_jon.png').convert()
        self.saturno = pygame.image.load('../images/saturno_moonpatrol.png').convert_alpha()

        # sonidos
        self.sonido_disparo = pygame.mixer.Sound('../images/Phaser.ogg')


        self.lista_spritesAdibujar = pygame.sprite.Group() # creamos una lisTa de sprites
        # colisiones con los disparos --> creamos lista de disparon
        self.lista_disparos = pygame.sprite.Group()

        self.instancias()

    def instancias(self): # creamos los objetos (los autométicos...)

        # nuestra nave
        self.nave = Nave(self)
        self.lista_spritesAdibujar.add(self.nave)

        # enemigos
        self.enemigo = Enemigo(self)
        self.lista_spritesAdibujar.add(self.enemigo)

        

    def instanciaDisparo(self):

        # imagen
        self.disparo = Disparo(self, self.nave.rect.centerx, self.nave.rect.y)
        # lo añadimos a las listas
        self.lista_spritesAdibujar.add(self.disparo)
        self.lista_disparos.add(self.disparo)

        # sonido
        self.sonido_disparo.play()


    def update(self):
        self.lista_spritesAdibujar.update()
        pygame.display.flip()
        self.reloj.tick(self.FPS)



    def draw(self):

        self.pantalla.blit(self.fondoEstrellas, (0,0))
        self.pantalla.blit(self.saturno, (500, 200))    

        self.lista_spritesAdibujar.draw(self.pantalla)




    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def buclePrincipal(self):
        while self.enJuego:
            self.check_event()  # chequea
            self.update() # actualiza
            self.draw() # dibuja

# instanciacion de la clase
if __name__ == '__main__':
    game = Game()
    game.buclePrincipal()