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
'''
Ahora hacemos un scroll paralax, que es un scroll vertical con varias
capas de profundidad
'''
class Game:
	def __init__(self):
		pygame.init()

		self.rojo = (255, 0, 0)
		self.verde = (0, 255, 0)
		self.amarillo = (255, 255, 0)
		self.fondoGRIS = (70, 70, 70)

		self.RESOLUCION = (800, 600)
		self.FPS = 60

		# añadimos un array de scrolls
		self.arrayScrolls = []

		self.scrollY = 0

		self.pantalla = pygame.display.set_mode(self.RESOLUCION)
		self.reloj = pygame.time.Clock()

		self.fondoEstrellas = pygame.image.load('../images/fondo_estrellas_jon.png').convert()
		self.saturno = pygame.image.load('../images/saturno_moonpatrol.png').convert_alpha()

		self.lista_spritesAdibujar = pygame.sprite.Group()
		self.instancias()

		self.enJuego = True

		



	def instancias(self):
		self.avioneta = Avioneta(self)
		self.lista_spritesAdibujar.add(self.avioneta)

		# instanciamos los paralax
		# y los añadimos al array
		scroll1 = ScrollParalax(self, 0, 350, 1, '../images/moonpatrol1.png')
		self.arrayScrolls.append(scroll1)
		scroll2 = ScrollParalax(self, 0, 420, 2, '../images/moonpatrol2.png')
		self.arrayScrolls.append(scroll2)
		scroll3 = ScrollParalax(self, 0, 540, 3, '../images/moonpatrol3.png')
		self.arrayScrolls.append(scroll3)
		
	

	
	def instanciaDisparo(self):
		disparo = Disparo(self, self.avioneta.rect.right, self.avioneta.rect.centery)
		self.lista_spritesAdibujar.add(disparo)




	def update(self):
		self.lista_spritesAdibujar.update()

		pygame.display.flip()
		self.reloj.tick(self.FPS)



	def draw(self):
		self.pantalla.blit(self.fondoEstrellas, (0, 0))
		
		# añadimos los scroll creado
		for scroll in self.arrayScrolls:
			scroll.dibuja()



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


			