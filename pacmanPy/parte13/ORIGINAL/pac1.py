import pygame
import random


class PacMan(pygame.sprite.Sprite):
	def __init__(self, game, centerx, centery):
		super().__init__()
		self.game = game 

		self.enemigos_anima = []
		for i in range(25):
			file = 'pacGraf/pacman{}.png'.format(i)
			img = pygame.image.load(file).convert()
			escalaX = self.game.BSX
			escalaY = self.game.BSY
			img2 = pygame.transform.scale(img, (escalaX, escalaY))
			img2.set_colorkey((255, 255, 255))
			self.enemigos_anima.append(img2)

		self.image = self.enemigos_anima[1]
		self.rect = self.image.get_rect()
		self.radius = self.game.BSX // 2 // 1.5
		self.rect.centerx = centerx
		self.rect.centery = centery
		self.i_d = self.game.lista_pacman
		self.pulsada = 'right'
		self.orientacion = 1	# A la derecha (por defecto)
		self.orientacion_max = self.orientacion + 6
		#self.escalarVelX = round((self.game.BSX * 2) / 50)
		#self.escalarVelY = round((self.game.BSY * 2) / 50)
		#print(self.escalarVelX, self.escalarVelY)
		self.escalarVelX = 2 
		self.escalarVelY = 2
		self.vel_x = self.escalarVelX
		self.vel_y = 0
		self.ultimo_update = pygame.time.get_ticks()
		self.fotograma_vel = 50		# Velocidad de la animacion
		self.sonarSirena = 0
		self.ultimo_updateSirena = pygame.time.get_ticks()
		self.cadenciaSirena = 500	# Cada cuanto suena (para NO acumular el Buffer)


	def update(self):
		if not self.game.enjuego:
			return

		self.leer_teclado()

		#print('pos:', self.rect.centerx, self.rect.centery)
		calculo = pygame.time.get_ticks()
		if calculo - self.ultimo_update > self.fotograma_vel:
			self.ultimo_update = calculo
			self.orientacion += 1
			if self.orientacion >= self.orientacion_max:
				self.orientacion = self.orientacion_max - 6

			centerx = self.rect.centerx
			centery = self.rect.centery
			self.image = self.enemigos_anima[self.orientacion]
			self.rect = self.image.get_rect()
			self.rect.centerx = centerx
			self.rect.centery = centery

		
		if self.check_colision_puntitos():
			self.game.puntos += self.game.puntitos.sumaPtos
			self.game.sonido_sirena.stop()
			self.game.sonido_wakawaka.play(maxtime=500)
		else:
			calculoSirena = pygame.time.get_ticks()
			if calculoSirena - self.ultimo_updateSirena > self.cadenciaSirena:
				self.ultimo_updateSirena = calculoSirena
				if self.game.countDownAzules <= 0:
					self.game.sonido_sirena.play(maxtime=500)
				else:
					self.game.sonido_fantasmas_azules.play(maxtime=500)

		if self.check_colision_item():
			self.game.puntos += self.game.item.sumaPtos
			self.game.mostrarPtosItem = 120
			self.game.salir_otro_item = pygame.time.get_ticks()
			self.game.sonido_sirena.stop()
			self.game.sonido_eatingCherry.play()

		if self.check_colision_puntosGordos():
			self.game.puntos += self.game.puntosgordos.sumaPtos
			self.game.countDownAzules = self.game.duracionAzules
			self.game.sumaPtosComeFantasmas = 100
			self.game.sonido_sirena.stop()
			self.game.sonido_eatingGhost.play()


		if self.rect.centerx % (self.game.BSX // 2) == 0 and self.rect.centery % (self.game.BSY // 2) == 0:
			if self.pulsada == 'left':
				self.rect.centerx -= self.game.BSX
				laberinto = self.check_colision_laberinto(self.i_d)
				if not laberinto:
					self.orientacion = 7
					self.orientacion_max = self.orientacion + 6
					self.vel_x = -self.escalarVelX
					self.vel_y = 0

				self.rect.centerx += self.game.BSX

			if self.pulsada == 'right':
				self.rect.centerx += self.game.BSX
				laberinto = self.check_colision_laberinto(self.i_d)
				if not laberinto:
					self.orientacion = 1
					self.orientacion_max = self.orientacion + 6
					self.vel_x = self.escalarVelX
					self.vel_y = 0

				self.rect.centerx -= self.game.BSX

			if self.pulsada == 'up':
				self.rect.centery -= self.game.BSY
				laberinto = self.check_colision_laberinto(self.i_d)
				if not laberinto:
					self.orientacion = 13
					self.orientacion_max = self.orientacion + 6
					self.vel_x = 0
					self.vel_y = -self.escalarVelY

				self.rect.centery += self.game.BSY

			if self.pulsada == 'down':
				self.rect.centery += self.game.BSY
				laberinto = self.check_colision_laberinto(self.i_d)
				if not laberinto:
					self.orientacion = 19
					self.orientacion_max = self.orientacion + 6
					self.vel_x = 0
					self.vel_y = self.escalarVelY

				self.rect.centery -= self.game.BSY

		laberinto = self.check_colision_laberinto(self.i_d)
		if not laberinto:
			self.rect.centerx += self.vel_x
			self.rect.centery += self.vel_y
			if self.rect.centerx < -self.game.BSX // 2:
				self.rect.centerx = self.game.BSX * self.game.NRO_COLUMNAS + self.game.BSX // 2
				pygame.time.delay(100)
			elif self.rect.centerx > self.game.BSX * self.game.NRO_COLUMNAS + self.game.BSX // 2:
				self.rect.centerx = -self.game.BSX // 2
				pygame.time.delay(100)
		
		else:
			self.rect.centerx += -self.vel_x
			self.rect.centery += -self.vel_y



	def leer_teclado(self):
		tecla = pygame.key.get_pressed()

		if tecla[pygame.K_LEFT]:
			self.pulsada = 'left'

		elif tecla[pygame.K_RIGHT]:
			self.pulsada = 'right'

		elif tecla[pygame.K_UP]:
			self.pulsada = 'up'

		elif tecla[pygame.K_DOWN]:
			self.pulsada = 'down'


	def check_colision_laberinto(self, i_d):
		impactos = pygame.sprite.groupcollide(self.game.lista_laberinto, i_d, False, False)
		for impacto in impactos:
			#print(impacto.rect.centerx, impacto.rect.centery, self.rect.centerx, self.rect.centery)
			return True

		return False


	def check_colision_puntitos(self):
		impactos = pygame.sprite.groupcollide(self.game.lista_puntitos, self.game.lista_pacman, True, False)
		for impacto in impactos:
			return True

		return False


	def check_colision_puntosGordos(self):
		impactos = pygame.sprite.groupcollide(self.game.lista_puntosGordos, self.game.lista_pacman, True, False)
		for impacto in impactos:
			return True

		return False


	def check_colision_item(self):
		impactos = pygame.sprite.groupcollide(self.game.lista_items, 
			self.game.lista_pacman, True, False, pygame.sprite.collide_circle)
		for impacto in impactos:
			return True

		return False


	def check_colision_fantasmas(self):
		impactos = pygame.sprite.groupcollide(self.game.lista_los4fantasmas, 
			self.game.lista_pacman, False, False, pygame.sprite.collide_circle)
		for impacto in impactos:
			self.kill()
			return True

		return False


class PacManDies(pygame.sprite.Sprite):
	def __init__(self, game, centerx, centery):
		super().__init__()
		self.game = game 

		animaciones = [1, 19, 7, 13]
		self.enemigos_anima = []
		for i in animaciones:
			file = 'pacGraf/pacman{}.png'.format(i)
			img = pygame.image.load(file).convert()
			escalaX = self.game.BSX
			escalaY = self.game.BSY
			img2 = pygame.transform.scale(img, (escalaX, escalaY))
			img2.set_colorkey((255, 255, 255))
			self.enemigos_anima.append(img2)

		self.image = self.enemigos_anima[0]
		self.rect = self.image.get_rect()
		self.rect.centerx = centerx
		self.rect.centery = centery
		self.vueltas = 0
		self.fotograma = 0
		self.ultimo_update = pygame.time.get_ticks()
		self.fotograma_vel = 150 # Velocidad animacion


	def update(self):
		calculo = pygame.time.get_ticks()
		if calculo - self.ultimo_update > self.fotograma_vel:
			self.ultimo_update = calculo
			self.fotograma += 1
			if self.fotograma >= 4:
				self.fotograma = 0
				self.vueltas += 1

			centerx = self.rect.centerx
			centery = self.rect.centery
			self.image = self.enemigos_anima[self.fotograma]
			self.rect = self.image.get_rect()
			self.rect.centerx = centerx
			self.rect.centery = centery

		if self.vueltas >= 3:
			self.game.enjuego = True
			self.game.reinstanciar_pacmanfantasmas = True
			self.kill()

		elif self.vueltas == 2:
			self.game.kill_fantasmas = True




class MostrarVidas(pygame.sprite.Sprite):
	def __init__(self, game, y):
		super().__init__()
		self.game = game 

		img = pygame.image.load('pacGraf/pacman1.png').convert()
		escalaX = self.game.BSX
		escalaY = self.game.BSY
		self.image = pygame.transform.scale(img, (escalaX, escalaY))
		self.image.set_colorkey((255, 255, 255))
		self.rect = self.image.get_rect()
		self.rect.x = self.game.BSX * self.game.NRO_COLUMNAS
		self.rect.y = self.game.BSY * (4 + y)


	def update(self):
		if self.game.kill_fantasmas:
			self.kill()


