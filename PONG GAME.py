import pygame
import random

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 450
BLACK = (0, 0, 0)
LIGHT_GREY = (200, 200, 200)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong Game')
clock = pygame.time.Clock()
last_scorer = None
lives1 = 5
lives2 = 5

class Ball(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(LIGHT_GREY)  # Use a surface instead of loading an image
        self.rect = self.image.get_rect()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset()

    def reset(self):
        global last_scorer
        if last_scorer == 'Player 1':

            self.rect.center = (self.screen_width - 20, random.randint(0, self.screen_height))
        elif last_scorer == 'Player 2':

            self.rect.center = (20, random.randint(0, self.screen_height))

        self.x_speed = random.choice([-4,-3,-2, -1, 1, 2, 3])
        self.y_speed = random.choice([-4,-3,-2, -1, 1, 2, 3])
        last_scorer = None  # Reset last_scorer after setting the ball's position

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        if self.rect.right < 0:
            self.rect.left = self.screen_width
        elif self.rect.left > self.screen_width:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = self.screen_height
        elif self.rect.top > self.screen_height:
            self.rect.bottom = 0

class Player1Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((9, 130))
        self.image.fill(LIGHT_GREY)
        self.rect = self.image.get_rect()
        self.rect.center = (20, SCREEN_HEIGHT // 2)
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed


        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Player2Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((9, 130))
        self.image.fill(LIGHT_GREY)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2)  # Corrected initial position
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed


        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

balli = Ball(SCREEN_WIDTH, SCREEN_HEIGHT)
player1_paddle = Player1Paddle()
player2_paddle = Player2Paddle()

sprites = pygame.sprite.Group()
sprites.add(balli, player1_paddle, player2_paddle)

def collision(balli, player1_paddle, player2_paddle, score1=0, score2=0):
    global last_scorer, lives1, lives2
    for ball in balli:
        if pygame.sprite.collide_rect(ball, player1_paddle) and last_scorer != 'Player 1':
            score1 += 1
            lives2 -= 1
            if lives1 == 0:
                return True, score1, score2  # Player 1 loses, game over
            last_scorer = 'Player 1'
        if pygame.sprite.collide_rect(ball, player2_paddle) and last_scorer != 'Player 2':
            score2 += 1
            lives1 -= 1
            if lives2 == 0:
                return True, score1, score2  # Player 2 loses, game over
            last_scorer = 'Player 2'
    return False, score1, score2

font = pygame.font.Font(None, 36)  # Load a default font with size 36
score1 = 0  # Initialize Player 1's score
score2 = 0  # Initialize Player 2's score

running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        player1_paddle.move()
        player2_paddle.move()


        game_over, score1, score2 = collision([balli], player1_paddle, player2_paddle, score1, score2)

        if not game_over:
            score1_text = font.render("Player 1 Score: " + str(score1), True, (255, 255, 255))
            score2_text = font.render("Player 2 Score: " + str(score2), True, (255, 255, 255))

            screen.fill(BLACK)
            sprites.draw(screen)
            balli.update()
            screen.blit(balli.image, balli.rect)
            screen.blit(score1_text, (10, 10))
            screen.blit(score2_text, (SCREEN_WIDTH - 200, 10))
        else:
            game_over_text = font.render("Game Over!", True, (255, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

    else:

        restart_text = font.render("Press 'Space Bar' to restart", True, (255, 255, 255))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 50))
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            # Restart the game
            score1 = 0
            score2 = 0
            lives1 = 5
            lives2 = 5
            balli.reset()
            game_over = False

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
