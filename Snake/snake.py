import random

import pygame

NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
NARANJA = (255, 160, 60)
BLANCO = (255, 255, 255)
pygame.init()
tamanio = (500, 500)
pantalla = pygame.display.set_mode(tamanio)
reloj = pygame.time.Clock()

# creamos la comida
def food_spawn():
    food_pos = [random.randint(0, 49)*10, random.randint(0, 49)*10]
    return food_pos

def main():
    # 1 definimos la cabeza y el cuerpo
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    # el cuerpo será al principio 3 rectángulos de 10x10
    # 3 - establecemos la dirección
    direccion = "RIGHT"
    change = direccion
    # 10 posicionamos la comida en un bucle y creamos puntuación:
    food_pos = food_spawn()
    score = 0


    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # 4 - establecemos las funciones de las teclas
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    change = "RIGHT"
                if event.key == pygame.K_LEFT:
                    change = "LEFT"
                if event.key == pygame.K_UP:
                    change = "UP"
                if event.key == pygame.K_DOWN:
                    change = "DOWN"
        # 5 impedimos los retrocesos en la misma línea
        if change == "RIGHT" and direccion != "LEFT":
            direccion = "RIGHT"
        if change == "LEFT" and direccion != "RIGHT":
            direccion = "LEFT"
        if change == "UP" and direccion != "DOWN":
            direccion = "UP"
        if change == "DOWN" and direccion != "UP":
            direccion = "DOWN"

        # 6 Movimientos:
        if direccion == "RIGHT":
            snake_pos[0] += 10  # pos x
        if direccion == "LEFT":
            snake_pos[0] -= 10  # pos x
        if direccion == "DOWN":
            snake_pos[1] += 10  # pos y
        if direccion == "UP":
            snake_pos[1] -= 10  # pos y
        # 7 agregamos las nuevas coordenadas a la cabeza
        snake_body.insert(0, list(snake_pos))  # posición y lista
        # 12 para que agrande cuando coma, pausamos el pop durante 1 seg
        if snake_pos == food_pos:
            food_pos = food_spawn()  # generamos nueva comida
            score += 1  # aumentamos la puntuación
        else:
            snake_body.pop()
        # 8 quitamos la última posición
        # (11) snake_body.pop()

        pantalla.fill(NEGRO)
        # 2 - pintamos la serp.
        for pos in snake_body:
            pygame.draw.rect(pantalla, BLANCO, pygame.Rect(pos[0], pos[1], 10, 10))  # --> (x,y,alto,ancho)
        # 11 pintamos la comida
        pygame.draw.rect(pantalla, NARANJA, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # 13 para controlar salida de la pantalla
        if snake_pos[0] >= 500 or snake_pos[0] <= 0:
            print(f"GAME OVER !!! Puntuación : {score}")
            run = False
        if snake_pos[1] >= 500 or snake_pos[1] <= 0:
            print(f"GAME OVER !!! Puntuación : {score}")
            run = False
        # 14 para controlar choque con el cuerpo:
        if snake_pos in snake_body[1:]:  # excepto el primer lugar (la cabeza siempre toca el cuerpo...)
            print(f"GAME OVER !!! Puntuación : {score}")
            run = False

        pygame.display.set_caption(f"Snake. Puntuación :  {score}")
        pygame.display.flip()
        reloj.tick(10)


main()
pygame.quit()