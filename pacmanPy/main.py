
import pygame
import random
import sys
from pac1 import *

#====================================================
#                 Cod. Ppal MAIN
#====================================================


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # colores
        self.AMARILLO = (220, 190, 0)
        self.BLANCO = (240, 240, 240)
        self.FONDO_GRIS = (73, 73, 73)
        self.ROJO = (230, 0, 0)
        self.VERDE_FONDO = (20, 110, 40)
        self.AZUL_C = (144, 205, 205)

        # banderas
        self.enJuego = False
        self.gameOver = True
        self.programaEjecutandose = True
        self.nivel_superado = True

        # pausa entre niveles
        self.pausa_superado_tomartiempo = pygame.time.get_ticks()

        # tamaños de los bloques (personajes)
        BLOQUE_SIZE_X = 50
        BLOQUE_SIZE_Y = 50
        self.BSX = BLOQUE_SIZE_X
        self.BSY = BLOQUE_SIZE_Y

        self.puntos = 0
        self.nivel = 1
        self.vidas = 3
        self.PAUSA_VIDAS = 2000
        self.RESOLUCION = (1200, 700)
        self.FPS = 60
        self.pantalla = pygame.display.set_mode(self.RESOLUCION)
        pygame.display.set_caption('PacMan - Versión Imad Elias')
        self.reloj = pygame.time.Clock()

        self.lista_sprites_adibujar = pygame.sprite.Group()
        # grupo de un solo elemento (personaje)
        self.lista_pacman = pygame.sprite.Group()

        self.crear_pantalla()

    def crear_pantalla(self):
        pass

    def new_game(self):
        self.puntos = 0
        self.nivel = 1
        self.vidas = 3

        # 2 - INSTANCIAMOS UN OBJETO PACMAN
        self.pacman = PacMan(self, 25, 25)
        self.lista_sprites_adibujar.add(self.pacman)

    def nivel_superado(self):
        pass

    def pausa_nivel_superado(self):
        pass

    def update(self):
        self.lista_sprites_adibujar.update()
        pygame.display.flip()
        self.reloj.tick(self.FPS)

    def draw(self):
        self.pantalla.fill(self.FONDO_GRIS)
        self.lista_sprites_adibujar.draw(self.pantalla)

        

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and self.gameOver:
                if pygame.K_KP_ENTER:
                    self.gameOver = False
                    self.new_game()
                    self.run()

            elif not self.gameOver:
                self.pacman.leer_teclado()

    def run(self):
        while not self.gameOver:
            self.check_event()
            self.update()
            self.draw()

        while self.gameOver:
            self.update()
            self.draw()
            self.check_event()



if __name__ == '__main__':
    game = Game() # instanaciamos el juego
    game.run()