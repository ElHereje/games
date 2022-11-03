import sys, pygame

pygame.init()

PANTALLA = pygame.display.set_mode((800, 600))
pygame.display.set_caption("SpaceInvader")

BLANCO = (255, 255, 255)

PANTALLA.fill(BLANCO)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    PANTALLA.fill(BLANCO)
    pygame.display.update()

