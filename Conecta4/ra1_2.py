import pygame
import random


# 4 creamos la clase Jugador
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