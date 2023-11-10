import pygame
import sys
import math

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ancho, alto = 800, 600
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Juego tipo Angry Birds")

# Colores
blanco = (255, 255, 255)
verde = (0, 255, 0)
rojo = (255, 0, 0)

# Gravedad
gravedad = 0.5

# Pájaro
pajaro_radio = 20
pajaro = pygame.Rect(100, alto - pajaro_radio - 10, pajaro_radio * 2, pajaro_radio * 2)
pajaro_color = verde
pajaro_en_vuelo = False
pajaro_velocidad = [0, 0]

# Objetivo
objetivo_radio = 30
objetivo = pygame.Rect(ancho - 100 - objetivo_radio, alto - objetivo_radio - 10, objetivo_radio * 2, objetivo_radio * 2)
objetivo_color = rojo

# Función principal del juego
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN and not pajaro_en_vuelo:
            # Iniciar el lanzamiento del pájaro al hacer clic
            pajaro_en_vuelo = True
            pos_mouse = pygame.mouse.get_pos()
            pajaro_velocidad = [(pos_mouse[0] - pajaro.centerx) / 10, (pos_mouse[1] - pajaro.centery) / 10]

    if pajaro_en_vuelo:
        # Mover el pájaro en vuelo
        pajaro.x += pajaro_velocidad[0]
        pajaro.y += pajaro_velocidad[1]
        pajaro_velocidad[1] += gravedad

        # Verificar colisión con el suelo
        if pajaro.bottom >= alto - 10:
            pajaro_en_vuelo = False
            pajaro.y = alto - pajaro_radio - 10

        # Verificar colisión con el objetivo
        if pajaro.colliderect(objetivo):
            print("¡Objetivo alcanzado!")
            pajaro_en_vuelo = False
            pajaro.x = 100
            pajaro.y = alto - pajaro_radio - 10
            pajaro_velocidad = [0, 0]  

    # Limpiar la pantalla
    pantalla.fill(blanco)

    # Dibujar el objetivo
    pygame.draw.circle(pantalla, objetivo_color, objetivo.center, objetivo_radio)

    # Dibujar el pájaro
    pygame.draw.circle(pantalla, pajaro_color, pajaro.center, pajaro_radio)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del juego
    pygame.time.Clock().tick(60)
