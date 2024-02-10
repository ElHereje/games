import pygame


class Laberinto(pygame.sprite.Sprite):
	def __init__(self, game, x, y, valor):
		super().__init__()
		self.game = game 

		img = pygame.image.load('pacGraf/bloquepac.png').convert()
		escalaX = self.game.BSX		# Bloque es de 50x50px ********
		escalaY = self.game.BSY
		self.image = pygame.transform.scale(img, (escalaX, escalaY))
		self.image.set_colorkey((255, 255, 255))
		self.rect = self.image.get_rect()
		self.rect.x = x 
		self.rect.y = y 
		self.valor = valor


	def update(self):
		pass



class Puntitos(pygame.sprite.Sprite):
	def __init__(self, game, centerx, centery, valor):
		super().__init__()
		self.game = game 

		img = pygame.image.load('pacGraf/pildopac.png').convert()
		escalaX = self.game.BSX // 5 		# Puntitos es de 10x10px ***
		escalaY = self.game.BSY // 5
		self.image = pygame.transform.scale(img, (escalaX, escalaY))
		self.image.set_colorkey((255, 255, 255))
		self.rect = self.image.get_rect()
		self.rect.centerx = centerx
		self.rect.centery = centery
		self.valor = valor
		self.sumaPtos = 10


	def update(self):
		pass


class Items(pygame.sprite.Sprite):
	def __init__(self, game, centerx, centery):
		super().__init__()
		self.game = game 

		escalaX = self.game.BSX // 1.11		# Item es de 45x45px ***
		escalaY = self.game.BSY // 1.11

		fruta = self.game.nivel
		if fruta > 4:
			fruta = 4

		img = pygame.image.load('pacGraf/item{}.png'.format(fruta)).convert()
		self.image = pygame.transform.scale(img, (escalaX, escalaY))
		self.image.set_colorkey((255, 255, 255))
		self.rect = self.image.get_rect()
		self.radius = self.game.BSX // 2 // 1.5
		self.rect.centerx = centerx 
		self.rect.centery = centery
		lista_sumaPtos = [100, 100, 300, 500, 800, 1200, 1500, 3000, 5000]
		elegir = self.game.nivel
		if elegir > 8:
			elegir = 8

		self.sumaPtos = lista_sumaPtos[elegir]


	def update(self):
		pass


class PuntosGordos(pygame.sprite.Sprite):
	def __init__(self, game, centerx, centery):
		super().__init__()
		self.game = game 

		self.nroAnimaciones = 8
		self.enemigos_anima = []
		for i in range(self.nroAnimaciones):
			file = 'pacGraf/pildopacxl{}.png'.format(i + 1)
			img = pygame.image.load(file).convert()
			escalaX = self.game.BSX - (5 * self.game.BSX // 50) * i
			escalaY = self.game.BSY - (5 * self.game.BSY // 50) * i
			img2 = pygame.transform.scale(img, (escalaX, escalaY))
			img2.set_colorkey((255, 255, 255))
			self.enemigos_anima.append(img2)

		self.image = self.enemigos_anima[0]
		self.rect = self.image.get_rect()
		self.radius = self.game.BSX // 2 // 1.5
		self.rect.centerx = centerx
		self.rect.centery = centery
		self.sumaPtos = 50
		self.fotograma = 5
		self.ultimo_update = pygame.time.get_ticks()
		self.fotograma_vel = 70


	def update(self):
		calculo = pygame.time.get_ticks()
		if calculo - self.ultimo_update > self.fotograma_vel:
			self.ultimo_update = calculo
			self.fotograma += 1
			if self.fotograma >= self.nroAnimaciones:
				self.fotograma = 0

			centerx = self.rect.centerx
			centery = self.rect.centery
			self.image = self.enemigos_anima[self.fotograma]
			self.rect = self.image.get_rect()
			self.rect.centerx = centerx
			self.rect.centery = centery




