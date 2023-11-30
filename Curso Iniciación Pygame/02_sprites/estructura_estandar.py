import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()

        self.ROJO = (255, 0, 0)   
        self.VERDE = (0, 255, 0)
        self.AMARILLO = (255, 255, 0)
        self.NEGRO = (0, 0, 0)
        self.fondoGRIS = (70, 70, 70)

        self.RESOLUCION = (800, 600)
        self.FPS = 60 

        self.enJuego = True

        self.pantalla = pygame.display.set_mode(self.RESOLUCION)
        self.reloj = pygame.time.Clock()

    def update(self):
        pygame.display.flip()
        self.reloj.tick(self.FPS)

    def draw(self):
        self.pantalla.fill((self.fondoGRIS))

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def buclePrincipal(self):
        while self.enJuego:
            self.check_event()
            self.update()
            self.draw()

# instanciacion de la clase
if __name__ == '__main__':
    game = Game()
    game.buclePrincipal()