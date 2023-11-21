'''
https://www.youtube.com/playlist?list=PLYu6HJLNYJW3bq3FJ6JceFpco4LN9yLY9

checkeamos 4enRaya diagonales y que juegue la CPU.'''


import pygame
import sys
import ra1_4

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


    # 1 se añaden las lista de chequeo de 4 en raya
    lista_check_horiz = []
    i = 0
    for y in range(6):
        for x in range(4):
            lista_check_horiz.append(i)
            i += 1
        i += 3 # hace el salto de fila

    lista_check_vert = []
    i = 0
    col = 0
    for x in range(7):
        i += col 
        col += 1
        for y in range(3):
            lista_check_vert.append(i)
            i += 7
        i = 0

    lista_check_diag = [
        0, 1, 2, 3, 7, 8, 9, 10, 14, 15, 16, 17,
        3, 4, 5, 6, 10, 11, 12, 13, 17, 18, 19, 20
    ]


    vacia = '_'

    lista_tablero_adibujar = pygame.sprite.Group()
    lista_sprites_adibujar = pygame.sprite.Group()

    # creamos el tablero
    for i in lista_x100: # 42 objetos de la clase tablero
        tablero = ra1_4.Tablero(i[0], i[1])
        lista_tablero_adibujar.add(tablero)

    jugador_cuatro_en_raya = False
    jugador_cuatro_en_diag = False # provisional, ya que no está implementado
    cpu_cuatro_en_raya = False
    cpu_cuatro_en_diag = False # provisional, ya que no está implementado

    empate = False
    turno = ra1_4.devuelve_numero_random(0, 9)


    jugador = ra1_4.Jugador()
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

        jugador_cuatro_en_raya = ra1_4.checkear_4enraya(lista_check_horiz, lista_check_vert, lista_cuadricula, 'O')
        cpu_cuatro_en_raya = ra1_4.checkear_4enraya(lista_check_horiz, lista_check_vert, lista_cuadricula, 'X')

        # 2 - Comprobamos 4enRaya diagonales
        jugador_cuatro_en_diag = ra1_4.checkear_diagonales(lista_check_diag,lista_cuadricula, 'O')
        cpu_cuatro_en_diag = ra1_4.checkear_diagonales(lista_check_diag,lista_cuadricula, 'X')


        if jugador_cuatro_en_raya or jugador_cuatro_en_diag:
            print('GANA Jugador!!! 4 en Raya!', jugador_cuatro_en_raya, cpu_cuatro_en_raya, empate)
            ganadas += 1
            break

        # 5 - comprobamos 4enRaya de la CPU y el empate
        elif cpu_cuatro_en_raya or cpu_cuatro_en_diag:
            print('GANA la CPU !!! 4 en Raya!',jugador_cuatro_en_raya, cpu_cuatro_en_raya , empate)
            perdidas += 1
            break

        elif empate:
            print('Empate! ', jugador_cuatro_en_raya, cpu_cuatro_en_raya, empate)
            empates += 1
            break


        # comprobamos turno
        if turno:
            if columna == -1:
                jugador.update(RES, columna, lista_x100, lista_cuadricula)
                lista_sprites_adibujar.draw(pantalla)
                columna = jugador.clickar(lista_x100, lista_cuadricula, RES)
            elif columna >= 0:
                turno = jugador.update(RES, columna, lista_x100, lista_cuadricula)
                lista_sprites_adibujar.draw(pantalla)
                # 3 implementamos el turno de la CPU
                if not turno:
                    cpu_col = -1
                    cpu = ra1_4.Cpu(RES, lista_cuadricula, cpu_col) # implementamos un objeto CPU
                    lista_sprites_adibujar.add(cpu)

        else: # cambio de turno
            turno = cpu.update(RES, lista_x100, lista_cuadricula)
            lista_sprites_adibujar.draw(pantalla)
            if turno:
                columna = -1 # para que no se mueva de momento
                jugador = ra1_4.Jugador() # nueva ficha
                lista_sprites_adibujar.add(jugador)
            


        lista_tablero_adibujar.draw(pantalla)
        reloj.tick(FPS) # refresco a 60 fps
        pygame.display.update()

    # ******** FIN BUCLE PPAL **********


    sys.exit()