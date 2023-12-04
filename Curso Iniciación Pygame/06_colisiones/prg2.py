'''
Este es el 2º código, donde creamos y almacenamos los SPRITES

La clase que crea los Sprites necesita como MINIMO una "image" y un "rect"


Incluimos en este video las colisiones y naves enemigas


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

        # limitamos la salida de disparos con un cronometro
        self.ultimoUpdate = pygame.time.get_ticks()

    def update(self):
        self.leerTeclado()
        

    def leerTeclado(self):
        # desplazamiento
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_RIGHT]:
            self.rect.centerx += 5
        elif tecla[pygame.K_LEFT]:
            self.rect.centerx -= 5

        # disparos
        if tecla[pygame.K_SPACE]:
            # chequeamos el tiempo pasado
            calculo = pygame.time.get_ticks()
            if calculo - self.ultimoUpdate > 200 : # tiempo en milisegundos
                self.ultimoUpdate = calculo
                self.game.instanciaDisparo()

        # límites de la pantalla
        if self.rect.x < 0 :
            self.rect.x = 0
        if self.rect.right > self.game.RESOLUCION[0]:
            self.rect.right = self.game.RESOLUCION[0]



class Disparo(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game 

        self.image = pygame.image.load('../images/laserBlue16.png').convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

        # posición inicial del disparo ( y se los pasamos por parámetros...)
        self.rect.centerx = x
        self.rect.bottom = y

        self.velY = 10


    def update(self):
        self.rect.y -= self.velY 

        # mouse = pygame.mouse.get_pos()
        # self.rect.y = mouse[0]
        # self.rect.x = mouse[1]
        
        # eliminamos el objeto si pasa de la poantalla
        if self.rect.bottom < 0:
            self.kill()



class Enemigo(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__() # herencia
        self.game = game

        # para las animaciones, creamos una lista de imagenes
        self.lista_imagenes = []
        self.anima = 0

        for i in range(5): # son 5 imágenes
            img = pygame.image.load('../images/enemyRed{}.png'.format(i + 1)) # las llaves sustituyen al nº
            img.set_colorkey((255, 255, 255)) # transparenta el fondo
            self.lista_imagenes.append(img)
        # cargamos la 1º de las imágenes
        self.image = self.lista_imagenes[self.anima]

        self.rect = self.image.get_rect()
        self.rect.centerx = self.game.RESOLUCION[0] // 2
        self.rect.bottom = 200

        self.ultimoUpdate = pygame.time.get_ticks()


    def update(self):

        self.check_colision()

        calculo = pygame.time.get_ticks()

        if calculo - self.ultimoUpdate > 100:
                self.ultimoUpdate = calculo
                self.anima += 1

                if self.anima >= 5:
                    self.anima = 0
                # cojemos las coord.
                centerx = self.rect.centerx
                bottom = self.rect.bottom
                # cambiamos de imagen
                self.image = self.lista_imagenes[self.anima]
                # las colocamos en las mismas coordenadas
                self.rect = self.image.get_rect()
                self.rect.centerx = centerx
                self.rect.bottom = bottom

    def check_colision(self):
        
        # con spritecollide
        colision = pygame.sprite.spritecollide(self, self.game.lista_disparos, True) # true hace que desaparezca el disparo

        # con groupcollide
        # colision = pygame.sprite.groupcollide(self.game.lista_enemigos, self.game.lista_disparos, tue, true)
        if colision:
            self.kill() # eliminamos la nave)



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