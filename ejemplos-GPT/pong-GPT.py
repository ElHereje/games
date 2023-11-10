import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ancho, alto = 800, 600
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Pong")

# Colores
blanco = (255, 255, 255)
negro = (0, 0, 0)

# Inicialización de variables
reloj = pygame.time.Clock()

# Jugador
jugador_ancho, jugador_alto = 15, 100
jugador1 = pygame.Rect(50, alto // 2 - jugador_alto // 2, jugador_ancho, jugador_alto)
jugador2 = pygame.Rect(ancho - 50 - jugador_ancho, alto // 2 - jugador_alto // 2, jugador_ancho, jugador_alto)
jugador_velocidad = 5

# Pelota
pelota_tamano = 20
pelota = pygame.Rect(ancho // 2 - pelota_tamano // 2, alto // 2 - pelota_tamano // 2, pelota_tamano, pelota_tamano)
pelota_velocidad = [5, 5]

# Función principal del juego
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Mover jugadores
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w] and jugador1.top > 0:
        jugador1.y -= jugador_velocidad
    if teclas[pygame.K_s] and jugador1.bottom < alto:
        jugador1.y += jugador_velocidad
    if teclas[pygame.K_UP] and jugador2.top > 0:
        jugador2.y -= jugador_velocidad
    if teclas[pygame.K_DOWN] and jugador2.bottom < alto:
        jugador2.y += jugador_velocidad

    # Mover la pelota
    pelota.x += pelota_velocidad[0]
    pelota.y += pelota_velocidad[1]

    # Rebotar en las paredes superior e inferior
    if pelota.top <= 0 or pelota.bottom >= alto:
        pelota_velocidad[1] = -pelota_velocidad[1]

    # Rebotar en los jugadores
    if pelota.colliderect(jugador1) or pelota.colliderect(jugador2):
        pelota_velocidad[0] = -pelota_velocidad[0]

    # Verificar si la pelota sale de la pantalla
    if pelota.left <= 0 or pelota.right >= ancho:
        # Puntuación
        if pelota.left <= 0:
            print("Puntuación Jugador 2!")
        else:
            print("Puntuación Jugador 1!")

        # Reposicionar la pelota al centro
        pelota.x = ancho // 2 - pelota_tamano // 2
        pelota.y = alto // 2 - pelota_tamano // 2

    # Limpiar la pantalla
    pantalla.fill(negro)

    # Dibujar jugadores y pelota
    pygame.draw.rect(pantalla, blanco, jugador1)
    pygame.draw.rect(pantalla, blanco, jugador2)
    pygame.draw.ellipse(pantalla, blanco, pelota)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del juego
    reloj.tick(60)
