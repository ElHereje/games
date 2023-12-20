import pygame


class PacMan(pygame.sprite.Sprite):
    def __init__(self, game, centerx, centery):
        super().__init__() # heredamos los métodos de la clase sprite
        self.game = game

        self.enemigos_anima = [] # lsta de pacmans e imagenes
        for i in range(4): # hay 25 archivos de imágenes
            file = f'pacGraf/pacman{i+1}.png' 
            img = pygame.image.load(file).convert()
            img.set_colorkey((255, 255, 255))
            self.enemigos_anima.append(img)

        # la imagen por defecto es la 1
        self.image = self.enemigos_anima[1]
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery

        self.pulsada = 'right' # por defecto es como si estubiera pulsada la dcha
        self.orientacion = 1 # orden de imagen correspondiente a la imagen a la dcha
        self.orientacion_max = self.orientacion + 3 # n de imagenes por movimiento
        self.vel_x = 2
        self.vel_y = 0
        # para determinar la velocidad de las animaciones
        self.ultimo_update = pygame.time.get_ticks()
        self.fotograma_vel = 100 # velocidad de la animación


    def update(self):
        calculo = pygame.time.get_ticks() # tomas de tiempo
        if calculo - self.ultimo_update > self.fotograma_vel: # cambio de animacion
            self.ultimo_update = calculo
            self.orientacion += 1 # cambiamos la imagen del fotograma
            if self.orientacion >= self.orientacion_max:
                self.orientacion = self.orientacion_max - 3 # si alcanza el tope, volvemos

            centerx = self.rect.centerx
            centery = self.rect.centery
            self.image = self.enemigos_anima[self.orientacion]
            self.rect = self.image.get_rect()
            self.rect.centerx = centerx
            self.rect.centery = centery

    def leer_teclado(self):
        tecla = pygame.key.get_pressed()

        if tecla[pygame.K_LEFT]:
            self.pulsada = 'left'
        elif tecla[pygame.K_RIGHT]:
            self.pulsada = 'right'
        elif tecla[pygame.K_UP]:
            self.pulsada = 'up'
        elif tecla[pygame.K_DOWN]:
            self.pulsada = 'down'



# 1 - creamos la clase LABERINTO
class Laberinto(pygame.sprite.Sprite):
    def __init__(self, game, x, y, valor):
        super().__init__()
        self.game = game

        self.image = pygame.image.load('packGraf/bloquepac.png').convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.valor = valor

    def update(self):
        pass

    