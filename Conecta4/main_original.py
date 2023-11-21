import pygame
import sys
import ra1

RESOLUCION = 700
RES = RESOLUCION
FPS = 60

BLANCO = (200, 200, 200)
ROJO = (230, 0, 0)
AZUL = (0, 210, 220)
GRIS = (65, 65, 65)

pygame.init()
pantalla = pygame.display.set_mode((RES, RES))
pygame.display.set_caption('Conecta 4 by Juan Eguia')
pantalla.fill(GRIS)
reloj = pygame.time.Clock()

ganadas = 0
perdidas = 0
empates = 0
salir = False

while not salir:

    lista_cuadricula = ['_'] * 42
    
    lista_x100 = []
    for y in range(6):
        for x in range(7):
            lista_x100.append((x * (RES // 7), (y + 1) * (RES // 7)))

    lista_check_horiz = []
    i = 0
    for y in range(6):
        for x in range(4):
            lista_check_horiz.append(i)
            i += 1
        i += 3 

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

    lista_sprites_adibujar = pygame.sprite.Group()
    lista_tablero_adibujar = pygame.sprite.Group()

    print(lista_x100)
    print(lista_cuadricula)

    for i in lista_x100:
        tablero = ra1.Tablero(i[0], i[1])
        lista_tablero_adibujar.add(tablero)

    jugador_cuatro_en_raya = False
    jugador_cuatro_en_diag = False
    cpu_cuatro_en_raya = False
    cpu_cuatro_en_diag = False
    empate = False
    turno = ra1.devuelve_numero_random(0, 9)

    if turno < 5:
        turno = True
        columna = -1
        jugador = ra1.Jugador()
        lista_sprites_adibujar.add(jugador)
    else:
        turno = False
        cpu_col = -1
        cpu = ra1.Cpu(RES, lista_cuadricula, cpu_col)
        lista_sprites_adibujar.add(cpu)

    # ************** BUCLE PRINCIPAL (MAIN LOOP) **************
    while not empate:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                empate = True
                salir = True
                sys.exit()

        pantalla.fill(GRIS)
        
        jugador_cuatro_en_raya = ra1.checkear_4enraya(lista_check_horiz, lista_check_vert, lista_cuadricula, 'O')
        jugador_cuatro_en_diag = ra1.checkear_diagonales(lista_check_diag, lista_cuadricula, 'O')
        cpu_cuatro_en_raya = ra1.checkear_4enraya(lista_check_horiz, lista_check_vert, lista_cuadricula, 'X')
        cpu_cuatro_en_diag = ra1.checkear_diagonales(lista_check_diag, lista_cuadricula, 'X')
        empate = ra1.checkear_empate(vacia, lista_cuadricula)

        if jugador_cuatro_en_raya or jugador_cuatro_en_diag:
            print('GANA Jugador!!! 4 en Raya!', jugador_cuatro_en_raya, cpu_cuatro_en_raya, empate)
            ganadas += 1
            break
        elif cpu_cuatro_en_raya or cpu_cuatro_en_diag:
            print('GANA la CPU !!! 4 en Raya!',jugador_cuatro_en_raya, cpu_cuatro_en_raya , empate)
            perdidas += 1
            break
        elif empate:
            print('Empate! ', jugador_cuatro_en_raya, cpu_cuatro_en_raya, empate)
            empates += 1
            break

        if turno:
            if columna == -1:
                jugador.update(RES, columna, lista_x100, lista_cuadricula)
                lista_sprites_adibujar.draw(pantalla)
                columna = jugador.clickar(lista_x100, lista_cuadricula, RES)
            elif columna >= 0:
                turno = jugador.update(RES, columna, lista_x100, lista_cuadricula)
                lista_sprites_adibujar.draw(pantalla)
                if not turno:
                    cpu_col = ra1.cpu_intenta_4raya_v2(lista_check_horiz, lista_check_vert,
                    lista_check_diag, lista_cuadricula, lista_x100)
                    if cpu_col == -1:
                        cpu_col = ra1.cpu_defiende(lista_check_horiz, lista_check_vert,
                        lista_check_diag, lista_cuadricula, lista_x100)
                        cpu = ra1.Cpu(RES, lista_cuadricula, cpu_col)
                        lista_sprites_adibujar.add(cpu)
                    else:
                        cpu = ra1.Cpu(RES, lista_cuadricula, cpu_col)
                        lista_sprites_adibujar.add(cpu) 
        else:
            turno = cpu.update(RES, lista_x100, lista_cuadricula)
            lista_sprites_adibujar.draw(pantalla)
            if turno:
                columna = -1
                jugador = ra1.Jugador()
                lista_sprites_adibujar.add(jugador)


        lista_tablero_adibujar.draw(pantalla)
        if turno:
            ra1.dibuja_texto(pantalla, 'Turno del Jugador', 25, RES // 2, 10)
        elif not turno:
            ra1.dibuja_texto(pantalla, 'Turno de la CPU', 25, RES // 2, 10)

        #print(columna, turno, jugador.rect.left, jugador.rect.top)
        #print(lista_cuadricula)
        #print(lista_check_vert)

        reloj.tick(FPS)
        pygame.display.update()

    # ******************* FIN BUCLE PRINCIPAL **********************
    #print(jugador_cuatro_en_raya, cpu_cuatro_en_raya, empate)
    #sys.exit()

    otra_partida = False
    while not otra_partida:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if pygame.K_SPACE:
                    otra_partida = True

        pantalla.fill(GRIS)
        lista_sprites_adibujar.draw(pantalla)
        lista_tablero_adibujar.draw(pantalla)

        if jugador_cuatro_en_raya:
            ra1.dibuja_texto(pantalla,' GANA Jugador!!! ', 50, RES // 2, RES //2 - 100)
        elif cpu_cuatro_en_raya:
            ra1.dibuja_texto(pantalla,' GANA la CPU !!! ', 50, RES // 2, RES //2 - 100)
        elif empate:
            ra1.dibuja_texto(pantalla,' EMPATE! ', 50, RES // 2, RES //2 - 100)

        ra1.dibuja_texto(pantalla, 'Pulse la <barra espaciadora> para jugar otra vez...', 
            25, RES // 2, RES - 50)

        ra1.dibuja_texto(pantalla, 'Ganadas: {}   Perdidas: {}   Empates: {} '.format(ganadas, perdidas, empates),
                     30, RES // 2,  10)

        reloj.tick(FPS)
        pygame.display.update()

    # ******** Otra partida ********* 
    impactos = pygame.sprite.groupcollide(lista_sprites_adibujar, lista_tablero_adibujar, True, True)
    for impacto in impactos:
        print(impacto)

sys.exit()


