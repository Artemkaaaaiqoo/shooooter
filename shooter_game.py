from pygame import *
from random import randint
from time import time as timer
score = 0
lost = 0
class GameSprite(sprite.Sprite):
    def __init__(self, player_img, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_img), (size_x, size_y))
        self.speed = player_speed
        # прямоугольник каждого спрайта
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self): 
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 15, 20)
        bullets.add(bullet)
        # bullets = Sprite.Group()


# создаём врагов
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed # перемещаем спрайт ниже
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(100, 600)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed # перемещаем спрайт выше
        if self.rect.y < 0: # проверка выхода за границу
            self.kill()

window = display.set_mode((700, 500)) # создаем окно приложения
display.set_caption('Shooter') # заголовок окна
background = transform.scale(image.load('galaxy.jpg'), (700, 500)) 

# mixer.init()
# mixer.music.load('space.ogg')
# mixer.music.play()
# fire = mixer.Sound('fire.ogg')


font.init()
font1 = font.SysFont('Arial', 36)

game = True
finish = False
clock = time.Clock()
fps = 120
# картинка, координата х, координата у, скорость, размер по х, размер по у
rocket = Player('rocket.png', 300, 400, 10, 80, 100)

monsters = sprite.Group() # группа спрайтов
for i in range(5):
    monster = Enemy('ufo.png', randint(100, 600), -20, randint(2, 7), 80, 50)
    monsters.add(monster)

bullets = sprite.Group() # группа для пуль

asteroids = sprite.Group() # группа для астероидов
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(100, 600), -20, randint(2, 7), 80, 50)
    asteroids.add(asteroid)

life = 3 # количество жизней
rel_time = False # перезарядка 
num_fire = 0 # количество выстрелов
while game:
    for e in event.get(): # для всех событий системы
        if e.type == QUIT: # если событие типа нажатие на крестик
                game = False # завершаем
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                rocket.fire()
                if rel_time == False and num_fire >= 5:
                    rel_time = True
                    last_time = timer()
               #fire.play()
    if finish != True:
        
        window.blit(background, (0, 0))

        text_score = font1.render('Счёт: ' + str(score), 1, (255, 255, 255))
        text_lost = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))

        window.blit(text_score, (10, 20))
        window.blit(text_lost, (10, 50))

        rocket.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        
        rocket.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        for s in sprite_list:
            score += 1
            monster = Enemy('ufo.png', randint(100, 600), -20, randint(2, 7), 80, 50)
            monsters.add(monster)
        
        if sprite.spritecollide(rocket, asteroids, True):
            life -= 1
        text_life = font1.render('Жизни: ' + str(life), 1, (255, 255, 255))
        window.blit(text_life ,(580, 10))
        if rel_time == True:
            new_time = timer()
            if new_time - last_time < 3:
                reload = font1.render('Перезагрузка', 1, (255, 255, 255))
                window.blit(reload, (250, 450))
            else:
                num_fire = 0
                rel_time = False
        # условие победы
        if score == 10:
            finish = True
            font2 = font.SysFont('Arial', 70)
            win = font2.render('YOU WON!', True, (0,255,0))
            window.blit(win, (200,200))

        # условие проигрыша
        if lost == 3 or life == 0: # if lost == 3 or sprite.spritecollide(rocket, monsters, False):
            finish = True
            font2 = font.SysFont('Arial', 70)
            win = font2.render('YOU LOSE!', True, (0,255,0))
            window.blit(win, (200,200))

        

    display.update()
    clock.tick(fps)
