import pygame

class Laberinto(pygame.sprite.Sprite):
    def __init__(self, game, x, y, valor):
        super().__init__()
        self.game = game
        img = pygame.image.load('pacGraf/bloquepac.png').convert()
        escalaX = self.game.BSX
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
        # puntitos no es 50x50, sino 10x10, por lo que podemos dividir entre 5
        escalaX = self.game.BSX // 5
        escalaY = self.game.BSY // 5
        self.image = pygame.transform.scale(img, (escalaX, escalaY))

        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.valor = valor # al compartar con laberinto --> 0 = vacio / 1 = puntito
        self.sumaPuntos = 10

    def update(self):
        pass


class Items(pygame.sprite.Sprite):
    def __init__(self, game, centerx, centery):
        super().__init__()
        self.game = game
        img = pygame.image.load('pacGraf/item1.png').convert()
        # las imagenes son de mas o menos 45x45 --> dividimos por 1.11
        escalaX = self.game.BSX // 1.11
        escalaY = self.game.BSY // 1.11
        self.image = pygame.transform.scale(img, (escalaX, escalaY))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.radius = self.game.BSX // 2 // 1.5
        self.sumaPtos = 100

    def update(self):
        pass



# 1d - CREAMOS LA CLASE PTOS GORDOS
class PuntosGordos(pygame.sprite.Sprite):
    def __init__(self, game, centerx, centery):
        super().__init__()
        self.game = game
        self.nroAnimaciones = 8 # nº de imagenes
        self.enemigos_anima = []
        for i in range(self.nroAnimaciones):
            file = f'pacGraf/pildopacxl{i+1}.png'
            img = pygame.image.load(file).convert()
            escalaX = self.game.BSX - 5 * i
            escalaY = self.game.BSY - 5 * i
            img2 = pygame.transform.scale(img, (escalaX, escalaY))
            img2.set_colorkey((255, 255, 255))
            self.enemigos_anima.append(img2)

        self.image = self.enemigos_anima[0] # ponemos el 1ª imagen en la lista
        self.rect = self.image.get_rect()
        self.radius = self.game.BSX // 2 //1.5
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
    