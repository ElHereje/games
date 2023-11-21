import pygame
import random


class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ficha_roja.png").convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.vel_y = 10

    def update(self, RES, columna, lista_x100, lista_cuadricula):
        if columna == -1:
            mouse_xy = pygame.mouse.get_pos()
            self.rect.x = mouse_xy[0]
            convertir = self.convertir_coordenadasxy(RES)
            self.rect.x = convertir[0]

        elif columna >= 0:
            if self.rect.bottom >= RES:
                lista_cuadricula[columna + 35] = 'O'
                return False

            xy = (self.rect.x, self.rect.y) 
            i = 0
            for check_xy in lista_x100:
                if check_xy == xy:
                    if lista_cuadricula[i + 7] != '_':
                        lista_cuadricula[i] = 'O'
                        return False
                i += 1

            self.rect.y += self.vel_y
            return True

    def clickar(self, lista_x100, lista_cuadricula, RES):
        hacer_click = pygame.mouse.get_pressed()
        if hacer_click[0]:
            columna = self.convertir_en_7columnas(RES)
            if lista_cuadricula[columna] == '_':
                self.rect.x = columna * RES // 7
                return columna
            else:
                return -1 
        return -1

    def convertir_coordenadasxy(self, RES):
        return (self.rect.left // (RES // 7)) * RES // 7, (self.rect.top // (RES // 7)) * RES // 7

    def convertir_en_7columnas(self, RES):
        return self.rect.left // (RES // 7)


class Cpu(pygame.sprite.Sprite):
    def __init__(self, RES, lista_cuadricula, cpu_col):
        super().__init__()
        self.image = pygame.image.load("ficha_verde.png").convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.vel_y = 10
        if cpu_col == -1:
            salir = False
            while not salir:
                self.columna = devuelve_numero_random(0, 6)
                if lista_cuadricula[self.columna] == '_':
                    salir = True

            self.rect.x = self.columna * (RES // 7)
        else:
            self.rect.x = cpu_col
            self.columna = cpu_col // (RES // 7)

    def update(self, RES, lista_x100, lista_cuadricula):
        if self.rect.bottom >= RES:
            lista_cuadricula[self.columna + 35] = 'X'
            return True

        xy = (self.rect.x, self.rect.y)
        i = 0
        for check_xy in lista_x100:
            if check_xy == xy:
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


def cpu_intenta_4raya(lista_check_horiz, lista_check_vert, lista_check_diag, l_cuadricula, lista_x100):
    for i in range(42):
        if l_cuadricula[i] == '_':
            l_cuadricula[i] = 'X'
            for check in lista_check_horiz:
                if l_cuadricula[check] == 'X' and l_cuadricula[check + 1] == 'X' and l_cuadricula[check + 2] == 'X' and \
                l_cuadricula[check + 3] == 'X':
                    l_cuadricula[i] = '_'
                    coord_x = lista_x100[i][0]
                    return coord_x


            for check in lista_check_vert:
                if l_cuadricula[check] == 'X' and l_cuadricula[check + 7] == 'X' and l_cuadricula[check + 14] == 'X' and \
                l_cuadricula[check + 21] == 'X':
                    l_cuadricula[i] = '_'
                    coord_x = lista_x100[i][0]
                    return coord_x

            contador = 0
            for check in lista_check_diag:
                if contador < 12:
                    if l_cuadricula[check] == 'X' and l_cuadricula[check + 8] == 'X' and l_cuadricula[check + 16] == 'X' and \
                    l_cuadricula[check + 24] == 'X':
                        l_cuadricula[i] = '_'
                        coord_x = lista_x100[i][0]
                        return coord_x
                else:
                    if l_cuadricula[check] == 'X' and l_cuadricula[check + 6] == 'X' and l_cuadricula[check + 12] == 'X' and \
                    l_cuadricula[check + 18] == 'X':
                        l_cuadricula[i] = '_'
                        coord_x = lista_x100[i][0]
                        return coord_x

                contador += 1

            l_cuadricula[i] = '_'

    return -1


def cpu_intenta_4raya_v2(lista_check_horiz, lista_check_vert, lista_check_diag, l_cuadricula, lista_x100):
    for i in range(7):
        c_final = i + 35
        bandera = True
        for lanzam in range(c_final, i, -7):
            if l_cuadricula[lanzam] == '_' and bandera == True:
                bandera = False
                l_cuadricula[lanzam] = 'X'
                for check in lista_check_horiz:
                    if l_cuadricula[check] == 'X' and l_cuadricula[check + 1] == 'X' and l_cuadricula[check + 2] == 'X' and \
                    l_cuadricula[check + 3] == 'X':
                        l_cuadricula[lanzam] = '_'
                        coord_x = lista_x100[i][0]
                        return coord_x


                for check in lista_check_vert:
                    if l_cuadricula[check] == 'X' and l_cuadricula[check + 7] == 'X' and l_cuadricula[check + 14] == 'X' and \
                    l_cuadricula[check + 21] == 'X':
                        l_cuadricula[lanzam] = '_'
                        coord_x = lista_x100[i][0]
                        return coord_x

                contador = 0
                for check in lista_check_diag:
                    if contador < 12:
                        if l_cuadricula[check] == 'X' and l_cuadricula[check + 8] == 'X' and l_cuadricula[check + 16] == 'X' and \
                        l_cuadricula[check + 24] == 'X':
                            l_cuadricula[lanzam] = '_'
                            coord_x = lista_x100[i][0]
                            return coord_x
                    else:
                        if l_cuadricula[check] == 'X' and l_cuadricula[check + 6] == 'X' and l_cuadricula[check + 12] == 'X' and \
                        l_cuadricula[check + 18] == 'X':
                            l_cuadricula[lanzam] = '_'
                            coord_x = lista_x100[i][0]
                            return coord_x

                    contador += 1

                l_cuadricula[lanzam] = '_'
                
    return -1


def cpu_defiende(lista_check_horiz, lista_check_vert, lista_check_diag, l_cuadricula, lista_x100):
    for i in range(7):
        c_final = i + 35
        bandera = True
        for lanzam in range(c_final, i, -7):
            if l_cuadricula[lanzam] == '_' and bandera == True:
                bandera = False
                l_cuadricula[lanzam] = 'O'
                for check in lista_check_horiz:
                    if l_cuadricula[check] == 'O' and l_cuadricula[check + 1] == 'O' and l_cuadricula[check + 2] == 'O' and \
                    l_cuadricula[check + 3] == 'O':
                        l_cuadricula[lanzam] = '_'
                        coord_x = lista_x100[i][0]
                        return coord_x


                for check in lista_check_vert:
                    if l_cuadricula[check] == 'O' and l_cuadricula[check + 7] == 'O' and l_cuadricula[check + 14] == 'O' and \
                    l_cuadricula[check + 21] == 'O':
                        l_cuadricula[lanzam] = '_'
                        coord_x = lista_x100[i][0]
                        return coord_x

                contador = 0
                for check in lista_check_diag:
                    if contador < 12:
                        if l_cuadricula[check] == 'O' and l_cuadricula[check + 8] == 'O' and l_cuadricula[check + 16] == 'O' and \
                        l_cuadricula[check + 24] == 'O':
                            l_cuadricula[lanzam] = '_'
                            coord_x = lista_x100[i][0]
                            return coord_x
                    else:
                        if l_cuadricula[check] == 'O' and l_cuadricula[check + 6] == 'O' and l_cuadricula[check + 12] == 'O' and \
                        l_cuadricula[check + 18] == 'O':
                            l_cuadricula[lanzam] = '_'
                            coord_x = lista_x100[i][0]
                            return coord_x

                    contador += 1

                l_cuadricula[lanzam] = '_'
                
    return -1

   
def juega_cpu_random(tirada_random, lista_cuadricula):
    if lista_cuadricula[tirada_random] == '_':
        lista_cuadricula[tirada_random] = 'X'
        return True

    return False


def devuelve_numero_random(cero, ocho):
    return random.randint(cero, ocho)

 
def checkear_4enraya(lista_check_horiz, lista_check_vert, l_cuadricula, xo):
    for i in lista_check_horiz:
        if l_cuadricula[i] == xo and l_cuadricula[i + 1] == xo and l_cuadricula[i + 2] == xo and \
        l_cuadricula[i + 3] == xo:
            return True

    for i in lista_check_vert:
        if l_cuadricula[i] == xo and l_cuadricula[i + 7] == xo and l_cuadricula[i + 14] == xo and \
        l_cuadricula[i + 21] == xo:
            return True

    return False

def checkear_diagonales(lista_check_diag, l_cuadricula, xo):
    contador = 0
    for i in lista_check_diag:
        if contador < 12:
            if l_cuadricula[i] == xo and l_cuadricula[i + 8] == xo and l_cuadricula[i + 16] == xo and \
            l_cuadricula[i + 24] == xo:
                return True
        else:
            if l_cuadricula[i] == xo and l_cuadricula[i + 6] == xo and l_cuadricula[i + 12] == xo and \
            l_cuadricula[i + 18] == xo:
                return True

        contador += 1

    return False


def checkear_empate(vacia, lista_cuadricula):
    if vacia not in lista_cuadricula:
        return True

    return False


def dibuja_texto(surface, texto, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(texto, True, (200, 220, 30))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


