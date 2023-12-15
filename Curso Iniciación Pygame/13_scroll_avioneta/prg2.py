import pygame
import random

# -------------------------------------------------------------
# Codigo prg2.py (1er codigo auxiliar)
# 
# En estos codigos, crearemos las clases que necesitemos
# -------------------------------------------------------------
class Avioneta(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game 

        # creamos un array de imagenes
        self.lista_imagenes = []

        # y añadimos las avionetas
        for i in range(3):
            img = pygame.image.load(f'../images/planeRed{i + 1}.png').convert()
            img.set_colorkey((0, 0, 0)) # negro transparente
            self.lista_imagenes.append(img)

        # creamos una variable de imagen por defecto
        self.imgPd = 0
        self.image = self.lista_imagenes[self.imgPd]

        self.rect = self.image.get_rect()
        
        # creamos la imagen en el centro de la pantalla
        self.rect.centerx = self.game.RESOLUCION[0] // 2
        self.rect.bottom = self.game.RESOLUCION[1] // 2

        # creamos 2 temporizadores (disparo y hélice)
        self.ultimoUpdate = pygame.time.get_ticks()
        self.ultimoUpdateHelice = pygame.time.get_ticks()


    def update(self):
        self.leerTeclado()

        # se manejará con el ratón
        self.leerRaton()

        # para el movimiento:
        calculo = pygame.time.get_ticks()

        if calculo - self.ultimoUpdateHelice > 60:
            self.ultimoUpdateHelice = calculo
            self.imgPd += 1
            if self.imgPd >= 3:
                self.imgPd = 0
            self.image = self.lista_imagenes[self.imgPd]


    def leerRaton(self):
        posXY = pygame.mouse.get_pos()

        self.rect.x = posXY[0]
        self.rect.y = posXY[1]


    def leerTeclado(self):
        tecla = pygame.key.get_pressed()

        if tecla[pygame.K_LEFT]:
            self.rect.x -= 5

        elif tecla[pygame.K_RIGHT]:
            self.rect.x += 5

        if tecla[pygame.K_SPACE]:
            calculo = pygame.time.get_ticks()

            if calculo - self.ultimoUpdate > 150:
                self.ultimoUpdate = calculo
                self.game.instanciaDisparo()

        if self.rect.x < 0:
            self.rect.x = 0

        elif self.rect.right > self.game.RESOLUCION[0]:
            self.rect.right = self.game.RESOLUCION[0]



# creamos una clase para los disparos
class Disparo(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game

        self.image = pygame.image.load('../images/disparoAv1.png').convert()
        self.image.set_colorkey((255, 255, 255))

        self.rect = self.image.get_rect()
        self.height = self.image.get_height()
        self.rect.x = x 
        self.rect.y = y


    def update(self):
        self.rect.x += 9

        if self.rect.x > self.game.RESOLUCION[0]:
            self.kill()




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


