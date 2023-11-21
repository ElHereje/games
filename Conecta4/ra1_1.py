import pygame
import random


class Tablero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() # heredamos los métodos de la superclase (sprite)
        # cargamos la imagen
        self.image = pygame.image.load("tablero_conecta4.png").convert()
        self.image.set_colorkey((255, 255, 255)) # el blanco del interior será transparente
        self.rect = self.image.get_rect()
        self.rect.x = x # valor cero de la tupla que se declaró al instanciarlo  (1, 100)
                        # que es: tablero = ra1_1.Tablero(i[0]. i[1])
        self.rect.y = y

def devuelve_numero_random(cero, ocho):
    return random.randint(cero, ocho)