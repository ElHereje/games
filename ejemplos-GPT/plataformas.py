import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ancho, alto = 800, 600
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Juego de Plataformas")

# Colores
blanco = (255, 255, 255)
verde = (0, 255, 0)

# Jugador
jugador_ancho, jugador_alto = 50, 50
jugador = pygame.Rect(300, alto - jugador_alto - 100, jugador_ancho, jugador_alto)
jugador_velocidad = 5
en_el_aire = True

# Plataforma
plataforma_ancho, plataforma_alto = 200, 20
plataforma = pygame.Rect(300, alto - plataforma_alto - 10, plataforma_ancho, plataforma_alto)

# Gravedad
gravedad = 1
velocidad_y = 0

# Función principal del juego
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Mover el jugador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jugador.left > 0:
        jugador.x -= jugador_velocidad
    if teclas[pygame.K_RIGHT] and jugador.right < ancho:
        jugador.x += jugador_velocidad
    if teclas[pygame.K_SPACE]:
        jugador.y -= jugador_velocidad + 2

    # Simular gravedad
    jugador.y += velocidad_y
    velocidad_y += gravedad

    # Verificar colisión con la plataforma
    if jugador.colliderect(plataforma) and velocidad_y > 0:
        jugador.y = plataforma.y - jugador_alto
        velocidad_y = 0
        en_el_aire = False
    else:
        en_el_aire = True

    # Limpiar la pantalla
    pantalla.fill(blanco)

    # Dibujar la plataforma
    pygame.draw.rect(pantalla, verde, plataforma)

    # Dibujar al jugador
    pygame.draw.rect(pantalla, verde, jugador)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del juego
    pygame.time.Clock().tick(60)
