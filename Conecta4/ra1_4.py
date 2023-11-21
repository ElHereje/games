import pygame
import random


class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("ficha_roja.png").convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.y = 0 # posicion inicial de la ficha
        self.vel_y = 10 # velocidad ala que cae

    
    def update(self, RES, columna, lista_x100, lista_cuadricula): # cuando cae la ficha
        if columna == -1: # no cae... solo sigue al ratón en X
            mouse_xy = pygame.mouse.get_pos()
            self.rect.x = mouse_xy[0]
            convertir = self.convertir_coordenadasxy(RES)
            self.rect.x = convertir[0]

        elif columna >= 0:
            if self.rect.bottom >= RES: # si llega al fondo...
                lista_cuadricula[columna + 35] = 'O'
                return False # cambio de turno

            xy = (self.rect.x, self.rect.y) 
            i = 0 # contador ... para ver si choca con otra ficha
            for check_xy in lista_x100:
                if check_xy == xy:
                    if lista_cuadricula[i + 7] != '_':
                        lista_cuadricula[i] = 'O'
                        return False
                i += 1
            # si no es el fondo, no choca con otra, continua callendo...
            self.rect.y += self.vel_y
            return True

    
    def clickar(self, lista_x100, lista_cuadricula, RES):
        hacer_click = pygame.mouse.get_pressed()
        if hacer_click[0]: # si pulsamos le botón izq....
            columna = self.convertir_en_7columnas(RES)
            if lista_cuadricula[columna] == '_': #... si está vacía
                self.rect.x = columna * RES // 7
                return columna
            else:
                return -1 # la ficha no sale
        return -1 # la ficha no sale

    def convertir_coordenadasxy(self, RES): # convertimos coordenadas en múltiplos de 100
        return (self.rect.left // (RES // 7)) * RES // 7, (self.rect.top // (RES // 7)) * RES // 7

    def convertir_en_7columnas(self, RES):
        return self.rect.left // (RES // 7) # convierte una coordenada en un columna


# 4 - Creamos la clase CPU
class Cpu(pygame.sprite.Sprite):
    def __init__(self, RES, lista_cuadricula, cpu_col):
        super().__init__()
        self.image = pygame.image.load("ficha_verde.png").convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.vel_y = 10
        if cpu_col == -1: # columna al azar
            salir = False
            while not salir:
                self.columna = devuelve_numero_random(0, 6)
                if lista_cuadricula[self.columna] == '_': # si la 1º fila esta libre
                    salir = True

            self.rect.x = self.columna * (RES // 7)
        else:
            self.rect.x = cpu_col
            self.columna = cpu_col // (RES // 7)

    def update(self, RES, lista_x100, lista_cuadricula):
        if self.rect.bottom >= RES: # si ha llegado al final del tablero...
            lista_cuadricula[self.columna + 35] = 'X'
            return True

        xy = (self.rect.x, self.rect.y)
        i = 0
        for check_xy in lista_x100:
            if check_xy == xy: # comprobamos si hay ficha debajo...
                if lista_cuadricula[i + 7] != '_':
                    lista_cuadricula[i] = 'X'
                    return True
            i += 1

        self.rect.y += self.vel_y
        return False



class Tablero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() 
        self.image = pygame.image.load("tablero_conecta4.png").convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def devuelve_numero_random(cero, ocho):
    return random.randint(cero, ocho)


def checkear_4enraya(lista_check_horiz, lista_check_vert, l_cuadricula, xo):
    for i in lista_check_horiz:
        if l_cuadricula[i] == xo and l_cuadricula[i + 1] == xo and l_cuadricula[i + 2] == xo and \
        l_cuadricula[i + 3] == xo:
            return True  # ... se es que es cierto 

    for i in lista_check_vert:
        if l_cuadricula[i] == xo and l_cuadricula[i + 7] == xo and l_cuadricula[i + 14] == xo and \
        l_cuadricula[i + 21] == xo:
            return True

    return False

# 1 - función para comprobar 4enRaya Diagonal
def checkear_diagonales(lista_check_diag, l_cuadricula, xo):
    contador = 0 # limita diagonales hacia la izq o dcha
    for i in lista_check_diag:
        if contador < 12: # hacia la dcha
            if l_cuadricula[i] == xo and l_cuadricula[i + 8] == xo and l_cuadricula[i + 16] == xo and \
            l_cuadricula[i + 24] == xo:
                return True # hay cuatro en raya
        else: # hacia la izq
            if l_cuadricula[i] == xo and l_cuadricula[i + 6] == xo and l_cuadricula[i + 12] == xo and \
            l_cuadricula[i + 18] == xo:
                return True # hay cuatro en raya

        contador += 1 

    return False # No hay cuatro en raya
