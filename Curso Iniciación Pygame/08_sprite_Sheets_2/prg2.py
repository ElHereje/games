import pygame
import random

# -------------------------------------------------------------
# Codigo prg2.py (1er codigo auxiliar)
# 
# En estos codigos, crearemos las clases que necesitemos
# -------------------------------------------------------------
class Personaje(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game

        # creamos la lista de imagenes
        self.lista_imagenes = []

        # animación por defecto
        self.anima = 7

        #... y cargamos el gráfico
        image_rect = self.game.obtenerGrafico('sSheet1.png', (720, 330))
        self.image = image_rect[0] # solo rescatamos la imagen
        self.rect = image_rect[1] # solo rescatamos la escala/resolución
        
        # cargamos cada imagen de la lista, recorriendo el archivo
        for i in range(3): # 3 filas
            for ii in range(9): # 9 columnas
                img = pygame.Surface((80, 110)) # es lo que sale cada animacion del sprite
                img.blit(self.image, (0, 0), (ii*80, i*110, 80, 110))
                img.set_colorkey((0,0,0)) # transparentamos
                self.lista_imagenes.append(img)

        self.image = self.lista_imagenes[0]
        # lo posicionamos
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # giros del personaje
        self.flip = False
        

        # toma de tiempo para las animaciones:
        self.ultimoUpdate = pygame.time.get_ticks()
        



    def update(self):
        self.leerTeclado()

        # vel de la animacion
        calculo = pygame.time.get_ticks()
        if calculo - self.ultimoUpdate > 100: # en segundos
            self.ultimoUpdate = calculo

            # cambio de animnacion
            if self.anima == 9:
                self.anima = 10
            else:
                self.anima = 9

            self.image = self.lista_imagenes[self.anima]
            # giramos la imagen al cambiar de sentido
            self.image = pygame.transform.flip(self.image, self.flip, False)



    def leerTeclado(self):
        tecla = pygame.key.get_pressed()

        if tecla[pygame.K_LEFT]:
            self.rect.x -= 5
            self.flip = True

        elif tecla[pygame.K_RIGHT]:
            self.rect.x += 5
            self.flip = False


        # ------------------ Check Limites ----------------
        if self.rect.x < 0:
            self.rect.x = 0

        elif self.rect.right > self.game.RESOLUCION[0]:
            self.rect.right = self.game.RESOLUCION[0]





# creamos el suelo
class SueloTile(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game 

        image_rect = self.game.obtenerGrafico('SueloTile.png', (80, 110))
        self.image = image_rect[0]
        self.rect = image_rect[1]
        self.rect.bottomleft = (x, y)


    def update(self):
        pass 


