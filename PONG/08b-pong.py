import pygame, sys
pygame.init()

# colores
black = (0, 0, 0)
white = (255, 255, 255)

# tamaño de ventana y origen de fondo
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
fondo = pygame.image.load("images/CASCADA.png")
sonido_pala = pygame.mixer.Sound("sound/ice.wav")
rebote = pygame.mixer.Sound("sound/boing.wav")
out = pygame.mixer.Sound("sound/ouch.wav")
musica = pygame.mixer.Sound("sound/mountain2.wav")

# reloj
clock = pygame.time.Clock()

# valores de las paletas
player_width = 15
player_height = 90

# coord y vel del jug 1
player1_x_coord = 50
player1_y_coord = 255
player1_y_speed = 0

# coord y vel del jug 2
player2_x_coord = 725
player2_y_coord = 255
player2_y_speed = 0

# coord de la pelota
pelota_x = 400
pelota_y = 300
pelota_speed_x = 3
pelota_speed_y = 3

# ponemos la música
musica.set_volume(50)
musica.play(-1)

# variable para salir
game_over = False

# bucle principal
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        # 3 - controlamos los movimientos
        if event.type == pygame.KEYDOWN:
            # Jug1
            if event.key == pygame.K_w:
                player1_y_speed = -3
            if event.key == pygame.K_s:
                player1_y_speed = 3
            # Jug2
            if event.key == pygame.K_UP:
                player2_y_speed = -3
            if event.key == pygame.K_DOWN:
                player2_y_speed = 3
        if event.type == pygame.KEYUP:
            # Jug1
            if event.key == pygame.K_w:
                player1_y_speed = 0
            if event.key == pygame.K_s:
                player1_y_speed = 0
            # Jug2
            if event.key == pygame.K_UP:
                player2_y_speed = 0
            if event.key == pygame.K_DOWN:
                player2_y_speed = 0

    # para que rebote la pelota
    if pelota_y > 590 or pelota_y < 10:
        rebote.play(0)
        pelota_speed_y *= -1
    # si sale del lado derecho
    if pelota_x > 800:
        out.play(0)
        pelota_x = 400
        pelota_y = 300
        # si se sale de la pantalla, invierte dirección
        pelota_speed_x *= -1
        pelota_speed_y *= -1
    # si sale del lado izquierdo
    if pelota_x < 0:
        out.play(0)
        pelota_x = 400
        pelota_y = 300
        # si se sale de la pantalla, invierte dirección
        pelota_speed_x *= -1
        pelota_speed_y *= -1

    # 4 modificamos coord. para dar movimientos y controlar los límites de las palas
    player1_y_coord += player1_y_speed
    if player1_y_coord <= 0:
        player1_y_coord = 0
    if player1_y_coord >= 510:
        player1_y_coord = 510
    player2_y_coord += player2_y_speed
    if player2_y_coord <= 0:
        player2_y_coord = 0
    if player2_y_coord > 510:
        player2_y_coord = 510
    # 5 movimiento pelota
    pelota_x += pelota_speed_x
    pelota_y += pelota_speed_y

    # 1 damos color de fondo, dibujamos la ventana y los FPS (fill, flip y clock)
    # screen.fill(black)
    screen.blit(fondo, (0, 0))
    # ZONA DE DIBUJO
    # 2 creamos los jugadores (paletas) y la pelota
    jug1 = pygame.draw.rect(screen, white, (player1_x_coord,
                                            player1_y_coord,
                                            player_width,
                                            player_height )) # paleta izq.
    jug2 = pygame.draw.rect(screen, white, (player2_x_coord,
                                            player2_y_coord,
                                            player_width,
                                            player_height))  # paleta dcha.
    pelota = pygame.draw.circle(screen,
                                white,
                                (pelota_x, pelota_y),
                                10)

    # 6 para detectar colisiones
    if pelota.colliderect(jug1) or pelota.colliderect(jug2):
        sonido_pala.play(0)
        pelota_speed_x *= -1  # invertimos la dirección

    pygame.display.flip()
    clock.tick(100)

pygame.quit()
