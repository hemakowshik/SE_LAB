# Real-Time Flappy Bird Clone (Updated & Fixed Version)

This folder contains the completed and refined version of the Flappy Bird project meeting all lab requirements (Tasks 1 to 4) plus interactive start screen and screen maximize support.

---

## What Was Added & Enhanced

### 1. Start Screen with "START GAME" Trigger
* When you launch the game, it opens into an attractive **Title Screen** instead of immediately dropping the bird into gameplay.
* The bird hovers gently with an idle animation while waiting for the player.
* Features:
  * **[ START GAME ] Button**: Click the button or press <kbd>Space</kbd> / <kbd>Enter</kbd> to begin.
  * **Difficulty Selector**: Select **Easy**, **Medium**, or **Hard** before starting by clicking the buttons or pressing <kbd>1</kbd>, <kbd>2</kbd>, or <kbd>3</kbd>.

### 2. Window Resizing & Screen Maximize Support
* Configured with `pygame.RESIZABLE`, enabling the standard **Maximize Button** on the Windows window title bar.
* Maximizing or resizing dynamically scales the game graphics smoothly (`pygame.transform.smoothscale`) while preserving the 500x700 aspect ratio with clean letterboxing borders.
* Includes accurate **mouse coordinate translation**, ensuring that button clicks, flaps, and UI interactions align accurately regardless of how large the window is expanded.
* Shortcut: Press <kbd>F11</kbd> or <kbd>Alt</kbd> + <kbd>Enter</kbd> anytime to toggle borderless fullscreen / maximize.

### 3. Task 1: Refined Collision Detection
* Replaced flawed point-only collision (`collidepoint(self.bird.center())`) with exact **Circle-to-AABB (Axis-Aligned Bounding Box)** collision detection.
* Tests whether $(\Delta x^2 + \Delta y^2) \le r^2$ against pipe rectangles, preventing all edge-clipping.
* Ceiling and ground collisions strictly check the full radius of the bird.

### 4. Task 2: In-Game Game Over Screen
* Cleanly renders a semi-transparent modal card on the screen:
  * Prominent **GAME OVER** title
  * **Final Score** and **Best Session Score**
  * Interactive replay and difficulty selection menu

### 5. Task 3: Replay & Difficulty System
* On Game Over, players can immediately replay with any difficulty:
  * **[1] Easy**: Pipe Speed 3, Gap 185px, Pipe Spawn Interval 105 frames
  * **[2] Medium**: Pipe Speed 4, Gap 150px, Pipe Spawn Interval 90 frames
  * **[3] Hard**: Pipe Speed 6, Gap 125px, Pipe Spawn Interval 70 frames
  * **[SPACE] / [R]**: Quick restart using the current difficulty
  * **[Q] / [ESC]**: Exit the game cleanly

### 6. Task 4: Sound Feedback
* Integrated retro 8-bit sound effects for:
  * **Flap**: Upward sweep when jumping
  * **Score**: Pleasant two-tone chime when clearing a pipe
  * **Hit / Die**: Low impact thump upon collision

---

## How to Run

1. Open PowerShell or Command Prompt.
2. Navigate to this directory:
   ```powershell
   cd C:\SE_LAB4\flappybird-updated
   ```
3. Run the game:
   ```powershell
   python main.py
   ```

## Controls
* **Start Screen**: Click **START GAME** or press <kbd>Space</kbd> / <kbd>Enter</kbd>
* **Difficulty Selection**: Keys <kbd>1</kbd>, <kbd>2</kbd>, <kbd>3</kbd> or click the difficulty buttons
* **Flap**: <kbd>Spacebar</kbd> or <kbd>Left Mouse Click</kbd>
* **Maximize Screen**: Click the **Maximize** button on the window title bar, or press <kbd>F11</kbd>
* **Game Over Screen**: <kbd>1</kbd> / <kbd>2</kbd> / <kbd>3</kbd> for difficulty replay, <kbd>Space</kbd> / <kbd>R</kbd> for quick restart, <kbd>Q</kbd> to quit
