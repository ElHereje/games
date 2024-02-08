import pygame

class Laberinto(pygame.sprite.Sprite):
    def __init__(self, game, x, y, valor):
        super().__init__()
        self.game = game

        self.image = pygame.image.load('pacGraf/bloquepac1.png').convert()
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

        self.image = pygame.image.load('pacGraf/pildopac.png').convert()
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

        self.image = pygame.image.load('pacGraf/item1.png').convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.radius = self.game.BSX // 2 // 1.5

        # fijamos los puntos para los items
        self.sumaPtos = 100

    def update(self):
        pass