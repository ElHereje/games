'''creamos el tablero'''


import pygame
import sys
import ra1_1

RESOLUCION = 700 # 700X700 (600 + FICHA QUE CAE)
RES = RESOLUCION # para acortar nombres
FPS = 60

BLANCO = (200, 200, 200)
ROJO = (230, 0, 0)
AZUL = (0, 210, 220)
GRIS = (65, 65, 65)

pygame.init()
pantalla = pygame.display.set_mode((RES, RES))
pygame.display.set_caption('Conecta 4 - Tutorizado')
pantalla.fill(GRIS)
reloj = pygame.time.Clock()

ganadas = 0
perdidas = 0
empates = 0
salir = False

while not salir:

    lista_cuadricula = ['_'] * 42 # lista de 42 (7x6) guiones

    lista_x100 = [] # se le asignan coordenadas a cada cuadrícula
    for y in range(6):
        for x in range(7):
            lista_x100.append((x * (RES // 7), (y + 1) * (RES // 7)))

    vacia = '_'

    lista_tablero_adibujar = pygame.sprite.Group()

    # creamos el tablero
    for i in lista_x100: # 42 objetos de la clase tablero
        tablero = ra1_1.Tablero(i[0], i[1])
        lista_tablero_adibujar.add(tablero)

    empate = False
    turno = ra1_1.devuelve_numero_random(0, 9)

    if turno < 5:
        turno = True  # empezamos nosotros
        columna = -1
    else:
        turno = True
        columna = -1


    # ********** BUCLE PPAL ************

    while not empate:
        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                empate = True
                salir = True
                sys.exit()
        
        pantalla.fill(GRIS)
        lista_tablero_adibujar.draw(pantalla)
        reloj.tick(FPS) # refresco a 60 fps
        pygame.display.update()



