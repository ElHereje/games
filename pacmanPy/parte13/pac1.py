import pygame
import random
from pygame.sprite import Group

'''
Código relativo a PacMAN
'''


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
        self.radius = self.game.BSX // 2 // 1.5
       # id para Pacman
        self.i_d = self.game.lista_pacman

        self.pulsada = 'right' # por defecto es como si estubiera pulsada la dcha
        self.orientacion = 1 # orden de imagen correspondiente a la imagen a la dcha
        self.orientacion_max = self.orientacion + 3 # n de imagenes por movimiento
        self.vel_x = 2
        self.vel_y = 0
        # para determinar la velocidad de las animaciones
        self.ultimo_update = pygame.time.get_ticks()
        self.fotograma_vel = 100 # velocidad de la animación

        # Para la sirena, ponemos una cadencia (para no acumular el buffer)
        self.sonarSirena = 0
        self.ultimo_updateSirena = pygame.time.get_ticks()
        self.cadenciaSirena = 500 # cada cuanto suena


    def update(self):
        if not self.game.enJuego:
            return
        

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

        # gestionamos los sonidos de colision con los puntitos, sirena y los items
        # y hacemos que suyme puntos
        if self.check_colision_puntitos():
            self.game.puntos += self.game.puntitos.sumaPuntos
            self.game.sonido_sirena.stop()
            self.game.sonido_wakawaka.play(maxtime = 500)
        else:
            calculoSirena = pygame.time.get_ticks()
            if calculoSirena - self.ultimo_updateSirena > self.cadenciaSirena:
                self.ultimo_updateSirena = calculoSirena
                self.game.sonido_sirena.play(maxtime = 500)

        if self.check_colision_item():
            # 8 - Añadimos los ptos al comerlos
            self.game.puntos += self.game.items.sumaPtos
            self.game.mostrarPuntosItem = 100  # (contador de tiempo de un mensaje)
            self.game.sonido_sirena.stop()
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


    # unción para detectar quien es (id)
    def check_colision_laberinto(self, i_d):
        impactos = pygame.sprite.groupcollide(self.game.lista_laberinto, i_d, False, False) # detecta colisiones entre grupos
        for impacto in impactos:
            return True # true signifioca que hay una pared
        return False
    

    # función de colisión con los puntitos y otra para los items
    def check_colision_puntitos(self):
        impactos = pygame.sprite.groupcollide(self.game.lista_puntitos, self.game.lista_pacman, True, False)
        for impacto in impactos:
            return True
        return False
    

    def check_colision_item(self):
        impactos = pygame.sprite.groupcollide(self.game.lista_items, self.game.lista_pacman, True, False,
                                              pygame.sprite.collide_circle)
        for impacto in impactos:
            return True
        return False

    # funcion de colision con los fantasmas.
    def check_colision_fantasmas(self):
        impactos = pygame.sprite.groupcollide(self.game.lista_4fantasmas, self.game.lista_pacman, False, False,
                                              pygame.sprite.collide_circle)
        for impacto in impactos:
            self.kill()
            return True
        return False
    
# clase PacManDies (lleva una animación) - el personaje muere y da vueltas
class PacManDies(pygame.sprite.Sprite):
    def __init__(self, game, centerx, centery):
        super().__init__()
        self.game = game

        animaciones = [1, 4, 8, 12] # las imagenes que vamos a usarç
        self.enemigos_anima = []
        for i in animaciones:
            file = f'pacgraf/pacman{i}.png'
            img = pygame.image.load(file).convert()
            img.set_colorkey((255, 255, 255))
            self.enemigos_anima.append(img)

        self.image = self.enemigos_anima[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery

        self.vueltas = 0
        self.fotograma = 0
        self.ultimo_update = pygame.time.get_ticks()
        self.fotograma_vel = 150 # velocidad de animaciçón


    def update(self):
        # solo va a rotar
        calculo = pygame.time.get_ticks()
        if calculo - self.ultimo_update > self.fotograma_vel:
            self.ultimo_update = calculo
            self.fotograma += 1
            if self.fotograma >= 4:
                self.fotograma = 0
                self.vueltas += 1

            centerx = self.rect.centerx
            centery = self.rect.centery

            self.image = self.enemigos_anima[self.fotograma]
            self.rect = self.image.get_rect()
            self.rect.centerx = centerx
            self.rect.centery = centery
        
        if self.vueltas >= 3: # dará 3 vueltas
            self.game.enJuego = True
            self.game.reinstanciar_pacmanfantasmas = True
            self.kill()

        elif self.vueltas == 2:
            self.game.kill_fantasmas = True

    


# Clase para gestionar las vidas
class MostrarVidas(pygame.sprite.Sprite):
    def __init__(self, game, y):
        super().__init__()
        self.game = game
        self.image = pygame.image.load('pacGraf/pacman1.png').convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = self.game.BSX * self.game.NRO_COLUMNAS
        self.rect.y = self.game.BSY * (4 + y)


    def update(self):
        # actualizamos las vidas:
        if self.game.kill_fantasmas:
            self.kill() # eliminamos una da las imágenes de las vidas