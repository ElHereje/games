# -----------------------------------------------------------------------------
#
# Space Invaders
# Language - Python
# Modules - pygame, sys, time
#
# Controls - <-- and --> Keys para mover, Space para disparar
#
#
# -----------------------------------------------------------------------------

import pygame
import sys
import time

# -------------- Iniciación ------------
pygame.init()

width = 700
height = 500

display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("Space Invaders")

ship_width = 40
ship_height = 30

# -------------- Colores -----------------
FONDO = (74, 35, 90)
BLANCO = (244, 246, 247)
AMARILLO = (241, 196, 15)
NARANJA = (186, 74, 0)
VERDE = (35, 155, 86)
BLANCO1 = (253, 254, 254)
GRIS_OSCURO = (23, 32, 42)


# -------------- Clase Nave --------------
class Nave:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w  # ancho
        self.h = h  # alto
        self.color = color

    def draw(self):
        pygame.draw.rect(display, AMARILLO, (self.x + self.w/2 - 8, self.y - 10, 16, 10))
        pygame.draw.rect(display, self.color, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(display, GRIS_OSCURO, (self.x + 5, self.y + 6, 10, self.h - 10))
        pygame.draw.rect(display, GRIS_OSCURO, (self.x + self.w - 15, self.y + 6, 10, self.h - 10))


# ----------------- Clase bala -------------
class Bala:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.d = 10
        self.speed = -5

    def draw(self):
        pygame.draw.ellipse(display, NARANJA, (self.x, self.y, self.d, self.d))

    def move(self):
        self.y += self.speed

    def hit(self, x, y, d):
        if x < self.x < x + d:
            if y + d > self.y > y:
                return True


# ------------------ Clase Alien ---------------
class Alien:
    def __init__(self, x, y, d):
        self.x = x
        self.y = y
        self.d = d
        self.x_dir = 1
        self.speed = 3

    def draw(self):
        pygame.draw.ellipse(display, VERDE, (self.x, self.y, self.d, self.d))
        pygame.draw.ellipse(display, GRIS_OSCURO, (self.x + 10, self.y + self.d/3, 8, 8), 2)
        pygame.draw.ellipse(display, GRIS_OSCURO, (self.x + self.d - 20, self.y + self.d/3, 8, 8), 2)
        pygame.draw.rect(display, GRIS_OSCURO, (self.x, self.y+self.d-20, 50, 7))

    def move(self):
        self.x += self.x_dir*self.speed

    def shift_down(self):
        self.y += self.d


# ------------------- Saved ------------------
def victoria():
    font = pygame.font.SysFont("Wide Latin", 22)
    font_large = pygame.font.SysFont("Wide Latin", 43)
    text2 = font_large.render("Felicidades...!", True, BLANCO1)
    text = font.render("Has evitado la invasión Alienígena ...!", True, BLANCO1)
    display.blit(text2, (60, height/2))
    display.blit(text, (45, height/2 + 100))
    pygame.display.update()
    time.sleep(3)


# -------------------- Death ----------------
def GameOver():
    font = pygame.font.SysFont("Chiller", 50)
    font_large = pygame.font.SysFont("Chiller", 100)
    text2 = font_large.render("Game Over!", True, BLANCO1)
    text = font.render("no has podido prevenir la invasión...!", True, BLANCO1)
    display.blit(text2, (180, height/2-50))
    display.blit(text, (45, height/2 + 100))


# --------------------- The Game ------------------
def game():
    invasion = False
    aliado = Nave(width/2-ship_width/2, height-ship_height - 10, ship_width, ship_height, BLANCO)
    balas = []
    num_bala = 0

    for i in range(num_bala):
        i = Bala(width/2 - 5, height - ship_height - 20)
        balas.append(i)

    x_move = 0
    aliens = []
    num_aliens = 8
    d = 50

    for i in range(num_aliens):
        i = Alien((i+1)*d + i*20, d+20, d)
        aliens.append(i)

    while not invasion:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RIGHT:
                    x_move = 5
                if event.key == pygame.K_LEFT:
                    x_move = -5
                if event.key == pygame.K_SPACE:
                    num_bala += 1
                    i = Bala(aliado.x + ship_width/2 - 5, aliado.y)
                    balas.append(i)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    x_move = 0
                if event.key == pygame.K_LEFT:
                    x_move = 0

        display.fill(FONDO)

        for i in range(num_bala):
            balas[i].draw()
            balas[i].move()

        for alien in list(aliens):
            alien.draw()
            alien.move()
            for item in list(balas):
                if item.hit(alien.x, alien.y, alien.d):
                    balas.remove(item)
                    num_bala -= 1
                    aliens.remove(alien)
                    num_aliens -= 1

        if num_aliens == 0:
            victoria()
            invasion = True

        for i in range(num_aliens):
            if aliens[i].x + d >= width:
                for j in range(num_aliens):
                    aliens[j].x_dir = -1
                    aliens[j].shift_down()

            if aliens[i].x <= 0:
                for j in range(num_aliens):
                    aliens[j].x_dir = 1
                    aliens[j].shift_down()

        try:
            if aliens[0].y + d > height:
                GameOver()
                pygame.display.update()
                time.sleep(3)
                invasion = True
        except Exception as e:
            pass

        aliado.x += x_move

        if aliado.x < 0:
            aliado.x -= x_move
        if aliado.x + ship_width > width:
            aliado.x -= x_move

        aliado.draw()

        pygame.display.update()
        clock.tick(60)

# ----------------- Calling the Game Function ---------------------
game()
