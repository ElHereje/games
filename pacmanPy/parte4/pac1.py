import pygame


class PacMan(pygame.sprite.Sprite):
    def __init__(self, game, centerx, centery):
        super().__init__() # heredamos los métodos de la clase sprite
        self.game = game

        self.enemigos_anima = [] # lsta de pacmans e imagenes
        for i in range(14): # hay 25 archivos de imágenes
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
                self.orientacion = self.orientacion_max - 2 # si alcanza el tope, volvemos

            centerx = self.rect.centerx
            centery = self.rect.centery
            self.image = self.enemigos_anima[self.orientacion]
            self.rect = self.image.get_rect()
            self.rect.centerx = centerx
            self.rect.centery = centery

        # interseccion entre bloques (cuando es posible el camnio de dirrccipon)
        if self.rect.centerx % 25 == 0 and self.rect.centery % 25 == 0: # si es exacta
            if self.pulsada == 'left':
                self.rect.centerx -= self.game.BSX
                laberinto = self.check_colision_laberinto() # comprueba si ahay colisión
                if not laberinto:
                    self.orientacion = 8
                    self.orientacion_max = self.orientacion - 3
                    self.vel_x = -2
                    self.vel_y = 0

                self.rect.centerx += self.game.BSX

            if self.pulsada == 'right':
                self.rect.centerx += self.game.BSX
                laberinto = self.check_colision_laberinto() # comprueba si ahay colisión
                if not laberinto:
                    self.orientacion = 6
                    self.orientacion_max = self.orientacion - 3
                    self.vel_x = 2
                    self.vel_y = 0

                self.rect.centerx -= self.game.BSX

            if self.pulsada == 'up':
                self.rect.centery -= self.game.BSY
                laberinto = self.check_colision_laberinto() # comprueba si ahay colisión
                if not laberinto:
                    self.orientacion = 11
                    self.orientacion_max = self.orientacion - 3
                    self.vel_x = 0
                    self.vel_y = -2

                self.rect.centery += self.game.BSY

            if self.pulsada == 'down':
                self.rect.centery += self.game.BSY
                laberinto = self.check_colision_laberinto() # comprueba si ahay colisión
                if not laberinto:
                    self.orientacion = 11
                    self.orientacion_max = self.orientacion +  3
                    self.vel_x = 0
                    self.vel_y = 2

                self.rect.centery -= self.game.BSY

        # si no estamos en una intersección:
        laberinto = self.check_colision_laberinto()
        if not laberinto:
            self.rect.centerx += self.vel_x
            self.rect.centery += self.vel_y
        else:
            self.rect.centerx -= self.vel_x # para que no se quede pegado a la pared
            self.rect.centery -= self.vel_y


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


    def check_colision_laberinto(self):
        impactos = pygame.sprite.groupcollide(self.game.lista_laberinto, self.game.lista_pacman, False, False) # detecta colisiones entre grupos
        for impacto in impactos:
            return True # true signifioca que hay una pared
        return False


class Laberinto(pygame.sprite.Sprite):
    def __init__(self, game, x, y, valor):
        super().__init__()
        self.game = game

        self.image = pygame.image.load('pacGraf/bloquepac1.png').convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.valor = valor

    def update(self):
        pass


class Puntitos(pygame.sprite.Sprite):
    def __init__(self, game, centerx, centery, valor):
        super().__init__()
        self.game = game

        self.image = pygame.image.load('pacGraf/pildopac.png').convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.valor = valor # al compartar con laberinto --> 0 = vacio / 1 = puntito

    def update(self):
        pass


class Items(pygame.sprite.Sprite):
    def __init__(self, game, centerx, centery):
        super().__init__()
        self.game = game

        self.image = pygame.image.load('pacGraf/item1.png').convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery

    def update(self):
        pass

    
# 1 Creamos la clase fantasma
class Fantasma(pygame.sprite.Sprite):
    def __init__(self, game, centerx, centery, tipoFantasma, direccion):
        super().__init__()
        self.game = game
        self.tipoF = tipoFantasma # hay 4 tipos de fantasmas
        # añadimos una lista con las animaciones
        self.enemigos_anima = []
        # animacioners por fantasma
        self.nro_fotogramas = 2
        # vamos metiendo los fantasmas en la lista
        for i in range(self.nro_fotogramas):
            file  =  f'pacGraf/fantasma{self.tipoF + i}.png'
            img = pygame.image.load(file).convert()
            img.set_colorkey((255, 255, 255))
            self.enemigos_anima.append(img)
        
        # creamos los fantasmas de la lista
        self.image = self.enemigos_anima[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.fotograma = 0
        self.ultimo_update = pygame.time.get_ticks()
        self.fotograma_vel = 90 # velocidad de animación


    def update(self):
        calculo = pygame.time.get_ticks() # tomas de tiempo
        if calculo - self.ultimo_update > self.fotograma_vel: # cambio de animacion
            self.ultimo_update = calculo
            self.fotograma += 1 # cambiamos la imagen del fotograma
            if self.fotograma >= self.nro_fotogramas:
                self.fotograma = 0 # si alcanza el tope, volvemos

            centerx = self.rect.centerx
            centery = self.rect.centery
            self.image = self.enemigos_anima[self.fotograma]
            self.rect = self.image.get_rect()
            self.rect.centerx = centerx
            self.rect.centery = centery