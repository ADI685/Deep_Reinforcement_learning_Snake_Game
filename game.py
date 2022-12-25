import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

BLOCK_SIZE = 20
SPEED = 40

class SnakeGameAI:
    def __init__(self, w=800, h=600):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.direction = Direction.UP
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self.food_pos()
        self.frame_iteration = 0

    def food_pos(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self.food_pos()

    def play_step(self, action):
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()       
        self.move(action) 
        self.snake.insert(0, self.head)       
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        if self.head == self.food:
            self.score += 1
            reward = 10
            self.food_pos()
        else:
            self.snake.pop()
        self.frame_render()
        self.clock.tick(SPEED)
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        if pt in self.snake[1:]:
            return True

        return False
    def move(self, action):
        all_direction = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        ind = all_direction.index(self.direction)
        if np.array_equal(action, [1, 0, 0]):
            newdir = all_direction[ind]
        elif np.array_equal(action, [0, 1, 0]):
            next_ind = (ind + 1) % 4
            newdir = all_direction[next_ind]
        else:
            next_ind = (ind - 1) % 4
            newdir = all_direction[next_ind]
        self.direction = newdir
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        self.head = Point(x, y)
    def frame_render(self):
        self.display.fill((255, 255, 255))
        for pt in self.snake:
            pygame.draw.rect(self.display, (180, 250, 25), pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.circle(self.display, (250, 250, 35),(self.snake[0].x+BLOCK_SIZE//2, self.snake[0].y+BLOCK_SIZE//2), BLOCK_SIZE//4,100 )

        pygame.draw.circle(self.display, (200,0,0),(self.food.x+BLOCK_SIZE//2, self.food.y+BLOCK_SIZE//2), BLOCK_SIZE//2,100 )
        text = font.render("Score: " + str(self.score), True, (0,0,0))
        self.display.blit(text, [0, 0])
        pygame.display.flip()