import pygame
import random

class Pipe:
    def __init__(self, x, screen_height, gap=150, width=70, speed=4):
        self.x = x
        self.width = width
        self.gap = gap
        self.speed = speed
        self.screen_height = screen_height
        # Ensure gap position gives fair clearance from top and ground
        min_top = 70
        max_top = max(min_top, screen_height - gap - 90)
        self.gap_y = random.randint(min_top, max_top)
        self.scored = False

    def move(self):
        self.x -= self.speed

    def off_screen(self):
        return self.x + self.width < 0

    def top_rect(self):
        return pygame.Rect(int(self.x), 0, int(self.width), int(self.gap_y))

    def bottom_rect(self):
        bottom_y = self.gap_y + self.gap
        return pygame.Rect(int(self.x), int(bottom_y), int(self.width), int(self.screen_height - bottom_y))

    def render(self, screen):
        PIPE_GREEN = (46, 178, 62)
        PIPE_DARK = (28, 122, 40)
        PIPE_LIGHT = (110, 220, 120)

        top = self.top_rect()
        bot = self.bottom_rect()

        # Draw main pipe shafts
        pygame.draw.rect(screen, PIPE_GREEN, top)
        pygame.draw.rect(screen, PIPE_DARK, top, 2)
        pygame.draw.rect(screen, PIPE_GREEN, bot)
        pygame.draw.rect(screen, PIPE_DARK, bot, 2)

        # Highlight streak on pipe shaft
        pygame.draw.line(screen, PIPE_LIGHT, (self.x + 8, top.top), (self.x + 8, top.bottom - 4), 3)
        pygame.draw.line(screen, PIPE_LIGHT, (self.x + 8, bot.top + 4), (self.x + 8, bot.bottom), 3)

        # Pipe end caps (collar)
        cap_h = 22
        cap_extra = 4
        # Top collar
        top_cap_rect = pygame.Rect(self.x - cap_extra, top.bottom - cap_h, self.width + cap_extra * 2, cap_h)
        pygame.draw.rect(screen, PIPE_GREEN, top_cap_rect)
        pygame.draw.rect(screen, PIPE_DARK, top_cap_rect, 2)
        pygame.draw.line(screen, PIPE_LIGHT, (top_cap_rect.left + 8, top_cap_rect.top + 2), (top_cap_rect.left + 8, top_cap_rect.bottom - 2), 3)

        # Bottom collar
        bot_cap_rect = pygame.Rect(self.x - cap_extra, bot.top, self.width + cap_extra * 2, cap_h)
        pygame.draw.rect(screen, PIPE_GREEN, bot_cap_rect)
        pygame.draw.rect(screen, PIPE_DARK, bot_cap_rect, 2)
        pygame.draw.line(screen, PIPE_LIGHT, (bot_cap_rect.left + 8, bot_cap_rect.top + 2), (bot_cap_rect.left + 8, bot_cap_rect.bottom - 2), 3)
