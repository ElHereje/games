import pygame
import sys

# iniciamos pygame
pygame.init()

# VARIABLES
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
NEGRO = (0, 0, 0)

resolucion = (800, 600)
FPS = 60
pi = 3.1416

# creamos la pantalla y el reloj
pantalla = pygame.display.set_mode(resolucion)
reloj = pygame.time.Clock()

# variables para movimiento
x = 0
y = 0

radianIni = 0.8 # boca abierta
radianFin = 5.5

# vandera de control del juego
enJuego = True

# bucle ppal
while enJuego:
    # detector de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            enJuego = False

    # ZONA DE UPDATES ----------------------------------------------------------

    x += 1
    y += 1
    # animacion
    
    radianIni -= 0.05
    radianFin += 0.05
    if radianIni <= 0:
        radianIni = 0.8
        radianFin = 5.5
    
    
    # ZONA DE DIBUJO -----------------------------------------------------------

    # Borado para refresco
    pantalla.fill(NEGRO)
    # rectangulo = pygame.draw.rect(donde, color, (pos1_x, pos1_y, largo, alto ))
    # rectangulo = pygame.draw.rect(pantalla, ROJO, (x, y, 100, 100 ))
    # circulo = pygame.draw.circle(donde, color, (centro, radio))
    # circulo = pygame.draw.circle(pantalla, VERDE, (400, 300), 100)
    # arco = pygame.draw.arc(donde, color, (rectangulo), angulo_1, angulo_2, grosor)
    # arco = pygame.draw.arc(pantalla, AZUL, (300, 100, 100, 100), 0, pi, 10)
    pacman = pygame.draw.arc(pantalla, AMARILLO, (x, 200, 100, 100), radianIni, radianFin, 50)

    pygame.display.flip() # refresco de pantalla
    reloj.tick(FPS)

pygame.quit()
sys.exit()