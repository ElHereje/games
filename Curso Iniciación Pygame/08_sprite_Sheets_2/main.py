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
		pygame.mixer.init()

		self.rojo = (255, 0, 0)
		self.verde = (0, 255, 0)
		self.amarillo = (255, 255, 0)
		self.blanco = (255, 255, 255)
		self.negro = (0, 0, 0)
		self.fondoGRIS = (70, 70, 70)

		self.RESOLUCION = (800, 600)
		self.FPS = 60

		self.enJuego = True

		self.pantalla = pygame.display.set_mode(self.RESOLUCION)
		self.reloj = pygame.time.Clock()

		self.lista_spritesAdibujar = pygame.sprite.Group()
		self.instancias()




	def instancias(self):
		# creamos el personaje
		self.personaje = Personaje(self)
		# y lo añadimos a la lista de personajes
		self.lista_spritesAdibujar.add(self.personaje)


	def obtenerGrafico(self, nombrePng, escala):
		# cargamos la imagen
		img = pygame.image.load('../images/' + nombrePng).convert()
		# escalamos la imagen
		img2 = pygame.transform.scale(img, escala)
		# obtenemos el rect.
		rect = img2.get_rect()
		image_rect = (img2, rect)

		return image_rect # nos devuelve una imagen y un rectangulo



	def update(self):
		self.lista_spritesAdibujar.update()

		pygame.display.flip()
		self.reloj.tick(self.FPS)



	def draw(self):
		self.pantalla.fill(self.fondoGRIS)

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


			
