import pygame
import os
import random

pygame.mixer.init()
pygame.font.init()

# constant variables
WIDTH, HEIGHT = 700, 690
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gabe's Game")

SECONDS_FONT = pygame.font.SysFont('comicsans', 30)
GAMEOVER_FONT = pygame.font.SysFont('comicsans', 30)

DEATH_SOUND = pygame.mixer.Sound(os.path.join('gameItems', 'boom.mp3'))
MUSIC = pygame.mixer.Sound(os.path.join('gameItems', 'music.wav'))
AHH = pygame.mixer.Sound(os.path.join('gameItems', 'ahh.mp3'))
LAUGH = pygame.mixer.Sound(os.path.join('gameItems', 'kingLaugh.mp3'))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (70, 10, 10)

FPS = 60  # how fast the game can run
VEL = 6
MAX_ASTOIRDS = 12
ASTROID_VEL = 8
SHIP_WIDTH, SHIP_HEIGHT = 40, 40
ASTROID_WIDTH, ASTROID_HEIGHT = 100, 100


MUSIC.play(-1)

ASTROID_HIT = pygame.USEREVENT+1


Ship_image = pygame.image.load(os.path.join('gameItems', 'Ship.png'))
Ship = pygame.transform.rotate(pygame.transform.scale(Ship_image, (SHIP_WIDTH, SHIP_HEIGHT)), 180)

astroid_image = pygame.image.load(os.path.join('gameItems', 'astroid.png'))
astroid = pygame.transform.scale(astroid_image, (ASTROID_HEIGHT, ASTROID_WIDTH))

Space = pygame.image.load(os.path.join('gameItems', 'space.png'))


def astroidShower(Astroid_Hitbox, Num_Astroids, Ship_Hitbox):
    for Astroid_Hitbox in Num_Astroids:
        Astroid_Hitbox.y += ASTROID_VEL

        if Astroid_Hitbox.y > HEIGHT:
            Num_Astroids.remove(Astroid_Hitbox)
        if Astroid_Hitbox.colliderect(Ship_Hitbox):
            pygame.event.post(pygame.event.Event(ASTROID_HIT))


def shipMovement(keys, Ship_Hitbox):

    if keys[pygame.K_DOWN] and Ship_Hitbox.y + VEL < HEIGHT - SHIP_HEIGHT:
        Ship_Hitbox.y += VEL
    if keys[pygame.K_UP] and Ship_Hitbox.y > 0:
        Ship_Hitbox.y -= VEL
    if keys[pygame.K_LEFT] and Ship_Hitbox.x > 0:
        Ship_Hitbox.x -= VEL
    if keys[pygame.K_RIGHT] and Ship_Hitbox.x < WIDTH - SHIP_WIDTH:
        Ship_Hitbox.x += VEL
    # if keys[pygame.K_SPACE]:
        # LAUGH.play()


def drawGameOver(Death_Time):
    WIN.fill(RED)
    GameOver_Text = GAMEOVER_FONT.render("GAME OVER", 1, BLACK)
    WIN.blit(GameOver_Text, (WIDTH/2 - GameOver_Text.get_width()/2, HEIGHT/2 - GameOver_Text.get_height()/2))

    DeathTime_Text = GAMEOVER_FONT.render("You survived " + str(Death_Time) + " Seconds", 1, BLACK)
    WIN.blit(DeathTime_Text, (WIDTH / 2 - DeathTime_Text.get_width()/2, HEIGHT / 2 + GameOver_Text.get_height()))
    pygame.display.update()

    pygame.time.delay(2000)


def drawWindow(Ship_Hitbox, Astroid_Hitbox, Num_Astroids, seconds):

    WIN.blit(Space, (0, 0))
    WIN.blit(Ship, (Ship_Hitbox.x, Ship_Hitbox.y))

    for Astroid_Hitbox in Num_Astroids:
        WIN.blit(astroid, (Astroid_Hitbox.x, Astroid_Hitbox.y))

    Seconds_Text = SECONDS_FONT.render("TIME: " + str(seconds), 1, WHITE)
    WIN.blit(Seconds_Text, (10, 10))

    pygame.display.update()


def main():
    Ship_Hitbox = pygame.Rect(300, HEIGHT - SHIP_HEIGHT-5, SHIP_WIDTH, SHIP_HEIGHT)
    start_ticks = pygame.time.get_ticks()
    Death_Time = 0

    Num_Astroids = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == ASTROID_HIT:   # player is hit and loses
                Death_Time = seconds
                DEATH_SOUND.play()
                # AHH.play()

        if len(Num_Astroids) < MAX_ASTOIRDS:
            Astroid_Hitbox = pygame.Rect(random.randint(0, WIDTH-ASTROID_WIDTH),
                                         random.randint(-HEIGHT, -ASTROID_HEIGHT), ASTROID_WIDTH-20, ASTROID_HEIGHT-20)
            Num_Astroids.append(Astroid_Hitbox)

            if Death_Time > 0:
                drawGameOver(Death_Time)
                main()

        # pygame.time.get_ticks
        keys_pressed = pygame.key.get_pressed()
        astroidShower(Astroid_Hitbox, Num_Astroids, Ship_Hitbox)
        shipMovement(keys_pressed, Ship_Hitbox)
        drawWindow(Ship_Hitbox, Astroid_Hitbox, Num_Astroids, seconds)


if __name__ == "__main__":
    main()
