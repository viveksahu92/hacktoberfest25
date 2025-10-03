# 🚀 Stack Invaders

Welcome to **Stack Invaders**, a Space-Invaders inspired arcade shooter where every stage celebrates a different programming language. Blast through themed enemy waves, collect power-ups, and face bosses that weaponize iconic keywords!

## 🎮 Getting Started
- **Requirements:** Python 3.10+ and [Pygame](https://www.pygame.org/). Install dependencies with:
  ```bash
  pip install pygame
  ```
- **Run the game:**
  ```bash
  python main.py
  ```
- **Audio tip:** The game gracefully continues without sound if the mixer fails to initialize, but for the full experience ensure your system audio is available.

## 🕹️ How to Play
- **Move:** `←/→` or `A/D`
- **Shoot:** `SPACE`
- **Pause / Back:** `ESC`
- **Objective:** Clear successive enemy waves to summon each stage boss. Defeat the boss to advance to the next language-themed arena.

### ⭐ Power-Ups
- **Double Shot:** Temporarily fires an additional projectile with every attack.
- **Shield:** Surrounds the ship with a protective barrier against a hit.
- **Slow Time:** Slows incoming threats, giving breathing room to dodge.

### 🧠 Tips
- Keep moving horizontally to dodge barrages from bosses and spiraling projectiles.
- Time your shots to maximize damage windows when enemies change direction.
- Watch for keyword-labeled bullets—boss specials are faster and hit harder.

## 🛠️ Adding New Features
### 🆕 Add a New Stage
Stages live in the `STAGES` list within `main.py`. Duplicate an existing block and tweak:
1. `name`, `color`, and enemy grid (`enemy_rows`, `enemy_cols`).
2. Difficulty knobs (`enemy_speed`, `enemy_drop`, `enemy_shoot_chance`, `enemy_hp`, `player_projectile_speed`).
3. Boss definition (`boss` dict) with its HP, patterns, specials, and sprite.
Remember to supply any custom sprites or icons in `assets/`.

### 🎯 Custom Enemy Behavior
- **Enemy visuals:** Update the `enemy_sprite` path in a stage to use a custom image.
- **Boss patterns:** Extend `Boss.fire_pattern` to add new attack types. Create a new branch in the method and append projectiles to `enemy_bullets` for your pattern.

### 🧩 Power-Up Experiments
`Player.apply_power` handles boosts. Add new cases and spawn them from `PowerUp` or wave logic to prototype unique mechanics (e.g., rapid fire or score multipliers).

### 🗂️ Keep Things Organized
- Store assets under `assets/` to avoid load failures.
- Reuse helper functions `try_load_image` and `try_load_sound` to provide fallbacks when files are missing.

## 📦 Repository Structure
```
Stackinvaders/
├── assets/         # Sprites, audio, and sound effects
├── main.py         # Game loop, entities, stage logic
├── README_EN.md    # English guide
└── README_PT.md    # Guia em português
```

Have fun hacking on Stack Invaders, and share your favorite language boss combos! 🚀
