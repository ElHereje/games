
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

        self.crear_laberinto = [
            9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,
            9,0,1,1,1,1,1,1,1,9,1,1,1,1,1,1,1,0,9,
            9,1,9,9,1,9,9,9,1,9,1,9,9,9,1,9,9,1,9,

            9,1,9,9,1,9,9,9,1,9,1,9,9,9,1,9,9,1,9,
            9,1,1,1,2,1,1,1,1,1,1,1,1,1,2,1,1,1,9,
            9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,

            9,1,1,1,1,9,1,1,1,9,1,1,1,1,1,1,1,1,9,
            9,9,9,9,1,9,9,9,1,9,1,9,9,9,1,9,9,9,9,
            9,1,1,1,2,1,1,1,1,1,1,1,1,1,2,1,1,1,9,

            9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,
            9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,
            9,1,1,1,1,9,1,1,1,0,1,1,1,9,1,1,1,1,9,

            9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,
            9,1,1,1,2,1,1,1,1,9,1,1,1,1,2,1,1,1,9,
            9,1,9,9,1,9,9,9,1,9,1,9,9,9,1,9,9,1,9,

            9,1,1,9,1,1,1,1,1,0,1,1,1,1,1,9,1,1,9,
            9,9,1,9,1,9,1,9,9,9,9,9,1,9,1,9,1,9,9,
            9,1,1,1,1,9,1,1,1,9,1,1,1,9,1,1,1,1,9,

            9,1,9,9,9,9,9,9,1,9,1,9,9,9,9,9,9,1,9,
            9,0,1,1,1,1,1,1,2,1,2,1,1,1,1,1,1,0,9,
            9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9
        ]

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
        # lista con los bloques
        self.lista_laberinto = pygame.sprite.Group()
        # 3 - lista con puntitos
        self.lista_puntitos = pygame.sprite.Group()
        # 6 - lista con los items
        self.lista_items = pygame.sprite.Group()

        self.crear_pantalla()

    def crear_pantalla(self):
        contador = -1
        for y in range(21):
            for x in range(19):
                contador += 1
                valor = self.crear_laberinto[contador]
                if valor == 9:
                    self.laberinto = Laberinto(self, x * self.BSX, y * self.BSY, valor)
                    self.lista_sprites_adibujar.add(self.laberinto)
                    self.lista_laberinto.add(self.laberinto)

                # 2 - creamos los puntitos en pantalla
                elif valor == 1:
                    self.puntitos = Puntitos(self, x * self.BSX + self.BSX // 2, y * self.BSY + self.BSY // 2, valor)
                    self.lista_sprites_adibujar.add(self.puntitos) # para que aparezca en pantalla
                    self.lista_puntitos.add(self.puntitos)


    def new_game(self):
        self.puntos = 0
        self.nivel = 1
        self.vidas = 3

        self.pacman = PacMan(self, 75, 75)
        self.lista_sprites_adibujar.add(self.pacman)
        self.lista_pacman.add(self.pacman)

        # 5 - instanciamos el item
        self.items = Items(self, 475, 575)
        self.lista_sprites_adibujar.add(self.items)
        self.lista_items.add(self.items)

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