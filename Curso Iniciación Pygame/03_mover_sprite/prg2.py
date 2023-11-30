'''
Este es el 2º código, donde creamos y almacenamos los SPRITES

La clase que crea los Sprites necesita como MINIMO una "image" y un "rect"


'''

# -------------------------------------------------------------
# Codigo prg2.py (1er codigo auxiliar)
# 
# En estos codigos, crearemos las clases que necesitemos
# -------------------------------------------------------------


import pygame

class Nave(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__() # herencia
        self.game = game
        self.image = pygame.image.load('../images/nave1.png').convert()
        self.image.set_colorkey((0, 0, 0)) # hace al negro transparente
        self.rect = self.image.get_rect()
        # posición inicial de la nave
        self.rect.centerx = self.game.RESOLUCION[0] // 2
        self.rect.bottom = self.game.RESOLUCION[1]

    def update(self):
        self.leerTeclado()
        

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