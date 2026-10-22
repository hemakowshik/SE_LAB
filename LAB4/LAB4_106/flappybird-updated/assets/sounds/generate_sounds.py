import os
import wave
import struct
import math

def write_wav(filename, samples, sample_rate=44100):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)        # Mono
        wf.setsampwidth(2)       # 16-bit
        wf.setframerate(sample_rate)
        buffer = bytearray()
        for sample in samples:
            clamped = max(-1.0, min(1.0, sample))
            ival = int(clamped * 32767)
            buffer += struct.pack("<h", ival)
        wf.writeframes(buffer)

def generate_all_sounds(target_dir):
    os.makedirs(target_dir, exist_ok=True)
    sr = 44100

    # 1. Flap sound: upward chirp (300Hz to 650Hz over 0.12s)
    dur_flap = 0.12
    n_flap = int(sr * dur_flap)
    flap_samples = []
    for i in range(n_flap):
        t = i / sr
        progress = t / dur_flap
        freq = 320 + (680 - 320) * (progress ** 1.3)
        # decaying envelope
        env = (1.0 - progress) ** 0.8
        # slight harmonic to make it punchy
        val = 0.7 * math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(4 * math.pi * freq * t)
        flap_samples.append(val * env)
    write_wav(os.path.join(target_dir, "flap.wav"), flap_samples, sr)

    # 2. Score sound: bright two-tone chime (587.33Hz (D5) for 0.08s then 880Hz (A5) for 0.14s)
    dur_score = 0.22
    n_score = int(sr * dur_score)
    score_samples = []
    t_split = 0.08
    for i in range(n_score):
        t = i / sr
        if t < t_split:
            freq = 587.33
            env = 1.0 - (t / t_split) * 0.3
        else:
            freq = 880.0
            t_rem = (t - t_split) / (dur_score - t_split)
            env = 1.0 - t_rem
        val = 0.8 * math.sin(2 * math.pi * freq * t) + 0.2 * math.sin(2 * math.pi * freq * 2 * t)
        score_samples.append(val * env)
    write_wav(os.path.join(target_dir, "score.wav"), score_samples, sr)

    # 3. Hit / Die sound: downward pitch punch with distortion (260Hz down to 50Hz over 0.28s)
    dur_hit = 0.28
    n_hit = int(sr * dur_hit)
    hit_samples = []
    for i in range(n_hit):
        t = i / sr
        progress = t / dur_hit
        freq = max(40.0, 260.0 * ((1.0 - progress) ** 1.8))
        env = (1.0 - progress) ** 0.5
        # slightly square-distorted wave for impactful thud
        raw = math.sin(2 * math.pi * freq * t)
        distorted = math.copysign(min(1.0, abs(raw) * 1.5), raw)
        hit_samples.append(distorted * env * 0.85)
    write_wav(os.path.join(target_dir, "hit.wav"), hit_samples, sr)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    generate_all_sounds(current_dir)
    print("Sound effects successfully generated in:", current_dir)
