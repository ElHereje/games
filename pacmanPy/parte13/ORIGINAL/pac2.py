import pygame
import random


class Fantasma(pygame.sprite.Sprite):
	def __init__(self, game, centerx, centery, tipoFantasma, direccion):
		super().__init__()
		self.game = game 
		self.tipoF = tipoFantasma
		self.direccion = direccion

		self.enemigos_anima = []
		self.nro_fotogramas = 5
		for i in range(self.nro_fotogramas):
			if i < 3:
				file = 'pacGraf/fantasma{}.png'.format(self.tipoF + i)
				img = pygame.image.load(file).convert()
				escalaX = self.game.BSX
				escalaY = self.game.BSY
				img2 = pygame.transform.scale(img, (escalaX, escalaY))
				img2.set_colorkey((255, 255, 255))
				self.enemigos_anima.append(img2)
			else:
				file = 'pacGraf/fantasmaAzul{}.png'.format(i - 2)
				img = pygame.image.load(file).convert()
				escalaX = self.game.BSX
				escalaY = self.game.BSY
				img2 = pygame.transform.scale(img, (escalaX, escalaY))
				img2.set_colorkey((255, 255, 255))
				self.enemigos_anima.append(img2)


		self.image = self.enemigos_anima[0]
		self.rect = self.image.get_rect()
		self.radius = self.game.BSX // 2 // 1.5
		self.rect.centerx = centerx
		self.rect.centery = centery
		self.cx = self.game.cx 
		self.cy = self.game.cy 
		self.cx[(self.tipoF - 1) // 10] = self.rect.centerx
		self.cy[(self.tipoF - 1) // 10] = self.rect.centery
		self.hacia_donde = {
			'le' : 'doupri', 'ri' : 'updole',
			'up' : 'lerido', 'do' : 'leriup'
		}
		self.hacia_donde_velXY = {
			'le' : [-2, 0], 'ri' : [2, 0],
			'up' : [0, -2], 'do' : [0, 2]
		}
		self.ptosClave = [
			(75, 425), (225, 225), (225, 425), (225, 675), (225, 575),
			(325, 575), (225, 75), (425, 425), (325, 225),
			(875, 425), (725, 225), (725, 425), (725, 675), (725, 575),
			(625, 575), (725, 75), (525, 425), (625, 225)
		]
		self.i_d = self.game.lista_fantasmas[(self.tipoF - 1) // 10]
		self.vel_x = self.hacia_donde_velXY[self.direccion][0]
		self.vel_y = self.hacia_donde_velXY[self.direccion][1]
		self.fotograma = 0
		self.ultimo_update = pygame.time.get_ticks()
		self.fotograma_vel = 90		# Velocidad de la animacion


	def update(self):
		if self.game.kill_fantasmas:
			self.kill()

		if not self.game.enjuego:
			return

		if self.game.countDownAzules > 0:
			if self.check_colision_esteFantasmaConcreto():
				for i in range(4):
					self.game.mostrar_ptosComeFantasmas[i] = 0 

				self.game.mostrar_ptosComeFantasmas[(self.tipoF - 1) // 10] = 100 
				self.game.coordXY_mostrarPtosCF[(self.tipoF - 1) // 10] = (self.rect.x,
					self.rect.y)
				self.game.sumaPtosComeFantasmas *= 2
				self.game.puntos += self.game.sumaPtosComeFantasmas
				if len(self.game.lista_los4fantasmas) == 0:
					self.game.countDownAzules = 5 	# Se puede poner 0

				self.game.sonido_eatingGhost.play()
				self.game.instanciar_ojosSinFantasma(self.rect.centerx, self.rect.centery,
					(self.tipoF - 1) // 10, self.direccion)
				
				self.kill()


		calculo = pygame.time.get_ticks()
		if calculo - self.ultimo_update > self.fotograma_vel:
			self.ultimo_update = calculo
			self.fotograma += 1

			if self.fotograma >= self.nro_fotogramas - 2:
				self.fotograma = 0

			if self.game.countDownAzules <= 0:
				centerx = self.rect.centerx
				centery = self.rect.centery
				self.image = self.enemigos_anima[self.fotograma]
				self.rect = self.image.get_rect()
				self.rect.centerx = centerx
				self.rect.centery = centery

			elif self.game.countDownAzules < 300:
				centerx = self.rect.centerx
				centery = self.rect.centery
				self.image = self.enemigos_anima[self.fotograma + 2]
				self.rect = self.image.get_rect()
				self.rect.centerx = centerx
				self.rect.centery = centery

			else:
				centerx = self.rect.centerx
				centery = self.rect.centery
				self.image = self.enemigos_anima[self.nro_fotogramas - 2]
				self.rect = self.image.get_rect()
				self.rect.centerx = centerx
				self.rect.centery = centery


		for i in self.ptosClave:
			if self.rect.centerx == i[0] and self.rect.centery == i[1]:
				if self.game.countDownAzules <= 0:
					self.fantasmaPersigue()


		if self.rect.centerx % (self.game.BSX // 2) == 0 and self.rect.centery % (self.game.BSY // 2) == 0:
			if self.direccion == 'le':
				self.rect.centerx -= self.game.BSX
				laberinto = self.game.pacman.check_colision_laberinto(self.i_d)
				if not laberinto:
					self.vel_x = -2
					self.vel_y = 0

				self.rect.centerx += self.game.BSX

			if self.direccion == 'ri':
				self.rect.centerx += self.game.BSX
				laberinto = self.game.pacman.check_colision_laberinto(self.i_d)
				if not laberinto:
					self.vel_x = 2
					self.vel_y = 0

				self.rect.centerx -= self.game.BSX

			if self.direccion == 'up':
				self.rect.centery -= self.game.BSY
				laberinto = self.game.pacman.check_colision_laberinto(self.i_d)
				if not laberinto:
					self.vel_x = 0
					self.vel_y = -2

				self.rect.centery += self.game.BSY

			if self.direccion == 'do':
				self.rect.centery += self.game.BSY
				laberinto = self.game.pacman.check_colision_laberinto(self.i_d)
				if not laberinto:
					self.vel_x = 0
					self.vel_y = 2

				self.rect.centery -= self.game.BSY


		laberinto = self.game.pacman.check_colision_laberinto(self.i_d)
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
			self.elegir_otra_direccion()

		self.cx[(self.tipoF - 1) // 10] = self.rect.centerx
		self.cy[(self.tipoF - 1) // 10] = self.rect.centery
		self.cx[(self.tipoF - 1) // 10 + 4] = self.vel_x
		self.cy[(self.tipoF - 1) // 10 + 4] = self.vel_y


	def elegir_otra_direccion(self):
		direcc = self.hacia_donde[self.direccion]
		num_rnd = random.randrange(0, 3, 2)
		self.direccion = direcc[num_rnd] + direcc[num_rnd + 1]


	def fantasmaPersigue(self):
		hor_ver = random.randrange(10)
		if hor_ver < 5:
			if self.game.pacman.rect.centery < self.rect.centery:
				self.direccion = 'up'
			elif self.game.pacman.rect.centery > self.rect.centery:
				self.direccion = 'do'
		else:
			if self.game.pacman.rect.centerx < self.rect.centerx:
				self.direccion = 'le'
			elif self.game.pacman.rect.centerx > self.rect.centerx:
				self.direccion = 'ri'


	def check_colision_esteFantasmaConcreto(self):
		impacto = pygame.sprite.groupcollide(self.game.lista_fantasmas[(self.tipoF - 1) // 10], 
			self.game.lista_pacman, True, False)

		return impacto



class Ojos(pygame.sprite.Sprite):
	def __init__(self, game, tipoFantasma):
		super().__init__()
		self.game = game 
		self.tipoF = tipoFantasma

		img = pygame.image.load('pacGraf/ojos_fantasma.png').convert()
		escalaX = self.game.BSX // 2.5 		# Ojos es de 20x5px
		escalaY = self.game.BSY // 20
		self.image = pygame.transform.scale(img, (escalaX, escalaY))
		self.image.set_colorkey((255, 255, 255))
		self.rect = self.image.get_rect()
		fantasmaX = self.game.fantasma.cx 
		fantasmaY = self.game.fantasma.cy
		self.rect.centerx = fantasmaX[self.tipoF] + fantasmaX[self.tipoF + 4]
		self.escalaCorreccY = (9 * self.game.BSY) // 50
		self.rect.centery = fantasmaY[self.tipoF] + fantasmaY[self.tipoF + 4] - self.escalaCorreccY


	def update(self):
		if self.game.kill_fantasmas:
			self.kill()

		if len(self.game.lista_fantasmas[self.tipoF]) == 0:
			self.kill()

		#print(self.rect.centerx, self.rect.centery)
		fantasmaX = self.game.fantasma.cx
		fantasmaY = self.game.fantasma.cy
		self.rect.centerx = fantasmaX[self.tipoF] + fantasmaX[self.tipoF + 4]
		self.rect.centery = fantasmaY[self.tipoF] + fantasmaY[self.tipoF + 4] - self.escalaCorreccY



class OjosSinFantasma(pygame.sprite.Sprite):
	def __init__(self, game, centerx, centery, tipoFantasma, direccion):
		super().__init__()
		self.game = game 

		self.nroAnimaciones = 5
		self.enemigos_anima = []
		for i in range(self.nroAnimaciones):
			file = 'pacGraf/ojos_sin_fantasma{}.png'.format(i)
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
		self.direccion = direccion
		self.tipoF = tipoFantasma
		self.i_d = self.game.lista_ojosSinFantasma[self.tipoF]
		self.hacia_donde = {
			'le' : 'doupri', 'ri' : 'updole',
			'up' : 'lerido', 'do' : 'leriup'
		}
		self.hacia_donde_velXY = {
			'le' : [-2, 0], 'ri' : [2, 0],
			'up' : [0, -2], 'do' : [0, 2]
		}
		self.queOjosDibujar = {'le' : 2, 'ri' : 1, 'up' : 3, 'do' : 4}
		self.vel_x = self.hacia_donde_velXY[direccion][0]
		self.vel_y = self.hacia_donde_velXY[direccion][1]


	def update(self):
		if self.game.countDownAzules <= 0:
			self.kill()

		centerx = self.rect.centerx
		centery = self.rect.centery
		self.image = self.enemigos_anima[self.queOjosDibujar[self.direccion]]
		self.rect = self.image.get_rect()
		self.rect.centerx = centerx
		self.rect.centery = centery

		if self.rect.centerx % (self.game.BSX // 2) == 0 and self.rect.centery % (self.game.BSY // 2) == 0:
			if self.direccion == 'le':
				self.rect.centerx -= self.game.BSX
				laberinto = self.game.pacman.check_colision_laberinto(self.i_d)
				if not laberinto:
					self.vel_x = -2
					self.vel_y = 0

				self.rect.centerx += self.game.BSX

			if self.direccion == 'ri':
				self.rect.centerx += self.game.BSX
				laberinto = self.game.pacman.check_colision_laberinto(self.i_d)
				if not laberinto:
					self.vel_x = 2
					self.vel_y = 0

				self.rect.centerx -= self.game.BSX

			if self.direccion == 'up':
				self.rect.centery -= self.game.BSY
				laberinto = self.game.pacman.check_colision_laberinto(self.i_d)
				if not laberinto:
					self.vel_x = 0
					self.vel_y = -2

				self.rect.centery += self.game.BSY

			if self.direccion == 'do':
				self.rect.centery += self.game.BSY
				laberinto = self.game.pacman.check_colision_laberinto(self.i_d)
				if not laberinto:
					self.vel_x = 0
					self.vel_y = 2

				self.rect.centery -= self.game.BSY


		laberinto = self.game.pacman.check_colision_laberinto(self.i_d)
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
			self.elegir_otra_direccion()


	def elegir_otra_direccion(self):
		direcc = self.hacia_donde[self.direccion]
		num_rnd = random.randrange(0, 3, 2)
		self.direccion = direcc[num_rnd] + direcc[num_rnd + 1]







