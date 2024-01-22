import pygame
import random

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

        # creamos un id para Pacman
        self.i_d = self.game.lista_pacman

        self.pulsada = 'right' # por defecto es como si estubiera pulsada la dcha
        self.orientacion = 1 # orden de imagen correspondiente a la imagen a la dcha
        self.orientacion_max = self.orientacion + 3 # n de imagenes por movimiento
        self.vel_x = 2
        self.vel_y = 0
        # para determinar la velocidad de las animaciones
        self.ultimo_update = pygame.time.get_ticks()
        self.fotograma_vel = 100 # velocidad de la animación

        # 4 - Para la sirena, ponomeos una cadencia (para no acumular el buffer)
        self.sonarSirena = 0
        self.ultimo_updateSirena = pygame.time.get_ticks()
        self.cadenciaSirena = 500 # cada cuanto suena


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

        # 3 - gestionamos los sonidos de colision con los puntitos, sirena y los items
        if self.check_colision_puntitos():
            self.game.sonido_sirena.stop()
            self.game.sonido_wakawaka.play(maxtime = 500)
        else:
            calculoSirena = pygame.time.get_ticks()
            if calculoSirena - self.ultimo_updateSirena > self.cadenciaSirena:
                self.ultimo_updateSirena = calculoSirena
                self.game.sonido_sirena.play(maxtime = 500)

        if self.check_colision_item():
            self.game.sonido_eatingCherry.play()

        # interseccion entre bloques (cuando es posible el camnio de dirrccipon)
        if self.rect.centerx % (self.game.BSX // 2) == 0 and self.rect.centery % (self.game.BSY // 2) == 0: # si es exacta
            if self.pulsada == 'left':
                self.rect.centerx -= self.game.BSX
                laberinto = self.check_colision_laberinto(self.i_d) # comprueba si ahay colisión
                if not laberinto:
                    self.orientacion = 8
                    self.orientacion_max = self.orientacion - 3
                    self.vel_x = -2
                    self.vel_y = 0

                self.rect.centerx += self.game.BSX

            if self.pulsada == 'right':
                self.rect.centerx += self.game.BSX
                laberinto = self.check_colision_laberinto(self.i_d) # comprueba si ahay colisión
                if not laberinto:
                    self.orientacion = 6
                    self.orientacion_max = self.orientacion - 3
                    self.vel_x = 2
                    self.vel_y = 0

                self.rect.centerx -= self.game.BSX

            if self.pulsada == 'up':
                self.rect.centery -= self.game.BSY
                laberinto = self.check_colision_laberinto(self.i_d) # comprueba si ahay colisión
                if not laberinto:
                    self.orientacion = 11
                    self.orientacion_max = self.orientacion - 3
                    self.vel_x = 0
                    self.vel_y = -2

                self.rect.centery += self.game.BSY

            if self.pulsada == 'down':
                self.rect.centery += self.game.BSY
                laberinto = self.check_colision_laberinto(self.i_d) # comprueba si ahay colisión
                if not laberinto:
                    self.orientacion = 11
                    self.orientacion_max = self.orientacion +  3
                    self.vel_x = 0
                    self.vel_y = 2

                self.rect.centery -= self.game.BSY

        # si no estamos en una intersección:
        laberinto = self.check_colision_laberinto(self.i_d)
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


    # modificamos la función para detectar quien es (id)
    def check_colision_laberinto(self, i_d):
        impactos = pygame.sprite.groupcollide(self.game.lista_laberinto, i_d, False, False) # detecta colisiones entre grupos
        for impacto in impactos:
            return True # true signifioca que hay una pared
        return False
    

    # 2 - creamos una función de colisión con los puntitos y otra para los items
    def check_colision_puntitos(self):
        impactos = pygame.sprite.groupcollide(self.game.lista_puntitos, self.game.lista_pacman, True, False)
        for impacto in impactos:
            return True
        return False
    

    def check_colision_item(self):
        impactos = pygame.sprite.groupcollide(self.game.lista_items, self.game.lista_pacman, True, False)
        for impacto in impactos:
            return True
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

    
class Fantasma(pygame.sprite.Sprite):
    def __init__(self, game, centerx, centery, tipoFantasma, direccion):
        super().__init__()
        self.game = game
        self.tipoF = tipoFantasma # hay 4 tipos de fantasmas

        # añadimos la dirección del movimietno
        self.direccion = direccion

        # añadimos una lista con las animaciones
        self.enemigos_anima = []
        # animacioners por fantasma
        self.nro_fotogramas = 3
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

        # añadimos las variables de las listas de los ojos
        self.cx = self.game.cx
        self.cy = self.game.cy

        # asignamos el elemento a cada valor de la lñista
        self.cx[(self.tipoF - 1) // 10] = self.rect.centerx
        self.cy[(self.tipoF - 1) // 10] = self.rect.centery

        # creamos un dicc con las direcciones alternativas
        self.hacia_donde = {
            'le' : 'doupri', 'ri' : 'updole',
            'up' : 'lerido', 'do' : 'leriup'
        }
        # otro para direccionar los ojos hacia pacman
        self.hacia_donde_velXY = {
            'le' : [-2, 0], 'ri' : [2, 0],
            'up' : [0, -2], 'do' : [0, 2]
        }

        # Array ptosClave (coord. de ptos clave de la pantalla)
        self.ptosClave = [
            # izq
            (75, 225), (225, 225), (225, 425), (225, 675), (225, 575),
            (325, 575), (225, 75), (425, 425), (325, 225), 
            # dcha
            (875, 425), (725, 225), (725, 425), (725, 675), (725, 575),
            (625, 575), (725, 75), (525, 425), (625, 225)
        ]

        # Identyificador a cada fantasma
        self.i_d = self.game.lista_fantasmas[(self.tipoF - 1) // 10]
        # damos movimiento
        self.vel_x = self.hacia_donde_velXY[self.direccion][0]
        self.vel_y = self.hacia_donde_velXY[self.direccion][1]

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

        # Averiguamos hacia donde debe ir (donde está pacman)
        for i in self.ptosClave:
            if self.rect.centerx == i[0] and self.rect.centery == i[1]:
                self.fantasmaPersigue()


        # Damos movimiento a los fantasmas
        if self.rect.centerx % (self.game.BSX // 2) == 0 and self.rect.centery % (self.game.BSY // 2) == 0: # si es exacta
            if self.direccion == 'le':
                self.rect.centerx -= self.game.BSX
                laberinto = self.game.pacman.check_colision_laberinto(self.i_d) # comprueba si ahay colisión
                if not laberinto:
                    self.vel_x = -2
                    self.vel_y = 0
                self.rect.centerx += self.game.BSX

            if self.direccion == 'ri':
                self.rect.centerx += self.game.BSX
                laberinto = self.game.pacman.check_colision_laberinto(self.i_d) # comprueba si ahay colisión
                if not laberinto:
                    self.vel_x = 2
                    self.vel_y = 0
                self.rect.centerx -= self.game.BSX

            if self.direccion == 'up':
                self.rect.centery -= self.game.BSY
                laberinto = self.game.pacman.check_colision_laberinto(self.i_d) # comprueba si ahay colisión
                if not laberinto:
                    self.vel_x = 0
                    self.vel_y = -2
                self.rect.centery += self.game.BSY

            if self.direccion == 'do':
                self.rect.centery += self.game.BSY
                laberinto = self.game.pacman.check_colision_laberinto(self.i_d) # comprueba si ahay colisión
                if not laberinto:
                    self.vel_x = 0
                    self.vel_y = 2
                self.rect.centery -= self.game.BSY

        # si no estamos en una intersección (movimiento de los fantasmas):
        laberinto = self.game.pacman.check_colision_laberinto(self.i_d)
        if not laberinto:
            self.rect.centerx += self.vel_x
            self.rect.centery += self.vel_y
        else:
            self.rect.centerx -= self.vel_x # para que no se quede pegado a la pared
            self.rect.centery -= self.vel_y
            self.elegir_otra_direccion()

        # para determinar movimietno de los ojos, identificamos el fantasma
        self.cx[(self.tipoF - 1) // 10] = self.rect.centerx
        self.cy[(self.tipoF - 1) // 10] = self.rect.centery
        # e indicamos hacia donde deben mirar los ojos
        self.cx[(self.tipoF - 1) // 10 + 4] = self.vel_x
        self.cy[(self.tipoF - 1) // 10 + 4] = self.vel_y

    # funcion para cambio de dirección de los dfantasmas (seleccionamos dos de las letras de las direcc)
    def elegir_otra_direccion(self):
        direcc = self.hacia_donde[self.direccion]
        num_rnd = random.randrange(0, 3, 2)
        self.direccion = direcc[num_rnd] + direcc[num_rnd + 1]

    # función para que nos persigan loos fantasmas
    def fantasmaPersigue(self):
        hor_ver = random.randrange(10)
        # si es hacia arriba o abajo
        if hor_ver < 5:
            if self.game.pacman.rect.centery < self.rect.centery:
                self.direccion = 'up'
            elif self.game.pacman.rect.centery > self.rect.centery:
                self.direccion = 'do'
        else :
            if self.game.pacman.rect.centerx < self.rect.centerx:
                self.direccion = 'le'
            elif self.game.pacman.rect.centerx > self.rect.centerx:
                self.direccion = 'ri'



class Ojos(pygame.sprite.Sprite):
    def __init__(self, game, tipoFantasma):
        super().__init__()
        self.game = game
        self.tipoF = tipoFantasma

        self.image = pygame.image.load('pacGraf/ojos_fantasma.png').convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        fantasmaX = self.game.fantasma.cx
        fantasmaY = self.game.fantasma.cy
        self.rect.centerx = fantasmaX[self.tipoF] + fantasmaX[self.tipoF + 4]
        self.rect.centery = fantasmaY[self.tipoF] + fantasmaY[self.tipoF + 4] - 9 # correccion en pixeles

    def update(self):
        fantasmaX = self.game.fantasma.cx
        fantasmaY = self.game.fantasma.cy
        self.rect.centerx = fantasmaX[self.tipoF] + fantasmaX[self.tipoF + 4]
        self.rect.centery = fantasmaY[self.tipoF] + fantasmaY[self.tipoF + 4] - 9

