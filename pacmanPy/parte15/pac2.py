import pygame
import random

'''
Código relativo a los fantasmas
'''

class Fantasma(pygame.sprite.Sprite):
    def __init__(self, game, centerx, centery, tipoFantasma, direccion):
        super().__init__()
        self.game = game
        self.tipoF = tipoFantasma # hay 4 tipos de fantasmas
        self.direccion = direccion
        

        self.enemigos_anima = []
        # Aumentamos el nº de animaciones a 5 (se han añadido 2)
        self.nro_fotogramas = 5
        for i in range(self.nro_fotogramas):
            # condicionamos por tipo de fantasma
            if i < 3: # ..normales
                file  =  f'pacGraf/fantasma{self.tipoF + i}.png'
                img = pygame.image.load(file).convert()
                escalaX = self.game.BSX
                escalaY = self.game.BSY
                img2 = pygame.transform.scale(img, (escalaX, escalaY))
                img2.set_colorkey((255, 255, 255))
                self.enemigos_anima.append(img2)
            else: # .. se convierten en azules....
                file  =  f'pacGraf/fantasmaAzul{i - 2}.png'
                img = pygame.image.load(file).convert()
                escalaX = self.game.BSX
                escalaY = self.game.BSY
                img2 = pygame.transform.scale(img, (escalaX, escalaY))
                img2.set_colorkey((255, 255, 255))
                self.enemigos_anima.append(img2)
        
        # creamos los fantasmas de la lista
        self.image = self.enemigos_anima[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.radius = self.game.BSX // 2 // 1.5 

        # variables de las listas de los ojos
        self.cx = self.game.cx
        self.cy = self.game.cy

        # asignamos el elemento a cada valor de la lista
        self.cx[(self.tipoF - 1) // 10] = self.rect.centerx
        self.cy[(self.tipoF - 1) // 10] = self.rect.centery

        # cdicc con las direcciones alternativas
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

        # Identificador a cada fantasma
        self.i_d = self.game.lista_fantasmas[(self.tipoF - 1) // 10]
        # damos movimiento
        self.vel_x = self.hacia_donde_velXY[self.direccion][0]
        self.vel_y = self.hacia_donde_velXY[self.direccion][1]

        self.fotograma = 0
        self.ultimo_update = pygame.time.get_ticks()
        self.fotograma_vel = 90 # velocidad de animación


    def update(self):
        # si nos han matado, eliminamos tambien lso fantasmas
        if self.game.kill_fantasmas:
            self.kill()

        if not self.game.enJuego:
            return
        
        # verificamos si están en azul...
        if self.game.countDownAzules > 0:
            self.game.countDownAzules -= 1


        calculo = pygame.time.get_ticks() # tomas de tiempo
        if calculo - self.ultimo_update > self.fotograma_vel: # cambio de animacion
            self.ultimo_update = calculo
            self.fotograma += 1 # cambiamos la imagen del fotograma
            if self.fotograma >= self.nro_fotogramas - 2: # 3c ... sin contar con los azules..
                self.fotograma = 0 # si alcanza el tope, volvemos

            # puntos intermitentes para avisar que se acaba el tiempo
            if self.game.countDownAzules <= 0:
                centerx = self.rect.centerx
                centery = self.rect.centery
                self.image = self.enemigos_anima[self.fotograma]
                self.rect = self.image.get_rect()
                self.rect.centerx = centerx
                self.rect.centery = centery

            elif self.game.countDownAzules < 300: 
                centerx = self.rect.centerx
                centery = self.rect.centery
                self.image = self.enemigos_anima[self.fotograma + 2] # así parpadea
                self.rect = self.image.get_rect()
                self.rect.centerx = centerx
                self.rect.centery = centery

            else:
                centerx = self.rect.centerx
                centery = self.rect.centery
                self.image = self.enemigos_anima[self.nro_fotogramas - 2] # pone uno en concreto
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
        escalaX = self.game.BSX // 2.5  
        escalaY = self.game.BSY // 10

        img = pygame.image.load('pacGraf/ojos_fantasma.png').convert()
        self.image = pygame.transform.scale(img, (escalaX, escalaY))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        fantasmaX = self.game.fantasma.cx
        fantasmaY = self.game.fantasma.cy
        self.rect.centerx = fantasmaX[self.tipoF] + fantasmaX[self.tipoF + 4]
        self.coorYcorrecion = (self.game.BSY * 9) / 50
        self.rect.centery = fantasmaY[self.tipoF] + fantasmaY[self.tipoF + 4] - self.coorYcorrecion # correccion en pixeles

    def update(self):
        if self.game.kill_fantasmas:
            self.kill()

        fantasmaX = self.game.fantasma.cx
        fantasmaY = self.game.fantasma.cy
        self.rect.centerx = fantasmaX[self.tipoF] + fantasmaX[self.tipoF + 4]
        self.rect.centery = fantasmaY[self.tipoF] + fantasmaY[self.tipoF + 4] - self.coorYcorrecion