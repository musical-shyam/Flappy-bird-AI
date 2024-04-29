# will contain Bird, Pipe, Ground, Background, Score classes
import pygame
import random
import brain # temp name for the neural network/genetic algorithm import

WINDOW_WIDTH = 550
WINDOW_HEIGHT = 550
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird AI")

class Ground:
    ground_level = 500

    def __init__(self, win_width):
        self.x, self.y = 0, Ground.ground_level
        self.rect = pygame.Rect(self.x, self.y, win_width, 5)

    def draw(self, window):
        pygame.draw.rect(window, (92, 58, 8), self.rect)


class Pipes:
    width = 15
    opening = 100 # DEFAULT 100, increase to make the gap bigger

    def __init__(self, win_width):
        self.x = win_width
        self.bottom_height = random.randint(10, 300)
        self.top_height = Ground.ground_level - self.bottom_height - self.opening
        self.bottom_rect, self.top_rect = pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0)
        self.passed = False
        self.off_screen = False

    def draw(self, window): # draws the pipe twice, bottom half then top half with the opening spacing the two pipes
        self.bottom_rect = pygame.Rect(self.x, Ground.ground_level - self.bottom_height, self.width, self.bottom_height)
        pygame.draw.rect(window, (6, 128, 39), self.bottom_rect)

        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        pygame.draw.rect(window, (6, 128, 39), self.top_rect)

    def update(self): # function for pipes to move across the GUI and determine whether they were passed or not (to remove themselves from screen)
        self.x -= 1
        if self.x + Pipes.width <= 50:
            self.passed = True
        if self.x <= -self.width:
            self.off_screen = True

ground = Ground(WINDOW_WIDTH)
pipes = []

class Player:
    def __init__(self):
        # Bird
        self.x, self.y = 50, 200
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
        self.vel = 0
        self.flap = False
        self.alive = True
        self.lifespan = 0

        # AI
        self.decision = None
        self.vision = [0.5, 1, 0.5]
        self.fitness = 0
        self.inputs = 3
        self.brain = brain.Brain(self.inputs)
        self.brain.generate_net()

    # Game related functions
    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def ground_collision(self, ground):
        return pygame.Rect.colliderect(self.rect, ground)

    def sky_collision(self):
        return bool(self.rect.y < 30)

    def pipe_collision(self):
        for p in pipes:
            return pygame.Rect.colliderect(self.rect, p.top_rect) or \
                   pygame.Rect.colliderect(self.rect, p.bottom_rect)

    def update(self, ground):
        if not (self.ground_collision(ground) or self.pipe_collision()):
            # Gravity
            self.vel += 0.25
            self.rect.y += self.vel
            if self.vel > 5:
                self.vel = 5
            # Increment lifespan
            self.lifespan += 1
        else:
            self.alive = False
            self.flap = False
            self.vel = 0

    def bird_flap(self):
        if not self.flap and not self.sky_collision():
            self.flap = True
            self.vel = -5
        if self.vel >= 3:
            self.flap = False

    @staticmethod
    def closest_pipe():
        for p in pipes:
            if not p.passed:
                return p

    # AI related functions
    def look(self):
        if pipes:

            # Line to top pipe
            self.vision[0] = max(0, self.rect.center[1] - self.closest_pipe().top_rect.bottom) / 500
            #pygame.draw.line(window, self.color, self.rect.center,
            #                (self.rect.center[0], pipes[0].top_rect.bottom))

            # Line to mid pipe
            self.vision[1] = max(0, self.closest_pipe().x - self.rect.center[0]) / 500
            #pygame.draw.line(window, self.color, self.rect.center,
            #                 (pipes[0].x, self.rect.center[1]))

            # Line to bottom pipe
            self.vision[2] = max(0, self.closest_pipe().bottom_rect.top - self.rect.center[1]) / 500
            #pygame.draw.line(window, self.color, self.rect.center,
            #                 (self.rect.center[0], pipes[0].bottom_rect.top))

    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision > 0.73:
            self.bird_flap()

    def calculate_fitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone = Player()
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_net()
        return clone
