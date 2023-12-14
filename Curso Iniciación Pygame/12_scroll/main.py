import pygame
import sys

from prg2 import *


# ----------------------------------------------------------------
# Codigo Principal (main.py) ... Aqui se aloja la clase Game
# 
# Funciones:
# 			instancias()
#			buclePrincipal()
#							update()
#							draw()
#							check_event()			
# ----------------------------------------------------------------
class Game:
	def __init__(self):
		pygame.init()

		self.rojo = (255, 0, 0)
		self.verde = (0, 255, 0)
		self.amarillo = (255, 255, 0)
		self.fondoGRIS = (70, 70, 70)

		self.RESOLUCION = (800, 600)
		self.FPS = 60

		# 3 - Nueva variable para controlar el scroll vertical
		self.scrollY = 0

		self.pantalla = pygame.display.set_mode(self.RESOLUCION)
		self.reloj = pygame.time.Clock()

		self.fondoEstrellas = pygame.image.load('../images/fondo_estrellas_jon.png').convert()
		self.saturno = pygame.image.load('../images/saturno_moonpatrol.png').convert_alpha()

		self.lista_spritesAdibujar = pygame.sprite.Group()
		self.instancias()

		self.enJuego = True



	def instancias(self):
		self.nave = Nave(self)
		self.lista_spritesAdibujar.add(self.nave)


	# 2 - creamos la clase mencionada:
	def scrollEspacial(self):
		self.scrollY += 1

		if self.scrollY >= self.RESOLUCION[1]:
			self.scrollY = 0

		# ahora pintamos
		self.pantalla.blit(self.fondoEstrellas, (0, self.scrollY))
		# para repetier el fondo
		self.pantalla.blit(self.fondoEstrellas, (0, self.scrollY - self.RESOLUCION[1]))



	def update(self):
		self.lista_spritesAdibujar.update()

		pygame.display.flip()
		self.reloj.tick(self.FPS)



	def draw(self):
		# 1 - llamamos a la función (aún no creada) scrollEspacial
		self.scrollEspacial()

		self.lista_spritesAdibujar.draw(self.pantalla) 



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



if __name__ == '__main__':
    game = Game()
    game.buclePrincipal()


			