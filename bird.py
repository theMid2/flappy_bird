import pygame
import random

pygame.init()
width = 544
height = 320
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('BIRDY')
red = (255, 0, 0)
tan4 = (139, 90, 43)
green4 = (0, 139, 0)

img = [pygame.image.load('Frame-1.png'), pygame.image.load('frame-2.png'), pygame.image.load('frame-3.png'),
       pygame.image.load('frame-4.png')]
bg = [pygame.image.load('bg1.png'), pygame.image.load('bg2.png'), pygame.image.load('bg3.png'),
      pygame.image.load('bg4.png'), pygame.image.load('bg5.png')]
bg2 = pygame.image.load('image.jpeg')
pillar_img = pygame.image.load('Screenshot.jpg')

# sound1 = pygame.mixer.music.load('Aion_Fairy_Of_The_Peace.mid')
# sound2 = pygame.mixer.music.load('Avengers_Theme__8_bit.mp3')
# pygame.mixer.music.play(-1)

winSound = pygame.mixer.Sound('level.wav')
# hitSound = pygame.mixer.Sound('score.wav')
# gSound = pygame.mixer.Sound('out.wav')

score = 0
size = []
for i in range(96, 164):
    size.append(i)
clock = pygame.time.Clock()


class Play:
    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.vel = vel
        self.jump = False
        self.count = 1
        self.hitbox = (self.x+28, self.y+21)

    def draw(self, win):
        win.blit(img[1], (player.x, player.y))
        self.hitbox = (self.x+28, self.y+21)
        pygame.draw.circle(win, (255, 0, 0), self.hitbox, 22, 1)


class Pillars:
    def __init__(self, x, length, vel):
        self.x = x
        self.length = length
        self.y1 = -(164 - self.length)
        self.y2 = (self.length + 100)
        self.dis = 40
        self.vel = vel

    def draw(self, win):
        win.blit(pillar_img, (self.x, self.y1))
        win.blit(pillar_img, (self.x, self.y2))


def redrawGame():
    screen.blit(bg[0], (0, 0))
    screen.blit(bg[1], (0, height//2))
    screen.blit(bg[2], (0, 0))
    screen.blit(bg[3], (0, height//2))
    screen.blit(bg[4], (0, height//2))
    # screen.blit(bg2, (0, 0))
    player.draw(screen)
    if start:
        for pi in pil:
            pi.draw(screen)
    text = font1.render('SCORE : '+str(score), 1, (0, 0, 200))
    overText = font2.render('GAMEOVER', 1, (255, 0, 0))
    starter = font3.render('Press space to start!', 1, (255, 0, 0))
    screen.blit(text, (width-90, 3))
    if not start:
        screen.blit(starter, ((width / 2) - overText.get_width()/2, (height / 2) - overText.get_height()/2))
    pygame.display.update()


font1 = pygame.font.SysFont('comicsans', 20, True)
font2 = pygame.font.SysFont('comicsans', 50, True)
font3 = pygame.font.SysFont('comicsans', 30, True)
player = Play(100, height//2, 1)
pil = []
pildis = 0
start = False
notHit = True
# ------- mainloop ----------------------------------------
over = False
while not over:
    clock.tick(20)
    if pildis > 0:
        pildis += 1
    if pildis > 40:
        pildis = 0
    if player.jump:
        player.y += player.vel
        start = True
    if start:
        if len(pil) < 7 and pildis == 0:
            pil.append(Pillars(width, random.choice(size), 3))
            pildis = 1
    # ----------- Pillar list-----------collision-detection-----------------------------------
    for pi in pil:
        if pi.y1+164 > player.hitbox[1]-21:
            if pi.x < player.hitbox[0]+22 and pi.x+40 > player.hitbox[0]-22:
                # pygame.mixer.music.pause()
                notHit = False
        elif pi.y2 < player.hitbox[1]+19:
            if pi.x < player.hitbox[0]+22 and pi.x+40 > player.hitbox[0]-22:
                # pygame.mixer.music.pause()
                notHit = False
        elif pi.x+40 == player.hitbox[0]:
            score += 1
        if notHit:
            if pi.x > -50:
                pi.x -= pi.vel
            else:
                pil.pop(pil.index(pi))

    if player.y+20 >= height:
        # pygame.mixer.music.pause()
        notHit = False
    if score % 10 == 0 and score > 0 and pi.x+40 == player.hitbox[0]-22:
        winSound.play()
    # -------------------------RESTART------------------------------------------------
    if not notHit:
        # hitSound.play()
        font2 = pygame.font.SysFont('comicsans', 50, True)
        overText = font2.render('GAMEOVER', 1, (255, 0, 0))
        screen.blit(overText, ((width / 2) - overText.get_width() / 2, (height / 2) - overText.get_height() / 2))
        pygame.display.update()
        score = 0
        notHit = True
        start = False
        player.jump = False
        pil = []
        player.x = 100
        player.y = height//2
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
        # pygame.mixer.music.play(-1)
    # ----------------------------JUMP--------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if notHit:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.y -= 35
                    player.vel = 1
                    player.jump = True

    player.vel += 1
    redrawGame()

pygame.quit()
