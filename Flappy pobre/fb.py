import random

import pygame

pygame.init()

alto = 700
ancho = 500
ventana = pygame.display.set_mode((ancho, alto))
background_image = pygame.image.load("back.png").convert()
bird_image = pygame.image.load("bird.png").convert_alpha()
top_pipe = pygame.image.load("pipe_top.png").convert_alpha()
bot_pipe = pygame.image.load("pipe_bot.png").convert_alpha()
reloj = pygame.time.Clock()

# 8 funcion que define la altura de las tuberías
def pipe_random_height():
    pipe_h = [random.randint(200, (alto/2)-20), random.randint((alto/2)+20, alto-200)]
    return pipe_h

def main():
    # 1 coor de inicio
    player_pos = [100, 300]
    # 3 establecemos la gravedad, velocidad, salto y puntuación
    gravedad = 1
    vel = 0
    salto = -20
    score = 0

    # 7 creamos las tuberías
    pipe_pos = 700
    pipe_widht = 50 #(ancho)
    pipe_height = pipe_random_height() # función que definimos ahora... en 8

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # 6 establecemos los saltos
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    vel += salto

        # 4 creamos la grav y vel
        vel += gravedad
        vel *= 0.95 # limita la aceleración de la gravedad
        player_pos[1] += vel

        # 10 movimiento de las tuberías hacia la izq.
        if pipe_pos >= -20:
            pipe_pos -= 5
        else:
            pipe_pos = 700
            pipe_height = pipe_random_height()
            score += 1

        # 2 - dibujamos el fondo, player y las tuberías
        ventana.blit(background_image, [0, 0])# comiena a dibujar en el 0,0
        ventana.blit(top_pipe, (pipe_pos, -pipe_height[0]))
        ventana.blit(bot_pipe, (pipe_pos, pipe_height[1]))
        ventana.blit(bird_image, (int(player_pos[0]), int(player_pos[1])))

        # 9 dibujamos las tuberias
       # pygame.draw.rect(ventana, GRIS, [pipe_pos, 0, pipe_widht, pipe_height[0]], 0) # la de arriba
       # pygame.draw.rect(ventana, GRIS, [pipe_pos, pipe_height[1], pipe_widht, 500], 0) # la de abajo
        # se pone 500 porque no se la altura del hueco y hago que salga por debajo de la pantalla

        # 11 - programamos los choques con las tuberías
        if player_pos[1] <= (-pipe_height[0] + 500) or player_pos[1] >= pipe_height[1]:
            if player_pos[0] in list(range(pipe_pos, pipe_pos + pipe_widht)):
                print(f"Game Over. Score: {score}")

        # 5 creamos los bordes
        if player_pos[1] >= alto:
            player_pos[1] = alto
            vel = 0
        elif player_pos[1] <= 0:
            player_pos[1] = 0
            vel = 0

        pygame.display.flip()
        reloj.tick(25)

main()
pygame.quit()