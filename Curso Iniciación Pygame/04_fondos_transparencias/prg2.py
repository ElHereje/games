'''
Este es el 2º código, donde creamos y almacenamos los SPRITES

La clase que crea los Sprites necesita como MINIMO una "image" y un "rect"


Incluimos en este video la clase EstrellasRetro para una alternativa de fonso

'''

# -------------------------------------------------------------
# Codigo prg2.py (1er codigo auxiliar)
# 
# En estos codigos, crearemos las clases que necesitemos
# -------------------------------------------------------------


import pygame
import random

class Nave(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__() # herencia
        self.game = game

        self.invisible = 255 # transparenceia de la image. 255=Totalmente Visible

        self.image = pygame.image.load('../images/nave1.png').convert()
        self.image.set_colorkey((0, 0, 0)) # hace al negro transparente

        self.image.set_alpha(self.invisible)

        self.rect = self.image.get_rect()
        # posición inicial de la nave
        self.rect.centerx = self.game.RESOLUCION[0] // 2
        self.rect.bottom = self.game.RESOLUCION[1]

    def update(self):
        self.leerTeclado()

        # podemos ir haciendo que se haga invisible
        self.invisible -= 3
        self.image.set_alpha(self.invisible)

        if self.invisible <= 100:
            self.invisible = 255
        

    def leerTeclado(self):
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_RIGHT]:
            self.rect.centerx += 5
        elif tecla[pygame.K_LEFT]:
            self.rect.centerx -= 5
        if self.rect.x < 0 :
            self.rect.x = 0
        if self.rect.right > self.game.RESOLUCION[0]:
            self.rect.right = self.game.RESOLUCION[0]


class EstrellasRetro:
    def __init__(self, game):
        self.game = game
        self.color = (random.randrange(255), random.randrange(255), random.randrange(255))
        self.x = random.randrange(self.game.RESOLUCION[0])
        self.y = random.randrange(self.game.RESOLUCION[1])


        self.size = random.randrange(2) + 1

    def dibuja(self):
        self.actualiza()

        pygame.draw.rect(self.game.pantalla, self.color, (self.x, self.y, self.size, self.size))



    def actualiza(self):
        self.y += 3
        if self.y > self.game.RESOLUCION[1]:
            self.y = 0