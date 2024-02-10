import pygame

class Laberinto(pygame.sprite.Sprite):
    def __init__(self, game, x, y, valor):
        super().__init__()
        self.game = game

        # 1 - MODIFICAMOS EL TAMAÑO DE LOS BLOQUIES CON EL ESCALADO
        img = pygame.image.load('pacGraf/bloquepac1.png').convert()
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

        # 3 - ESCALAMOS LA IMAGEN DE LOS PUNTITOS
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

        # 4 - ESCALAMOS LA IMAGENN DE LOS ITEMS
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