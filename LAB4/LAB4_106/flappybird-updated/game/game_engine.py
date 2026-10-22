import math
import pygame
from .bird import Bird
from .pipe import Pipe
from .sound_manager import SoundManager

# Palette
SKY_BLUE = (135, 206, 235)
GROUND_BROWN = (222, 184, 135)
GRASS_GREEN = (115, 190, 70)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GOLD = (255, 215, 0)
DARK_GRAY = (40, 40, 40)
OVERLAY_BG = (15, 25, 35, 210)
BTN_GREEN = (46, 180, 80)
BTN_GREEN_HOVER = (60, 215, 100)

DIFFICULTIES = {
    "Easy": {"speed": 3, "gap": 185, "interval": 105, "key": pygame.K_1},
    "Medium": {"speed": 4, "gap": 150, "interval": 90, "key": pygame.K_2},
    "Hard": {"speed": 6, "gap": 125, "interval": 70, "key": pygame.K_3},
}

STATE_START = "START"
STATE_PLAYING = "PLAYING"
STATE_GAME_OVER = "GAME_OVER"

STUDENT_SRN = "PES1UG24AM106"

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ground_y = height - 50

        # Ensure pygame font is initialized
        if not pygame.font.get_init():
            pygame.font.init()

        # Sounds
        self.sound = SoundManager()

        # Difficulty configuration
        self.current_difficulty = "Medium"
        self._apply_difficulty(self.current_difficulty)

        # Entities
        self.bird = Bird(width // 4, height // 2)
        self.pipes = []
        self._spawn_timer = 0
        self._hover_tick = 0

        # States: START -> PLAYING -> GAME_OVER
        self.state = STATE_START
        self.game_over = False
        self.should_quit = False

        # Scores
        self.score = 0
        self.high_score = 0

        # UI interactive buttons
        self.start_btn_rect = pygame.Rect(140, 405, 220, 56)
        self.diff_btn_rects = {
            "Easy": pygame.Rect(75, 345, 105, 38),
            "Medium": pygame.Rect(195, 345, 110, 38),
            "Hard": pygame.Rect(320, 345, 105, 38)
        }

        # Fonts
        self.font_score = pygame.font.SysFont("Arial", 32, bold=True)
        self.font_title = pygame.font.SysFont("Arial", 48, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_btn = pygame.font.SysFont("Arial", 26, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 18)

    def _apply_difficulty(self, diff_name):
        config = DIFFICULTIES.get(diff_name, DIFFICULTIES["Medium"])
        self.current_difficulty = diff_name
        self.pipe_speed = config["speed"]
        self.pipe_gap = config["gap"]
        self.pipe_interval = config["interval"]

    def start_game(self):
        """Starts a new round from the start screen or replay."""
        self.state = STATE_PLAYING
        self.game_over = False
        self.bird.reset()
        self.bird.y = self.ground_y // 2
        self.bird.flap()
        self.pipes = [Pipe(self.width + 80, self.ground_y, gap=self.pipe_gap, speed=self.pipe_speed)]
        self._spawn_timer = 0
        self.score = 0
        self.sound.play_flap()

    def reset(self, difficulty="Medium"):
        """Task 3: Resets the game state cleanly with the selected difficulty."""
        self._apply_difficulty(difficulty)
        self.start_game()

    def handle_event(self, event, mouse_pos=None):
        m_pos = mouse_pos if mouse_pos is not None else getattr(event, "pos", (0, 0))

        if event.type == pygame.QUIT:
            self.should_quit = True
            return

        # 1. Start Screen Event Handling
        if self.state == STATE_START:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self._apply_difficulty("Easy")
                elif event.key == pygame.K_2:
                    self._apply_difficulty("Medium")
                elif event.key == pygame.K_3:
                    self._apply_difficulty("Hard")
                elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    self.start_game()
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    self.should_quit = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check difficulty button clicks
                clicked_diff = False
                for diff_name, rect in self.diff_btn_rects.items():
                    if rect.collidepoint(m_pos):
                        self._apply_difficulty(diff_name)
                        clicked_diff = True
                        break

                # If start button or general area clicked, begin game
                if not clicked_diff:
                    if self.start_btn_rect.collidepoint(m_pos) or m_pos[1] > 200:
                        self.start_game()

        # 2. Playing State Event Handling
        elif self.state == STATE_PLAYING:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or \
               (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                self.bird.flap()
                self.sound.play_flap()

        # 3. Game Over State Event Handling
        elif self.state == STATE_GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.reset("Easy")
                elif event.key == pygame.K_2:
                    self.reset("Medium")
                elif event.key == pygame.K_3:
                    self.reset("Hard")
                elif event.key in (pygame.K_SPACE, pygame.K_r):
                    self.reset(self.current_difficulty)
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    self.should_quit = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Clicking screen restarts
                self.reset(self.current_difficulty)

    def handle_input(self):
        pass

    def trigger_game_over(self):
        """Handles collision event, high score tracking, and death sound."""
        if self.state == STATE_PLAYING:
            self.state = STATE_GAME_OVER
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
            self.sound.play_die()
            print(f"Game Over! Final Score: {self.score} (Difficulty: {self.current_difficulty})")

    def update(self):
        if self.state == STATE_START:
            # Idle hover animation on start screen
            self._hover_tick += 1
            self.bird.y = (self.ground_y // 2 - 30) + int(math.sin(self._hover_tick * 0.08) * 8)
            return

        if self.state == STATE_GAME_OVER:
            return

        # Update bird physics
        self.bird.update()

        # Task 1: Refined Boundary Collision with ceiling and ground
        if (self.bird.y - self.bird.radius <= 0) or (self.bird.y + self.bird.radius >= self.ground_y):
            self.trigger_game_over()
            return

        # Pipe spawning
        self._spawn_timer += 1
        if self._spawn_timer >= self.pipe_interval:
            self._spawn_timer = 0
            self.pipes.append(Pipe(self.width, self.ground_y, gap=self.pipe_gap, speed=self.pipe_speed))

        # Pipe updates & collision
        for pipe in self.pipes:
            pipe.move()

            # Task 1: Refined exact circle-to-box collision detection
            if self.bird.collides_with_rect(pipe.top_rect()) or self.bird.collides_with_rect(pipe.bottom_rect()):
                self.trigger_game_over()
                return

            # Scoring: trigger when bird safely passes pipe
            if not pipe.scored and (pipe.x + pipe.width < self.bird.x):
                pipe.scored = True
                self.score += 1
                self.sound.play_score()

        # Remove off-screen pipes
        self.pipes = [p for p in self.pipes if not p.off_screen()]

    def render(self, screen, mouse_pos=(0, 0)):
        # 1. Sky Background
        screen.fill(SKY_BLUE)

        # 2. Pipes (in playing or game over)
        if self.state != STATE_START:
            for pipe in self.pipes:
                pipe.render(screen)

        # 3. Ground
        ground_rect = pygame.Rect(0, self.ground_y, self.width, self.height - self.ground_y)
        pygame.draw.rect(screen, GROUND_BROWN, ground_rect)
        pygame.draw.rect(screen, GRASS_GREEN, (0, self.ground_y, self.width, 10))
        pygame.draw.line(screen, (80, 150, 40), (0, self.ground_y), (self.width, self.ground_y), 2)

        # 4. Bird
        self.bird.render(screen)

        # 5. Render Scene According to State
        if self.state == STATE_START:
            self._render_start_screen(screen, mouse_pos)
        elif self.state == STATE_PLAYING:
            self._render_hud(screen)
        elif self.state == STATE_GAME_OVER:
            self._render_hud(screen)
            self._render_game_over_screen(screen)

    def _render_hud(self, screen):
        score_surf = self.font_score.render(f"Score: {self.score}", True, WHITE)
        shadow_surf = self.font_score.render(f"Score: {self.score}", True, BLACK)
        screen.blit(shadow_surf, (18, 16))
        screen.blit(score_surf, (16, 14))

        diff_surf = self.font_small.render(f"Mode: {self.current_difficulty}", True, WHITE)
        screen.blit(diff_surf, (self.width - diff_surf.get_width() - 16, 18))

        srn_surf = self.font_small.render(f"SRN: {STUDENT_SRN}", True, (210, 230, 255))
        screen.blit(srn_surf, (self.width - srn_surf.get_width() - 16, 40))

    def _render_start_screen(self, screen, mouse_pos):
        # Title with drop shadow
        title_text = "FLAPPY BIRD"
        shadow = self.font_title.render(title_text, True, (40, 60, 80))
        title = self.font_title.render(title_text, True, GOLD)
        tx = (self.width - title.get_width()) // 2
        screen.blit(shadow, (tx + 3, 103))
        screen.blit(title, (tx, 100))

        subtitle = self.font_medium.render("Enhanced Pygame Edition", True, WHITE)
        screen.blit(subtitle, ((self.width - subtitle.get_width()) // 2, 160))

        srn_badge = self.font_small.render(f"Candidate SRN: {STUDENT_SRN}", True, (220, 235, 255))
        screen.blit(srn_badge, ((self.width - srn_badge.get_width()) // 2, 192))

        # Difficulty Selector Section
        diff_label = self.font_small.render("Select Difficulty:", True, (230, 240, 255))
        screen.blit(diff_label, ((self.width - diff_label.get_width()) // 2, 315))

        for diff_name, rect in self.diff_btn_rects.items():
            is_active = (diff_name == self.current_difficulty)
            is_hover = rect.collidepoint(mouse_pos)
            bg_col = (40, 110, 180) if is_active else ((60, 80, 105) if is_hover else (35, 45, 60))
            border_col = GOLD if is_active else (150, 170, 190)

            pygame.draw.rect(screen, bg_col, rect, border_radius=8)
            pygame.draw.rect(screen, border_col, rect, width=2 if is_active else 1, border_radius=8)

            txt_col = GOLD if is_active else WHITE
            label = self.font_small.render(diff_name, True, txt_col)
            screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))

        # Start Button
        is_btn_hover = self.start_btn_rect.collidepoint(mouse_pos)
        btn_col = BTN_GREEN_HOVER if is_btn_hover else BTN_GREEN
        pygame.draw.rect(screen, btn_col, self.start_btn_rect, border_radius=14)
        pygame.draw.rect(screen, WHITE, self.start_btn_rect, width=2, border_radius=14)

        btn_txt = self.font_btn.render("START GAME", True, WHITE)
        screen.blit(btn_txt, (self.start_btn_rect.centerx - btn_txt.get_width() // 2, self.start_btn_rect.centery - btn_txt.get_height() // 2))

        # Instructions
        hint1 = self.font_small.render("Press [SPACE] or Click to Start", True, (255, 255, 255))
        hint2 = self.font_small.render("Tip: Maximize window or press [F11] for Fullscreen", True, (210, 230, 250))
        screen.blit(hint1, ((self.width - hint1.get_width()) // 2, 480))
        screen.blit(hint2, ((self.width - hint2.get_width()) // 2, 515))

    def _render_game_over_screen(self, screen):
        # Translucent dark backdrop
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill(OVERLAY_BG)
        screen.blit(overlay, (0, 0))

        # Central Modal Card
        card_w, card_h = 400, 380
        card_x = (self.width - card_w) // 2
        card_y = (self.height - card_h) // 2 - 20
        card_rect = pygame.Rect(card_x, card_y, card_w, card_h)

        pygame.draw.rect(screen, (35, 45, 60), card_rect, border_radius=16)
        pygame.draw.rect(screen, GOLD, card_rect, width=3, border_radius=16)

        # Title: GAME OVER
        title = self.font_title.render("GAME OVER", True, (255, 80, 80))
        screen.blit(title, (self.width // 2 - title.get_width() // 2, card_y + 24))

        # Scores
        score_txt = self.font_medium.render(f"Final Score:  {self.score}", True, WHITE)
        best_txt = self.font_medium.render(f"Best Score:   {self.high_score}", True, GOLD)
        screen.blit(score_txt, (self.width // 2 - score_txt.get_width() // 2, card_y + 88))
        screen.blit(best_txt, (self.width // 2 - best_txt.get_width() // 2, card_y + 122))

        # Divider line
        pygame.draw.line(screen, (80, 100, 125), (card_x + 30, card_y + 162), (card_x + card_w - 30, card_y + 162), 2)

        # Difficulty Selection Header
        choose_txt = self.font_medium.render("Choose Difficulty to Play:", True, (180, 220, 255))
        screen.blit(choose_txt, (self.width // 2 - choose_txt.get_width() // 2, card_y + 175))

        # Difficulty Options Buttons / Prompts
        diff_options = [
            ("[1] Easy", "Easy", (120, 240, 140)),
            ("[2] Medium", "Medium", (255, 215, 100)),
            ("[3] Hard", "Hard", (255, 120, 120))
        ]
        btn_y = card_y + 215
        for text, mode, color in diff_options:
            is_active = (mode == self.current_difficulty)
            indicator = " *ACTIVE*" if is_active else ""
            line_txt = self.font_small.render(f"{text}{indicator}", True, color if is_active else WHITE)
            screen.blit(line_txt, (card_x + 60, btn_y))
            btn_y += 28

        # Quick restart / quit prompt
        replay_txt = self.font_small.render("[SPACE / R] Quick Replay    [Q] Quit", True, (200, 210, 225))
        screen.blit(replay_txt, (self.width // 2 - replay_txt.get_width() // 2, card_y + card_h - 52))

        srn_footer = self.font_small.render(f"Candidate: {STUDENT_SRN}", True, (160, 185, 215))
        screen.blit(srn_footer, (self.width // 2 - srn_footer.get_width() // 2, card_y + card_h - 26))
