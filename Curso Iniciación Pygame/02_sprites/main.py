'''
Vamos a usar ala codificación orientada a objetos con 2 archivos, uno main,
con las clases ppales y otro auxiliar.
'''

import pygame
import sys
from prg2 import *

class Game:
    def __init__(self):
        pygame.init()

        self.ROJO = (255, 0, 0)   
        self.VERDE = (0, 255, 0)
        self.AMARILLO = (255, 255, 0)
        self.NEGRO = (0, 0, 0)
        self.fondoGRIS = (70, 70, 70)

        self.RESOLUCION = (800, 600)
        self.FPS = 60 

        self.enJuego = True

        self.pantalla = pygame.display.set_mode(self.RESOLUCION)
        self.reloj = pygame.time.Clock()

        self.lista_spritesAdibujar = pygame.sprite.Group() # creamos una lisya de sprites

        self.instancias()

    def instancias(self):
        self.nave = Nave(self)
        self.lista_spritesAdibujar.add(self.nave)

    def update(self):
        self.lista_spritesAdibujar.update()
        pygame.display.flip()
        self.reloj.tick(self.FPS)


    def draw(self):
        self.pantalla.fill((self.fondoGRIS))
        self.lista_spritesAdibujar.draw(self.pantalla)


    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def buclePrincipal(self):
        while self.enJuego:
            self.check_event()
            self.update()
            self.draw()

# instanciacion de la clase
if __name__ == '__main__':
    game = Game()
    game.buclePrincipal()