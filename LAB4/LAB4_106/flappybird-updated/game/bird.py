import pygame

class Bird:
    def __init__(self, x, y, radius=15):
        self.initial_x = x
        self.initial_y = y
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = 0
        self.gravity = 0.5
        self.flap_strength = -8
        self.max_fall_speed = 12

    def flap(self):
        self.velocity = self.flap_strength

    def update(self):
        self.velocity += self.gravity
        if self.velocity > self.max_fall_speed:
            self.velocity = self.max_fall_speed
        self.y += self.velocity

    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.velocity = 0

    def center(self):
        return (self.x, self.y)

    def rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2
        )

    def collides_with_rect(self, rect):
        """
        Task 1 Fix: Precise Circle-to-AABB (Axis-Aligned Bounding Box) collision detection.
        Calculates the closest point on the rectangle to the bird's center.
        If the squared Euclidean distance from the center to this closest point is
        less than or equal to the radius squared, a collision is detected.
        This completely eliminates edge-clipping bugs.
        """
        closest_x = max(rect.left, min(self.x, rect.right))
        closest_y = max(rect.top, min(self.y, rect.bottom))

        dx = self.x - closest_x
        dy = self.y - closest_y

        return (dx * dx + dy * dy) <= (self.radius * self.radius)

    def render(self, screen):
        bx = int(self.x)
        by = int(self.y)

        # Colors
        BIRD_YELLOW = (255, 215, 0)
        BIRD_OUTLINE = (180, 140, 0)
        WHITE = (255, 255, 255)
        BLACK = (20, 20, 20)
        ORANGE = (255, 120, 0)

        # Main Body Circle + outline
        pygame.draw.circle(screen, BIRD_OUTLINE, (bx, by), self.radius + 1)
        pygame.draw.circle(screen, BIRD_YELLOW, (bx, by), self.radius)

        # Wing
        wing_y_offset = -2 if self.velocity < 0 else 2
        pygame.draw.ellipse(screen, (240, 190, 0), (bx - 10, by + wing_y_offset, 12, 8))

        # Eye
        eye_x = bx + 5
        eye_y = by - 5
        pygame.draw.circle(screen, WHITE, (eye_x, eye_y), 4)
        pygame.draw.circle(screen, BLACK, (eye_x + 1, eye_y), 2)

        # Beak
        beak_pts = [
            (bx + 10, by - 2),
            (bx + 18, by + 2),
            (bx + 10, by + 6)
        ]
        pygame.draw.polygon(screen, ORANGE, beak_pts)
