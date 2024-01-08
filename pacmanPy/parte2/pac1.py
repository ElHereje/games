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

        # 4 condicionales para el movimietno
        # interseccion entre bloques (cuando es posible el camnio de dirrccipon)
        if self.rect.centerx % 2 == 0 and self.rect.centery % 25 == 0: # sie es exacta
            if self.pulsada == 'left':
                self.rect.centerx -= self.game.BSX
                laberinto = self.check_colision_laberinto() # comprueba si ahay colisión
                if not laberinto:
                    self.orientacion = 5
                    self.orientacion_max = self.orientacion + 4
                    self.vel_x = -2
                    self.vel_y = 0

                self.rect.centerx += self.game.BSX

            if self.pulsada == 'right':
                self.rect.centerx += self.game.BSX
                laberinto = self.check_colision_laberinto() # comprueba si ahay colisión
                if not laberinto:
                    self.orientacion = 1
                    self.orientacion_max = self.orientacion + 4
                    self.vel_x = -2
                    self.vel_y = 0

                self.rect.centerx -= self.game.BSX

            if self.pulsada == 'up':
                self.rect.centery -= self.game.BSY
                laberinto = self.check_colision_laberinto() # comprueba si ahay colisión
                if not laberinto:
                    self.orientacion = 8
                    self.orientacion_max = self.orientacion + 4
                    self.vel_x = -2
                    self.vel_y = 0

                self.rect.centery += self.game.BSY

            if self.pulsada == 'down':
                self.rect.centery += self.game.BSY
                laberinto = self.check_colision_laberinto() # comprueba si ahay colisión
                if not laberinto:
                    self.orientacion = 11
                    self.orientacion_max = self.orientacion + 4
                    self.vel_x = -2
                    self.vel_y = 0

                self.rect.centery -= self.game.BSY

        # si no estamos en uina intersección:
        laberinto = self.check_colision_laberinto()
        if not laberinto:
            self.rect.centerx += self.vel_x
            self.rect.centery += self.vel_y
        else:
            self.rect.centerx += -self.vel_x # para que no se quede pegado a la pared
            self.rect.centery += -self.vel_y


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

    # 5 - creamos la función check_colisiópn_laberinto()
            # nos da true o false si es que hay colisiones con als paredes
    def check_colision_laberinto(self):
        impactos = pygame.sprite.groupcollide(self.game.lista_laberinto, self.game.lista_pacman, False, False) # detecta colisiones entre grupos
        for impacto in impactos:
            # info en consola para omproar las coordenadas
            print(impacto.rect.centerx, impacto.rect.centery, self.rect.centerx, self.rect.centery)
            return True # true signifioca que hay una pared
        return False


# 1 - creamos la clase LABERINTO
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

    