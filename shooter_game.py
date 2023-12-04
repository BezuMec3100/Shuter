#Создай собственный Шутер!

from pygame import *
from random import *
font.init()
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 120)
mixer.init()
window = display.set_mode((700, 500))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"),(700, 500))
window.blit(background, (0, 0))

mixer.music.load("space.ogg")
clock = time.Clock()

#коментарий

FPS = 60
run = True
lost = 0
score = 0

class Gamesprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load (player_image), (75, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Gamesprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 625:
            self.rect.x += self.speed
    def fire(self):
        bullet1 = Bullet("laser2.png", self.rect.centerx, self.rect.top, 15)
        bullets.add(bullet1)


class Enemy(Gamesprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load (player_image), (85, 55))
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(50, 650)
            self.rect.y = 0
            lost = lost + 1

class Bullet(Gamesprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load (player_image), (25, 35))
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

#mixer.music.play()
rocket1 = Player("korablik.png",10 , 400, 7)
monsters = sprite.Group()
bullets = sprite.Group()
text_lose = font1.render("Пропущенно: " + str(lost), 1, (255, 255, 255))
text_win = font1.render("Счет: " + str(score), 1, (255, 255, 255))

text_defeat = font1.render("YOU LOSE!", 1, (255, 0 ,0))
text_victore = font1.render("YOU WIN!", 1, (0, 255 ,0))
for i in range(5):
    monster = Enemy("tarelka2.png", randint(80, 650), 20, randint(1, 3))
    monsters.add(monster)
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket1.fire()
    window.blit(background, (0, 0))
    window.blit(text_lose, (10, 70))
    text_lose = font1.render("Пропущенно: " + str(lost), 1, (255, 255, 255))
    text_win = font1.render("Счет: " + str(score), 1, (255, 255, 255))
    text_defeat = font2.render("YOU LOSE!", 1, (255, 0 ,0))
    text_victore = font2.render("YOU WIN!", 1, (0, 255 ,0))
    window.blit(text_win, (10, 30))
    sprites_list = sprite.spritecollide(rocket1, monsters, False)
    if lost >= 3 or len(sprites_list) > 0:
        window.blit(text_defeat, (100, 200))
        rocket1.speed = 0
        for b in bullets:
            b.speed = 0
        for m in monsters:
            m.speed = 0

    
    elif score >= 10:
        window.blit(text_victore, (110, 200))
        rocket1.speed = 0
        for b in bullets:
            b.speed = 0
        for m in monsters:
            m.speed = 0
    
        
    rocket1.update()
    rocket1.reset()
    monsters.update()
    bullets.update()
    bullets.draw(window)
    monsters.draw(window)
    collides = sprite.groupcollide(monsters, bullets, True, True)
    for l in collides:
        score +=1
        monster = Enemy("tarelka2.png", randint(80, 650), 20, randint(1, 3))
        monsters.add(monster)
    clock.tick(FPS)
    display.update()

