import pygame
import random
import sys
from pac1 import *
from pac2 import *
from pac3 import *



#=====================================================================================
#---                       Codigo Principal ( M A I N )                            ---
#-------------------------------------------------------------------------------------
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.AMARILLO = (220, 190, 0)
        self.BLANCO = (240, 240, 240)
        self.GRIS_FONDO = (73, 73, 73)
        self.ROJO = (230, 30, 20)
        self.VERDE_FONDO = (20, 240, 30)
        self.AZUL_C = (144, 205, 205)
        self.intro_presentacion = True
        self.inicio = False
        self.inicio_ultimoUpdate = 0
        self.DURACION_MUSIC_INICIO = 4000
        self.gameover = True
        self.enjuego = False
        self.reinstanciar_pacmanfantasmas = True
        self.kill_fantasmas = False
        self.nivel_superado = False
        self.mostrarPtosItem = 0
        self.pausa_superado_tomartiempo = 0 
        self.salir_otro_item = 0
        BLOQUE_SIZE_X = 50
        BLOQUE_SIZE_y = 50
        self.BSX = BLOQUE_SIZE_X
        self.BSY = BLOQUE_SIZE_y
        self.NRO_FILAS = 15 # 21 FILAS ORIGINAL
        self.NRO_COLUMNAS = 19
        self.lista_valoresFantasmas = [
            (5, 8, 0, 'le'), (8, 8, 1, 'le'), 
            (10, 8, 2, 'ri'), (13, 8, 3, 'ri')
        ]
        # ******************************************
        # ARRAY ORIGINAL ***************************
        # ******************************************
        self.crear_laberinto2 = [
            9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,
            9,5,1,1,1,1,1,1,1,9,1,1,1,1,1,1,1,5,9,
            9,1,9,9,1,9,9,9,1,9,1,9,9,9,1,9,9,1,9,

            9,1,9,9,1,9,9,9,1,9,1,9,9,9,1,9,9,1,9,
            9,1,1,1,2,1,1,1,1,0,1,1,1,1,2,1,1,1,9,
            9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,

            9,1,1,1,1,9,1,1,1,9,1,1,1,1,1,1,1,1,9,
            9,9,9,9,1,9,9,9,1,9,1,9,9,9,1,9,9,9,9,
            9,1,1,1,2,1,1,1,1,1,1,1,1,1,2,1,1,1,9,

            9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,
            9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,
            9,1,1,1,1,9,1,1,1,0,1,1,1,9,1,1,1,1,9,

            9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,
            9,5,1,1,2,1,1,1,1,9,1,1,1,1,2,1,1,5,9,
            9,1,9,9,1,9,9,9,1,9,1,9,9,9,1,9,9,1,9,

            9,1,1,9,1,1,1,1,1,0,1,1,1,1,1,9,1,1,9,
            9,9,1,9,1,9,1,9,9,9,9,9,1,9,1,9,1,9,9,
            9,1,1,1,1,9,1,1,1,9,1,1,1,9,1,1,1,1,9,

            9,1,9,9,9,9,9,9,1,9,1,9,9,9,9,9,9,1,9,
            9,0,1,1,1,1,1,1,2,1,2,1,1,1,1,1,1,0,9,
            9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9
        ]

        # ********************************************
        #  ARRAY Modificado! *************************
        # ********************************************
        self.crear_laberinto = [
            9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,
            9,5,1,1,1,1,1,1,1,9,1,1,1,1,1,1,1,5,9,
            9,1,9,9,1,9,9,9,1,9,1,9,9,9,1,9,9,1,9,

            9,1,9,9,1,9,9,9,1,9,1,9,9,9,1,9,9,1,9,
            9,1,1,1,2,1,1,1,1,0,1,1,1,1,2,1,1,1,9,
            9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,

            9,1,1,1,1,9,1,1,1,9,1,1,1,1,1,1,1,1,9,
            9,9,9,9,1,9,9,9,1,9,1,9,9,9,1,9,9,9,9,
            9,1,1,1,2,1,1,1,1,1,1,1,1,1,2,1,1,1,9,

            9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,
            9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,
            0,1,1,1,1,9,1,1,1,0,1,1,1,9,1,1,1,1,0,

            9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,
            9,5,1,1,2,1,1,1,1,0,1,1,1,1,2,1,1,5,9,
            9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,

            9,0,0,9,0,0,0,0,0,0,0,0,0,0,0,9,0,0,9,
            9,9,0,9,0,9,0,9,9,9,9,9,0,9,0,9,0,9,9,
            9,0,0,0,0,9,0,0,0,9,0,0,0,9,0,0,0,0,9,

            9,0,9,9,9,9,9,9,0,9,0,9,9,9,9,9,9,0,9,
            9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,
            9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9
        ]
        self.cx = [0, 0, 0, 0, 0, 0, 0, 0]
        self.cy = [0, 0, 0, 0, 0, 0, 0, 0]
        self.puntos = 0
        self.nivel = 1
        self.vidas = 3
        self.countDownAzules = 0
        self.duracionAzules = 1000
        self.sumaPtosComeFantasmas = 0  # 200 -> 400 -> 800 -> 1600
        self.mostrar_ptosComeFantasmas = [0, 0, 0, 0]
        self.coordXY_mostrarPtosCF = [(0, 0), (0, 0), (0, 0), (0, 0)]
        self.PAUSA_VIDAS = 2000
        self.RESOLUCION = (self.BSX * self.NRO_COLUMNAS + 200, self.BSY * self.NRO_FILAS)
        self.FPS = 60
        self.sonido_wakawaka = pygame.mixer.Sound("sonido/pacmanwakawaka.ogg")
        self.sonido_wakawaka.set_volume(0.9)
        self.sonido_sirena = pygame.mixer.Sound("sonido/pacmansirena.ogg")
        self.sonido_sirena.set_volume(0.2)
        self.sonido_eatingCherry = pygame.mixer.Sound("sonido/pacmaneatingcherry.ogg")
        self.sonido_pacmanDies = pygame.mixer.Sound("sonido/pacmandies.ogg")
        self.sonido_gameover_retro = pygame.mixer.Sound("sonido/gameoveretro.ogg")
        self.sonido_fantasmas_azules = pygame.mixer.Sound("sonido/pacmanazules.ogg")
        self.sonido_eatingGhost = pygame.mixer.Sound("sonido/pacmaneatinghost.ogg")
        self.sonido_inicioNivel = pygame.mixer.Sound("sonido/pacmaninicionivel.ogg")
        pygame.mixer.music.load("sonido/pacmanintermision.ogg")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=-1)
        self.pantalla = pygame.display.set_mode(self.RESOLUCION)
        #pygame.display.set_caption("PacJon by Juan Eguia")
        self.reloj = pygame.time.Clock()

        self.lista_sprites_adibujar = pygame.sprite.Group()
        self.lista_pacman = pygame.sprite.Group()
        self.lista_laberinto = pygame.sprite.Group()
        self.lista_puntitos = pygame.sprite.Group()
        self.lista_puntosGordos = pygame.sprite.Group()
        self.lista_items = pygame.sprite.Group()
        self.lista_fantasmas = [0, 0, 0, 0]
        self.lista_fantasmas[0] = pygame.sprite.Group()
        self.lista_fantasmas[1] = pygame.sprite.Group()
        self.lista_fantasmas[2] = pygame.sprite.Group()
        self.lista_fantasmas[3] = pygame.sprite.Group()
        self.lista_los4fantasmas = pygame.sprite.Group()
        self.lista_ojosSinFantasma = [0, 0, 0, 0]
        self.lista_ojosSinFantasma[0] = pygame.sprite.Group()
        self.lista_ojosSinFantasma[1] = pygame.sprite.Group()
        self.lista_ojosSinFantasma[2] = pygame.sprite.Group()
        self.lista_ojosSinFantasma[3] = pygame.sprite.Group()
        self.crear_pantalla()



    def crear_pantalla(self):
        contador = -1
        for y in range(self.NRO_FILAS):
            for x in range(self.NRO_COLUMNAS):
                contador += 1
                valor = self.crear_laberinto[contador]
                if valor == 9 and self.nivel == 1:
                    self.laberinto = Laberinto(self, x * self.BSX, y * self.BSY, valor)
                    self.lista_sprites_adibujar.add(self.laberinto)
                    self.lista_laberinto.add(self.laberinto)
                elif valor == 1:
                    self.puntitos = Puntitos(self, x * self.BSX + self.BSX // 2, 
                        y * self.BSY + self.BSY // 2, valor)
                    self.lista_sprites_adibujar.add(self.puntitos)
                    self.lista_puntitos.add(self.puntitos)
                elif valor == 5:
                    self.puntosgordos = PuntosGordos(self, x * self.BSX + self.BSX // 2,
                        y * self.BSY + self.BSY // 2)
                    self.lista_sprites_adibujar.add(self.puntosgordos)
                    self.lista_puntosGordos.add(self.puntosgordos)



    def new_game(self):
        self.intro_presentacion = False
        self.inicio = True
        self.inicio_ultimoUpdate = pygame.time.get_ticks()
        self.sonido_inicioNivel.play()

        self.puntos = 0
        self.nivel = 1
        self.vidas = 3



    def dibuja_texto(self, surface, texto, size, x, y, qcolor):
        font = pygame.font.SysFont("serif", size)

        if self.intro_presentacion or self.inicio:
            text_surface = font.render(texto, True, qcolor, (90, 90, 90))
        else:
            text_surface = font.render(texto, True, qcolor)

        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_surface, text_rect)


    def mostrar_marcadores(self):
        self.dibuja_texto(self.pantalla, f' Ptos: {str(self.puntos)}', 45, 
            self.BSX * self.NRO_COLUMNAS, self.BSY, self.BLANCO)

        self.dibuja_texto(self.pantalla, f' Nivel: {str(self.nivel)}', 45,
            self.BSX * self.NRO_COLUMNAS, self.BSY * 3, self.BLANCO)

        if self.gameover and not self.intro_presentacion:
            self.dibuja_texto(self.pantalla, ' Game Over ', 120,
                self.RESOLUCION[0] // 7, self.RESOLUCION[1] // 2, (230, 230, 0))

        if self.intro_presentacion:
            self.dibuja_texto(self.pantalla, ' Pac Clon ', 200,
                60, self.RESOLUCION[1] // 4, self.VERDE_FONDO)

        if self.inicio:
            self.dibuja_texto(self.pantalla, ' Preparado... ', 60,
                self.RESOLUCION[0] // 3.8, self.RESOLUCION[1] // 1.5, self.AMARILLO)

        if self.mostrarPtosItem > 0:
            self.mostrarPtosItem -= 1
            self.dibuja_texto(self.pantalla, str(self.item.sumaPtos), int(self.BSY / 1.11),
                self.BSX * 9, self.BSY * 11, self.VERDE_FONDO)

        for i in range(4):
            if self.mostrar_ptosComeFantasmas[i] > 0:
                if self.mostrar_ptosComeFantasmas[i] == 99:
                    pygame.time.delay(500)

                self.mostrar_ptosComeFantasmas[i] -= 1
                self.dibuja_texto(self.pantalla, str(self.sumaPtosComeFantasmas), int(self.BSY / 1.11),
                    self.coordXY_mostrarPtosCF[i][0], self.coordXY_mostrarPtosCF[i][1], self.VERDE_FONDO)

        if self.nivel_superado:
            self.dibuja_texto(self.pantalla, ' Nivel Superado!', 120,
                self.RESOLUCION[0] // 9, self.RESOLUCION[1] // 3, self.AMARILLO)



    def check_nivelsuperado(self):
        if len(self.lista_puntitos) <= 0 and len(self.lista_puntosGordos) <= 0:
            self.duracionAzules -= 200
            if self.duracionAzules < 400:
                self.duracionAzules = 400 

            self.nivel += 1
            self.countDownAzules = 0
            self.nivel_superado = True
            self.kill_fantasmas = True
            self.pacman.kill()
            if len(self.lista_items) > 0:
                self.item.kill()

            self.pausa_superado_tomartiempo = pygame.time.get_ticks()
            pygame.mixer.music.play()
            print('nivel Superado!!')



    def instanciar_item(self):
        if self.salir_otro_item != 0:
            self.sonido_eatingCherry.play()

        self.item = Items(self, 9 * self.BSX + self.BSX // 2, 
            11 * self.BSY + self.BSY // 2)
        self.lista_sprites_adibujar.add(self.item)
        self.lista_items.add(self.item)



    def instanciar_fantasma(self, i):
        datos = self.lista_valoresFantasmas[i]
        coorX = datos[0] * self.BSX + self.BSX // 2
        coorY = datos[1] * self.BSY + self.BSY // 2
        self.fantasma = Fantasma(self, coorX, coorY, datos[2] * 10 + 1, datos[3])
        self.lista_sprites_adibujar.add(self.fantasma)
        self.lista_fantasmas[i].add(self.fantasma)
        self.lista_los4fantasmas.add(self.fantasma)

        self.ojos = Ojos(self, datos[2])
        self.lista_sprites_adibujar.add(self.ojos)


    def instanciar_ojosSinFantasma(self, centerx, centery, tipoFantasma, direccion):
        self.ojossinfantasma = OjosSinFantasma(self, centerx, centery, tipoFantasma, direccion)
        self.lista_sprites_adibujar.add(self.ojossinfantasma)
        self.lista_ojosSinFantasma[tipoFantasma].add(self.ojossinfantasma)



    def check_colision_pacmanFantasmas(self):
        if not self.enjuego:
            return

        if self.pacman.check_colision_fantasmas():
            if self.countDownAzules <= 0:
                self.enjuego = False
                self.vidas -= 1
                print('Colision Vida -')
                self.sonido_pacmanDies.play()
                self.pacmandies = PacManDies(self, self.pacman.rect.centerx, self.pacman.rect.centery)
                self.lista_sprites_adibujar.add(self.pacmandies)



    def update(self):
        pygame.display.set_caption(str(int(self.reloj.get_fps())))

        calculo = pygame.time.get_ticks()
        if calculo - self.inicio_ultimoUpdate > self.DURACION_MUSIC_INICIO:
            self.inicio = False

        if len(self.lista_puntitos) == 0 and len(self.lista_puntosGordos) == 0 and calculo - self.pausa_superado_tomartiempo > 7500:
            self.nivel_superado = False
            self.reinstanciar_pacmanfantasmas = True 
            self.crear_pantalla()


        if not self.inicio and not self.nivel_superado:
            if self.countDownAzules > 0:
                self.countDownAzules -= 1

            self.lista_sprites_adibujar.update()
            self.check_nivelsuperado()
            self.check_colision_pacmanFantasmas()
            self.check_reinstanciar()

            for i in range(4):
                if self.countDownAzules <= 0 and len(self.lista_fantasmas[i]) == 0:
                    self.instanciar_fantasma(i)


            if calculo - self.salir_otro_item > 9999 and len(self.lista_items) == 0:
                self.instanciar_item()

        pygame.display.flip()
        self.reloj.tick(self.FPS)

    
    def draw(self):
        self.pantalla.fill(self.GRIS_FONDO)
        self.lista_sprites_adibujar.draw(self.pantalla)
        pygame.draw.rect(self.pantalla, self.GRIS_FONDO, (self.BSX * self.NRO_COLUMNAS,
            self.BSY * 11, self.BSX, self.BSY))
        self.mostrar_marcadores()



    def check_reinstanciar(self):
        if not self.reinstanciar_pacmanfantasmas:
            return

        self.kill_fantasmas = False
        self.reinstanciar_pacmanfantasmas = False

        if self.vidas < 0:
            self.gameover = True
            self.enjuego = False
            self.sonido_gameover_retro.play()
            return

        self.pacman = PacMan(self, 9 * self.BSX + self.BSX // 2, 
            4 * self.BSY + self.BSY // 2)
        self.lista_sprites_adibujar.add(self.pacman)
        self.lista_pacman.add(self.pacman)

        if self.vidas >= 1:
            for i in range(self.vidas):
                self.mostrarvidas = MostrarVidas(self, i + 1)
                self.lista_sprites_adibujar.add(self.mostrarvidas)

        for i in range(4):
            self.instanciar_fantasma(i)

        self.instanciar_item()


    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN and self.gameover:
                if pygame.K_KP_ENTER:
                    pygame.mixer.music.stop()
                    self.gameover = False
                    self.enjuego = True
                    self.new_game()
                    self.run()

            elif not self.gameover:
                pass
                #self.pacman.leer_teclado()



    def run(self):
        while not self.gameover:
            self.check_event()
            self.update()
            self.draw()

        while self.gameover:
            self.update()
            self.draw()
            self.check_event()


if __name__ == '__main__':
    game = Game()
    game.run()
