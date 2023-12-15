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
                self.game.instanciaDisparo(False) # disparo normal
                self.game.instanciaDisparo(True)

        if self.rect.x < 0:
            self.rect.x = 0

        elif self.rect.right > self.game.RESOLUCION[0]:
            self.rect.right = self.game.RESOLUCION[0]



# creamos una clase para los disparos
class Disparo(pygame.sprite.Sprite):
    # añadimos un true o false con una variable --> diagonal
    def __init__(self, game, x, y, diagonal):
        super().__init__()
        self.game = game
        self.diagonal = diagonal

        img = pygame.image.load('../images/disparoAv1.png').convert()

        if self.diagonal:
            img = pygame.transform.rotate(img, 315)


        self.image = pygame.transform.scale(img, (35, 25))
        self.image.set_colorkey((255, 255, 255))

        self.rect = self.image.get_rect()
        self.height = self.image.get_height()
        self.rect.x = x 
        self.rect.y = y


    def update(self):

        if self.diagonal:
            self.rect.y += 9
            self.rect.x += 9

            if self.rect.x > self.game.RESOLUCION[0]:
                self.kill()

            if self.rect.y > 550: # si choca con el suelo:
                self.game.instanciaEfectoImpactoSuelo(self.rect.x, self.rect.y)
                self.kill()

        else:

            self.rect.x += 9

            if self.rect.x > self.game.RESOLUCION[0]:
                self.kill()




# haremos un efecto explosion
class EfectoImpactoBalaSuelo(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game 

        # definimos el tamaño del circulo 
        self.siz = 4 # radio

        self.image = pygame.Surface((self.siz * 2, self.siz * 2))
        pygame.draw.circle(self.image, (255, 155, 0), (self.siz, self.siz), self.siz)
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.bottom = y 



    def update(self):
        self.siz += 2 # aumenta el tamaño

        self.image = pygame.Surface((self.siz * 2, self.siz * 2))
        pygame.draw.circle(self.image, (255, random.randrange(155) + 100, 0), (self.siz, self.siz), self.siz)
        self.image.set_colorkey((0, 0, 0))

        if self.siz >= 24:
            self.kill()




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


