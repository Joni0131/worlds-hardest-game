import pygame

class Player:
    def __init__(self, x, y, width, height, vel=5, color=(255,0,0), deaths = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.color = color
        self.deaths = deaths

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 100 + self.width:
            self.x -= self.vel
        if keys[pygame.K_RIGHT] and self.x < 630:
            self.x += self.vel
        if keys[pygame.K_DOWN] and self.y < 420:
            self.y += self.vel
        if keys[pygame.K_UP] and self.y > 150 + self.height:
            self.y -= self.vel

    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,0), (self.x-2, self.y-2, self.width+4, self.height+4))
        return pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def reset(self):
        self.x = 150
        self.y = 390
