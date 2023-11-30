'''
Este es el 2º código, donde creamos y almacenamos los SPRITES
'''

import pygame

class Nave(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__() # herencia
        self.game = game
        self.image = pygame.image.load('../images/nave1.png').convert()
        self.image.set_colorkey((0, 0, 0)) # hace al negro transparente
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        self.rect.x += 1
        self.rect.y += 1
        

