
import pygame
import sys
from pac1 import *
from pac2 import *
from pac3 import *

'''  VIDEO 13
Escalar pantalla
1 - Escalamos bloques Clase Laberinto
2 - Modificamos BSY de la clase game
3 - Escalamos los puntitos
4 - Escalamos los items, modificanto tyb al instanciarlos el el método new_game
    (tienen posición absoluta 475, 575)
    ----------

5 - Escalamnos los Pacmans, modificando tb el método check_reinstancia
    (tienen posición absoluta 475, 575)
Superar nivel
    
    '''
#====================================================
#                 Cod. Ppal MAIN
#====================================================

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        # colores
        self.AMARILLO = (220, 190, 0)
        self.BLANCO = (240, 240, 240)
        self.FONDO_GRIS = (73, 73, 73)
        self.ROJO = (230, 0, 0)
        self.VERDE_FONDO = (20, 240, 30)
        self.AZUL_C = (144, 205, 205)
        self.intro_presentacion = True # se activa nada mas empezar
        self.inicio = False # comienza tras la presentaión ( y antes del juego)
        self.inicio_ultimoUpdate = 0
        self.DURACION_MUSIC_INICIO = 4000 # milisegundos
        # banderas
        self.enJuego = False
        self.gameOver = True
        # bandera para reiniciar personajes
        self.reinstanciar_pacmanfantasmas = True # tras muerte se reinician
        self.kill_fantasmas = True
        self.nivel_superado = True
        # Para que el item nos dé puntos, 1º creamos una variable
        self.mostrarPuntosItem = 0
        # pausa entre niveles
        self.pausa_superado_tomartiempo = pygame.time.get_ticks()
        # tamaños de los bloques (personajes)
        BLOQUE_SIZE_X = 50
        # 2 - MODIFICAMOS  PARA EL ESCALADO EL RANGO Y
        BLOQUE_SIZE_Y = 40
        self.BSX = BLOQUE_SIZE_X
        self.BSY = BLOQUE_SIZE_Y
        self.NRO_FILAS = 21
        self.NRO_COLUMNAS = 19     
        # lista con los valores iniciales de los fantasmas
        self.lista_valoresFantasmas = [
            (275, 425, 0, 'le'), # x, y, fotograma, direccion
            (425, 425, 1, 'le'),
            (525, 425, 2, 'ri'),
            (675, 425, 3, 'ri')
        ]

        self.crear_laberinto = [
            9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,
            9,0,1,1,1,1,1,1,1,9,1,1,1,1,1,1,1,0,9,
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
            9,1,1,1,2,1,1,1,1,9,1,1,1,1,2,1,1,1,9,
            9,1,9,9,1,9,9,9,1,9,1,9,9,9,1,9,9,1,9,

            9,1,1,9,1,1,1,1,1,0,1,1,1,1,1,9,1,1,9,
            9,9,1,9,1,9,1,9,9,9,9,9,1,9,1,9,1,9,9,
            9,1,1,1,1,9,1,1,1,9,1,1,1,9,1,1,1,1,9,

            9,1,9,9,9,9,9,9,1,9,1,9,9,9,9,9,9,1,9,
            9,0,1,1,1,1,1,1,2,1,2,1,1,1,1,1,1,0,9,
            9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9
        ]

        self.cx = [0, 0, 0, 0, 0, 0, 0, 0] # 4 coordenadas y 4 direcciones
        self.cy = [0, 0, 0, 0, 0, 0, 0, 0]

        self.puntos = 0
        self.nivel = 1
        self.vidas = 3
        self.PAUSA_VIDAS = 2000
        self.RESOLUCION = (1120, 850)
        self.FPS = 60
        # sonidos
        self.sonido_wakawaka = pygame.mixer.Sound('sonido/pacmanwakawaka.ogg')
        self.sonido_sirena = pygame.mixer.Sound('sonido/pacmansirena.ogg')
        self.sonido_eatingCherry = pygame.mixer.Sound('sonido/pacmaneatingcherry.ogg')
        self.sonido_pacmanDies = pygame.mixer.Sound('sonido/pacmandies.ogg')
        self.sonido_wakawaka.set_volume(0.9)
        self.sonido_sirena.set_volume(0.2)
        self.sonido_gameover_retro = pygame.mixer.Sound('sonido/gameoveretro.ogg')
        self.sonido_fantasmas_azules = pygame.mixer.Sound('sonido/pacmanazules.ogg')
        self.sonido_eatingGhost = pygame.mixer.Sound('sonido/pacmaneatinghost.ogg')
        self.sonido_inicioNivel = pygame.mixer.Sound('sonido/pacmaninicionivel.ogg')
        pygame.mixer.music.load('sonido/pacmanintermision.ogg')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(loops=-1) # sonido en bucle

        self.pantalla = pygame.display.set_mode(self.RESOLUCION)
        pygame.display.set_caption('PacMan - Versión Imad Elias')
        self.reloj = pygame.time.Clock()

        self.lista_sprites_adibujar = pygame.sprite.Group()
        # grupo de un solo elemento (personaje)
        self.lista_pacman = pygame.sprite.Group()
        # lista con los bloques
        self.lista_laberinto = pygame.sprite.Group()
        # lista con puntitos
        self.lista_puntitos = pygame.sprite.Group()
        # lista con los items
        self.lista_items = pygame.sprite.Group()
        # lista con los fantasmas para la deteccion de colisiones
        self.lista_fantasmas = [0, 0, 0, 0]
        self.lista_fantasmas[0] = pygame.sprite.Group()
        self.lista_fantasmas[1] = pygame.sprite.Group()
        self.lista_fantasmas[2] = pygame.sprite.Group()
        self.lista_fantasmas[3] = pygame.sprite.Group()
        # lista general de los fantasmas
        self.lista_4fantasmas = pygame.sprite.Group()

        self.crear_pantalla()

    def crear_pantalla(self):
        contador = -1
        for y in range(self.NRO_FILAS):
            for x in range(self.NRO_COLUMNAS):
                contador += 1
                valor = self.crear_laberinto[contador]
                if valor == 9:
                    self.laberinto = Laberinto(self, x * self.BSX, y * self.BSY, valor)
                    self.lista_sprites_adibujar.add(self.laberinto)
                    self.lista_laberinto.add(self.laberinto)

                elif valor == 1:
                    self.puntitos = Puntitos(self, x * self.BSX + self.BSX // 2, y * self.BSY + self.BSY // 2, valor)
                    self.lista_sprites_adibujar.add(self.puntitos) # para que aparezca en pantalla
                    self.lista_puntitos.add(self.puntitos)


    def new_game(self):
        # presentacion
        self.intro_presentacion = False
        self.inicio = True
        self.inicio_ultimoUpdate = pygame.time.get_ticks()
        self.sonido_inicioNivel.play()

        self.puntos = 0
        self.nivel = 1
        self.vidas = 3
        # 4b - AJUSTAMOS LA POSICION DE LOS PUNTITOS
        self.items = Items(self, 9*self.BSX + self.BSX //2,
                           11 * self.BSY + self.BSY //2)
        self.lista_sprites_adibujar.add(self.items)
        self.lista_items.add(self.items)


    # Función para dibujar texto (Marcadores)
    def dibuja_texto(self, surface, texto, size, x, y, qcolor):
        font = pygame.font.SysFont('seriff', size)
        # si estamos en la intro, ponemos un fondo:
        if self.intro_presentacion or self.inicio:
            text_surface = font.render(texto, True, qcolor, (90, 90, 90))
        else:
            text_surface = font.render(texto, True, qcolor)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_surface, text_rect)

    # texto en pantalla
    def mostrar_marcadores(self):
        self.dibuja_texto(self.pantalla, f' Ptos: {str(self.puntos)}', self.BSX - 5,
                          self.BSX * self.NRO_COLUMNAS, self.BSY, self.BLANCO)

        self.dibuja_texto(self.pantalla, f' Nivel: {str(self.nivel)}', self.BSX - 5,
                          self.BSX * self.NRO_COLUMNAS, self.BSY * 3, self.BLANCO)
        
        # texto de GAME OVER
        if self.gameOver and not self.intro_presentacion:
            self.dibuja_texto(self.pantalla, ' GAME OVER ', 120 ,
                              self.RESOLUCION[0] // 7, self.RESOLUCION[1] // 2,
                              (230, 230, 0))

        if self.intro_presentacion:
            self.dibuja_texto(self.pantalla, 'Pac Clon', 280,
                              60, self.RESOLUCION[1] // 4, self.VERDE_FONDO)
        if self.inicio:
            self.dibuja_texto(self.pantalla, 'Preparado..', 90,
                              self.RESOLUCION[0] // 3.8, self.RESOLUCION[1] // 1.5, self.AMARILLO)

            
        # texto de los ITEMS
        if self.mostrarPuntosItem > 0:
            self.mostrarPuntosItem -= 1 # cuanta atrás
            self.dibuja_texto(self.pantalla, '100', 45, 450, 550, self.ROJO)

        
    def nivel_superado(self):
        pass

    def pausa_nivel_superado(self):
        pass


    # función que controla la colision con los fantasmas
    def check_colision_pacmanFantasmas(self):
        if not self.enJuego:
            return
        if self.pacman.check_colision_fantasmas():
            self.enJuego = False
            # Restamos una vida al morir
            self.vidas -= 1
            self.sonido_pacmanDies.play()
            self.pacmandies = PacManDies(self, self.pacman.rect.centerx,
                                         self.pacman.rect.centery)
            self.lista_sprites_adibujar.add(self.pacmandies)


    def update(self):
        calculo = pygame.time.get_ticks()
        if calculo -self.inicio_ultimoUpdate > self.DURACION_MUSIC_INICIO:
            self.inicio = False

        if not self.inicio: # ... si no es inicio, comienza el juego
            self.lista_sprites_adibujar.update()
            self.check_colision_pacmanFantasmas()
            self.check_reinstanciar()

        pygame.display.flip()
        self.reloj.tick(self.FPS)

    def draw(self):
        self.pantalla.fill(self.FONDO_GRIS)
        self.lista_sprites_adibujar.draw(self.pantalla)
        # marcadores
        self.mostrar_marcadores()

    # función que reinstancie los personajes si nos matan
    def check_reinstanciar(self):
        if not self.reinstanciar_pacmanfantasmas:
            return
        
        self.kill_fantasmas = False # para que no elimine fantasmas
        self.reinstanciar_pacmanfantasmas = False

        # Controlamos el GAME OVER
        if self.vidas < 0:
            self.gameOver = True
            self.enJuego = False
            # SONIDO DE FIN
            self.sonido_gameover_retro.play()
            return # NO SIGAS...

        # Movemos las instancias desde new_game
        # 5b - RECALCULAMOS LA POSICION ORIGINAL DE PACMAN
        self.pacman = PacMan(self, 9 * self.BSX + self.BSX // 2, 
                             4 * self.BSY + self.BSY // 2)
        self.lista_sprites_adibujar.add(self.pacman)
        self.lista_pacman.add(self.pacman)

        # instanacias de las vidas
        if self.vidas >= 1:
            for i in range(self.vidas):
                self.mostrarvidas = MostrarVidas(self, i + 1)
                self.lista_sprites_adibujar.add(self.mostrarvidas)
        

        # instanciamos los 4 fantasmas
        for i in range (4):
            datos = self.lista_valoresFantasmas[i]
            self.fantasma = Fantasma(self, datos[0], datos[1], datos[2] * 10 + 1, datos[3])
            self.lista_sprites_adibujar.add(self.fantasma)
            self.lista_fantasmas[i].add(self.fantasma)
            self.lista_4fantasmas.add(self.fantasma)
            # ... y sus ojos
            self.ojos = Ojos(self, datos[2])
            self.lista_sprites_adibujar.add(self.ojos)

        
    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and self.gameOver:
                if pygame.K_KP_ENTER:
                    # al empezar el juego, la música deja de sonar
                    pygame.mixer.music.stop()

                    self.gameOver = False
                    self.enJuego = True
                    self.new_game()
                    self.run()

            elif not self.gameOver:
                self.pacman.leer_teclado()

    def run(self):
        while not self.gameOver:
            self.check_event()
            self.update()
            self.draw()

        while self.gameOver:
            self.update()
            self.draw()
            self.check_event()



if __name__ == '__main__':
    game = Game() # instanaciamos el juego
    game.run()