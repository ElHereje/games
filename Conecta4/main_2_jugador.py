'''
https://www.youtube.com/playlist?list=PLYu6HJLNYJW3bq3FJ6JceFpco4LN9yLY9

creamos el jugador'''


import pygame
import sys
import ra1_2

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
    # 2 cremoas la lista de sprites (fichas)
    lista_sprites_adibujar = pygame.sprite.Group()

    # creamos el tablero
    for i in lista_x100: # 42 objetos de la clase tablero
        tablero = ra1_2.Tablero(i[0], i[1])
        lista_tablero_adibujar.add(tablero)

    empate = False
    turno = ra1_2.devuelve_numero_random(0, 9)


    # 1 CREAMOS EL OBJETO JUGADOR
    jugador = ra1_2.Jugador()
    # 3... y lo añadimos a una lista
    lista_sprites_adibujar.add(jugador)



    if turno < 5:
        turno = True  # por ahora siempre empezamos nosotros
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

        # 5 comprobamos turno
        if turno:
            if columna == -1:
                jugador.update(RES, columna, lista_x100, lista_cuadricula)
                lista_sprites_adibujar.draw(pantalla)
                columna = jugador.clickar(lista_x100, lista_cuadricula, RES)
            elif columna >= 0:
                turno = jugador.update(RES, columna, lista_x100, lista_cuadricula)
                lista_sprites_adibujar.draw(pantalla)
        else: # cambio de turno
            turno = True # aún no está implementada la máquina
            columna = -1 # para que no se mueva de momento
            jugador = ra1_2.Jugador() # nueva ficha
            lista_sprites_adibujar.add(jugador)
            


        lista_tablero_adibujar.draw(pantalla)
        reloj.tick(FPS) # refresco a 60 fps
        pygame.display.update()

    # ******** FIN BUCLE PPAL **********


    sys.exc_info()



