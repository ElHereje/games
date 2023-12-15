import pygame
import random

# -------------------------------------------------------------
# Codigo prg2.py (1er codigo auxiliar)
# 
# En estos codigos, crearemos las clases que necesitemos
# -------------------------------------------------------------
class Nave(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game 

        self.invisible = 255

        self.image = pygame.image.load('../images/nave1.png').convert()
        self.image.set_colorkey((0, 0, 0))
        self.image.set_alpha(self.invisible)
        self.rect = self.image.get_rect()
        #print(self.image, self.rect)
        self.rect.centerx = self.game.RESOLUCION[0] // 2
        self.rect.bottom = self.game.RESOLUCION[1] 


    def update(self):
        self.leerTeclado()

        self.invisible -= 0
        self.image.set_alpha(self.invisible)

        if self.invisible <= 0:
            self.invisible = 255



    def leerTeclado(self):
        tecla = pygame.key.get_pressed()

        if tecla[pygame.K_LEFT]:
            self.rect.x -= 5

        elif tecla[pygame.K_RIGHT]:
            self.rect.x += 5

        if tecla[pygame.K_SPACE]:
            self.game.instanciaDisparo()

        if self.rect.x < 0:
            self.rect.x = 0

        elif self.rect.right > self.game.RESOLUCION[0]:
            self.rect.right = self.game.RESOLUCION[0]

# 1creamos la clase (no va a ser clase sprite)
class ScrollParalax:
    def __init__(self, game, x, y, velX, img):
        self.game = game

        # llamamos a la imagen y la cargamos
        imagen = pygame.image.load(img).convert_alpha()
        # .. y la transformarla en 800x600 (son de 512x128)
        self.image = pygame.transform.scale(imagen, (self.game.RESOLUCION[0], self.game.RESOLUCION[1]))

        # obtenemos el rectangulo
        self.rect = self.image.get_rect()

        self.posInicial = x 
        self.rect.x = x 
        self.rect.y = y 

        self.velX = velX


    # al no ser un sprite, podemos crear una función que dibuje y actualice a la vez
    def dibuja(self):
        self.rect.x -= self.velX

        if self.rect.x <= -self.game.RESOLUCION[0]:
            self.rect.x = self.posInicial

        self.game.pantalla.blit(self.image, (self.rect.x, self.rect.y))
        # para cuando acaba, empuieza el oto...
        self.game.pantalla.blit(self.image, (self.rect.x + self.game.RESOLUCION[0], self.rect.y))


