import os
import pygame

class SoundManager:
    """
    Manages sound effects for the Flappy Bird game.
    Safely initializes pygame mixer and plays sound effects.
    """
    def __init__(self):
        self.enabled = False
        self.sounds = {}

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
            self.enabled = True
        except Exception as e:
            print(f"[SoundManager] Audio initialization warning: {e}. Running in silent mode.")
            self.enabled = False
            return

        # Base sound directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sound_dir = os.path.abspath(os.path.join(current_dir, "..", "assets", "sounds"))

        # Verify sounds exist, otherwise auto-generate
        required = ["flap.wav", "score.wav", "hit.wav"]
        missing = [name for name in required if not os.path.exists(os.path.join(sound_dir, name))]
        if missing:
            try:
                from assets.sounds.generate_sounds import generate_all_sounds
                generate_all_sounds(sound_dir)
            except Exception as e:
                print(f"[SoundManager] Could not auto-generate sounds: {e}")

        for name in required:
            filepath = os.path.join(sound_dir, name)
            if os.path.exists(filepath):
                try:
                    sound = pygame.mixer.Sound(filepath)
                    sound.set_volume(0.6)
                    self.sounds[name] = sound
                except Exception as e:
                    print(f"[SoundManager] Error loading {name}: {e}")

    def play_flap(self):
        if self.enabled and "flap.wav" in self.sounds:
            try:
                self.sounds["flap.wav"].play()
            except Exception:
                pass

    def play_score(self):
        if self.enabled and "score.wav" in self.sounds:
            try:
                self.sounds["score.wav"].play()
            except Exception:
                pass

    def play_die(self):
        if self.enabled and "hit.wav" in self.sounds:
            try:
                self.sounds["hit.wav"].play()
            except Exception:
                pass
