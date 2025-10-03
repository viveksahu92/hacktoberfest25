import pygame
import random
import json
import math
from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional

BASE_WIDTH, BASE_HEIGHT = 900, 620
WIDTH, HEIGHT = BASE_WIDTH, BASE_HEIGHT
FPS = 60
DEFAULT_VOLUME = 0.6
VOLUME = DEFAULT_VOLUME
HUD_HEIGHT = 70

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Stack Invaders")
screen = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
clock = pygame.time.Clock()

try:
    pygame.mixer.init()
except Exception:
    pass

SOUND_EFFECTS = []

LANG = "en"

STRINGS = {
    "en": {
        "title": "STACK INVADERS",
        "subtitle": "Space-Invaders tribute with JS, Python, PHP and Java (boss)",
        "menu_start": "Start",
        "menu_controls": "Controls",
        "menu_language": "Language",
        "menu_volume": "Volume",
        "menu_quit": "Quit",
        "tip_nav": "Use ↑/↓ to navigate and ENTER to select",
        "controls_title": "Controls",
        "controls_move": "←/→ or A/D: move",
        "controls_shoot": "SPACE: shoot",
        "controls_esc": "ESC: pause / back",
        "controls_hint": "Defeat all to advance. Each stage has a boss.",
        "back": "Press ESC to go back",
        "volume_title": "Volume",
        "volume_tip": "Use ←/→ to adjust, ENTER or ESC to return",
        "paused": "Paused",
        "resume": "Resume",
        "restart": "Restart Stage",
        "quit_title": "Quit to Title",
        "game_over": "Game Over",
        "you_win": "You Win!",
        "stage": "Stage",
        "score": "Score",
        "lives": "Lives",
        "highscore": "Highscore",
        "language_title": "Language",
        "lang_en": "English",
        "lang_pt": "Português (Brasil)",
        "power_double": "Double Shot",
        "power_shield": "Shield",
        "power_slow": "Slow Time",
    },
    "pt_BR": {
        "title": "STACK INVADERS",
        "subtitle": "Tributo ao Space-Invaders com JS, Python, PHP e Java (boss)",
        "menu_start": "Iniciar",
        "menu_controls": "Controles",
        "menu_language": "Idioma",
        "menu_volume": "Volume",
        "menu_quit": "Sair",
        "tip_nav": "Use ↑/↓ para navegar e ENTER para selecionar",
        "controls_title": "Controles",
        "controls_move": "←/→ ou A/D: mover",
        "controls_shoot": "ESPAÇO: atirar",
        "controls_esc": "ESC: pausar / voltar",
        "controls_hint": "Derrote todos para avançar. Cada fase tem um chefe.",
        "back": "Pressione ESC para voltar",
        "volume_title": "Volume",
        "volume_tip": "Use ←/→ para ajustar, ENTER ou ESC para voltar",
        "paused": "Pausado",
        "resume": "Retomar",
        "restart": "Reiniciar Fase",
        "quit_title": "Sair para o Menu",
        "game_over": "Game Over",
        "you_win": "Você Venceu!",
        "stage": "Fase",
        "score": "Pontos",
        "lives": "Vidas",
        "highscore": "Recorde",
        "language_title": "Idioma",
        "lang_en": "Inglês",
        "lang_pt": "Português (Brasil)",
        "power_double": "Tiro Duplo",
        "power_shield": "Escudo",
        "power_slow": "Tempo Lento",
    },
}

def T(key: str):
    return STRINGS.get(LANG, STRINGS["en"]).get(key, key)

FONT_SMALL = pygame.font.SysFont("consolas", 18)
FONT = pygame.font.SysFont("consolas", 24)
FONT_BIG = pygame.font.SysFont("consolas", 42, bold=True)
FONT_ICON = pygame.font.SysFont("consolas", 16, bold=True)

SPEEDS = {
    "enemy": 3.0,
    "boss_fan": 3.0,
    "boss_special": 3.4,
    "boss_burst": 2.0,
    "boss_spiral": 2.0,
    "boss_zigzag": 3.0,
}

WHITE = (240, 240, 240)
BLACK = (10, 10, 10)
GRAY = (40, 40, 40)
GREEN = (80, 200, 120)
RED = (220, 80, 80)
YELLOW = (245, 214, 80)
BLUE = (80, 160, 245)
ORANGE = (255, 150, 80)
PURPLE = (170, 120, 255)
CYAN = (120, 230, 230)


def make_power_icon(color, text):
    size = 28
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    center = (size // 2, size // 2)
    radius = size // 2 - 2
    pygame.draw.circle(surf, (*color, 90), center, radius)
    pygame.draw.circle(surf, color, center, radius, 2)
    if text:
        glyph = FONT_ICON.render(text, True, WHITE)
        surf.blit(glyph, glyph.get_rect(center=center))
    return surf

@dataclass
class Sprite:
    image: pygame.Surface
    rect: pygame.Rect

def try_load_image(path: str, size=None, fallback_color=(200, 200, 200)) -> pygame.Surface:
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.smoothscale(img, size)
        return img
    except Exception:
        surf = pygame.Surface(size if size else (40, 40), pygame.SRCALPHA)
        surf.fill((*fallback_color, 255))
        return surf

def try_load_sound(path: str):
    try:
        snd = pygame.mixer.Sound(path)
        SOUND_EFFECTS.append(snd)
        snd.set_volume(VOLUME)
        return snd
    except Exception:
        return None

# >>> MOVIDO PARA DEPOIS DE try_load_image <<<
LIFE_ICON = try_load_image("assets/life.png", (24, 24), RED)

POWER_ICONS = {
    "double": make_power_icon(GREEN, "x2"),
    "slow": make_power_icon(YELLOW, "S"),
    "shield": make_power_icon(CYAN, "SH"),
}

SND_SHOOT = try_load_sound("assets/sfx/Hit.wav")
SND_ENEMY_SHOOT = try_load_sound("assets/sfx/enemy_shoot.wav")
SND_EXPLODE = try_load_sound("assets/sfx/explosion.wav")
SND_POWER = try_load_sound("assets/sfx/PowerUp1.wav")
SND_LOSE = try_load_sound("assets/sfx/Boom.wav")

MUSIC = {
    "menu": "assets/audio/menu.mp3",
    "JavaScript": "assets/audio/js.mp3",
    "Python": "assets/audio/python.mp3",
    "PHP": "assets/audio/php.mp3",
    "Java — Boss": "assets/audio/java.mp3",
}

def set_master_volume(level: float):
    global VOLUME
    VOLUME = max(0.0, min(1.0, level))
    try:
        pygame.mixer.music.set_volume(VOLUME)
    except Exception:
        pass
    for snd in SOUND_EFFECTS:
        try:
            snd.set_volume(VOLUME)
        except Exception:
            pass
    return VOLUME

def change_volume(delta: float):
    return set_master_volume(VOLUME + delta)

def play_music(key):
    try:
        path = MUSIC.get(key)
        if not path:
            return
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(VOLUME)
        pygame.mixer.music.play(-1)
    except Exception:
        pass

STAGE_ICONS = {
    "JavaScript": "assets/icon_js.png",
    "Python": "assets/icon_py.png",
    "PHP": "assets/icon_php.png",
    "Java — Boss": "assets/icon_java.png",
}

STAGES = [
    {
        "name": "JavaScript",
        "color": YELLOW,
        "enemy_rows": 2,
        "enemy_cols": 7,
        "enemy_speed": 1.2,
        "enemy_drop": 24,
        "enemy_shoot_chance": 0.003,
        "enemy_hp": 1,
        "player_projectile_speed": 9,
        "ext": ".js",
        "enemy_sprite": "",
        "boss": {
            "name": "JavaScript Boss",
            "hp": 28,
            "specials": ["let", "const", "()=>"],
            "cooldown": 850,
            "sprite": "assets/bossjs.png",
            "patterns": ["fan", "burst"],
        },
    },
    {
        "name": "Python",
        "color": BLUE,
        "enemy_rows": 3,
        "enemy_cols": 8,
        "enemy_speed": 1.5,
        "enemy_drop": 26,
        "enemy_shoot_chance": 0.0035,
        "enemy_hp": 1,
        "player_projectile_speed": 10,
        "ext": ".py",
        "enemy_sprite": "",
        "boss": {
            "name": "Python Boss",
            "hp": 34,
            "specials": ["def", "lambda", "async"],
            "cooldown": 800,
            "sprite": "assets/bosspython.png",
            "patterns": ["spiral", "fan"],
        },
    },
    {
        "name": "PHP",
        "color": PURPLE,
        "enemy_rows": 4,
        "enemy_cols": 9,
        "enemy_speed": 1.5,
        "enemy_drop": 26,
        "enemy_shoot_chance": 0.0035,
        "enemy_hp": 1,
        "player_projectile_speed": 10,
        "ext": ".php",
        "enemy_sprite": "",
        "boss": {
            "name": "PHP Boss",
            "hp": 36,
            "specials": ["$var", "echo", "->"],
            "cooldown": 820,
            "sprite": "assets/bossphp.png",
            "patterns": ["zigzag", "burst"],
        },
    },
    {
        "name": "Java — Boss",
        "color": ORANGE,
        "enemy_rows": 2,
        "enemy_cols": 6,
        "enemy_speed": 1.6,
        "enemy_drop": 28,
        "enemy_shoot_chance": 0.004,
        "enemy_hp": 2,
        "player_projectile_speed": 11,
        "ext": ".java",
        "enemy_sprite": "",
        "boss": {
            "name": "Java Final Boss",
            "hp": 50,
            "specials": ["new", "static", "final"],
            "cooldown": 780,
            "sprite": "assets/bossjava.png",
            "patterns": ["spiral", "fan", "burst"],
        },
    },
]

STAGE_CONFIG_BY_NAME = {stage["name"]: stage for stage in STAGES}
STAGE_ICON_SURFACES = {
    name: try_load_image(STAGE_ICONS.get(name, ""), (28, 28), config["color"])
    for name, config in STAGE_CONFIG_BY_NAME.items()
}
DEFAULT_STAGE_ICON = try_load_image("", (28, 28), (90, 90, 90))

class ScreenState(Enum):
    MENU = auto()
    CONTROLS = auto()
    LANGUAGE = auto()
    VOLUME = auto()
    PLAYING = auto()

@dataclass
class Projectile:
    owner: str
    rect: pygame.Rect
    vx: float
    vy: float
    label: str | None
    color: tuple
    x: float = 0.0
    y: float = 0.0

    def __post_init__(self):
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def set_center(self, pos):
        self.rect.center = pos
        self.sync_position()

    def sync_position(self):
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self, speed_scale=1.0):
        self.x += self.vx * speed_scale
        self.y += self.vy * speed_scale
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, surface):
        cx, cy = self.rect.centerx - 10, self.rect.centery
        pygame.draw.circle(surface, self.color, (cx, cy), 5 if self.owner == "player" else 6)
        if self.label:
            txt = FONT_SMALL.render(self.label, True, self.color)
            surface.blit(txt, (self.rect.centerx - 2, self.rect.centery - 9))

class Player:
    def __init__(self):
        self.w, self.h = 48, 32
        self.image = try_load_image("assets/player.png", (self.w, self.h), (120, 240, 160))
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 30))
        self.base_speed = 6
        self.speed = self.base_speed
        self.cooldown = 350
        self.last_shot = 0
        self.max_lives = 3
        self.lives = self.max_lives
        self.score = 0
        self.double_until = 0
        self.shield_until = 0
        self.slow_until = 0

    def move(self, keys):
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed
        self.rect.x += dx
        self.rect.x = max(10, min(WIDTH - self.rect.width - 10, self.rect.x))

    def can_shoot(self, now):
        return now - self.last_shot >= self.cooldown

    def shoot(self, bullets, speed, now):
        self.last_shot = now
        if SND_SHOOT:
            SND_SHOOT.play()
        double_active = now < self.double_until
        offsets = [0]
        if double_active:
            offsets = [-16, 16]
        for offset in offsets:
            p = Projectile("player", pygame.Rect(0,0,16,10), 0, -speed, None, GREEN)
            p.set_center((self.rect.centerx + offset, self.rect.top))
            bullets.append(p)

    def has_shield(self, now=None):
        if now is None:
            now = pygame.time.get_ticks()
        return now < self.shield_until

    def apply_power(self, kind, duration_ms, now=None):
        if now is None:
            now = pygame.time.get_ticks()
        if kind == "double":
            self.double_until = max(self.double_until, now) + duration_ms
        elif kind == "shield":
            self.shield_until = max(self.shield_until, now) + duration_ms
        elif kind == "slow":
            self.slow_until = max(self.slow_until, now) + duration_ms

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.has_shield():
            pygame.draw.rect(surface, CYAN, self.rect.inflate(10,6), 2, border_radius=6)

class Enemy:
    def __init__(self, x, y, theme_color, hp, sprite_path):
        self.w, self.h = 36, 26
        self.image = try_load_image(sprite_path, (self.w, self.h), theme_color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hp = hp

    def hit(self):
        self.hp -= 1
        return self.hp <= 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Boss:
    def __init__(self, color, name, hp, specials, cooldown, sprite, patterns):
        self.w, self.h = 140, 90
        self.image = try_load_image(sprite or "assets/boss.png", (self.w, self.h), color)
        self.rect = self.image.get_rect(midtop=(WIDTH // 2, 40))
        self.speed = 2.0
        self.dir = 1
        self.hp = hp
        self.hp_total = hp
        self.cooldown = cooldown
        self.last_fire = 0
        self.specials = specials
        self.name = name
        self.patterns = patterns
        self.pattern_index = 0
        self.spiral_angle = 0

    def update(self, speed_scale=1.0):
        self.rect.x += self.dir * (self.speed * speed_scale)
        if self.rect.right >= WIDTH - 16:
            self.dir = -1
        if self.rect.left <= 16:
            self.dir = 1

    def fire_pattern(self, enemy_bullets):
        pattern = self.patterns[self.pattern_index % len(self.patterns)]
        if pattern == "fan":
            for vx in (-4, -2, 0, 2, 4):
                b = Projectile("enemy", pygame.Rect(0,0,28,12), vx, SPEEDS["boss_fan"], None, RED)
                b.set_center(self.rect.midbottom)
                enemy_bullets.append(b)
            label = random.choice(self.specials)
            c = Projectile("enemy", pygame.Rect(0,0,38,14), 0, SPEEDS["boss_special"], label, RED)
            c.set_center(self.rect.midbottom)
            enemy_bullets.append(c)
        elif pattern == "burst":
            for i in range(12):
                ang = (i / 12) * 2 * math.pi
                vx = math.cos(ang) * SPEEDS["boss_burst"]
                vy = math.sin(ang) * SPEEDS["boss_burst"]
                b = Projectile("enemy", pygame.Rect(0,0,16,10), vx, vy, None, RED)
                b.set_center(self.rect.center)
                enemy_bullets.append(b)
        elif pattern == "spiral":
            for k in range(6):
                ang = (self.spiral_angle + k * 0.8)
                vx = math.cos(ang) * SPEEDS["boss_spiral"]
                vy = math.sin(ang) * SPEEDS["boss_spiral"]
                b = Projectile("enemy", pygame.Rect(0,0,16,10), vx, vy, None, RED)
                b.set_center(self.rect.center)
                enemy_bullets.append(b)
            self.spiral_angle += 0.5
        elif pattern == "zigzag":
            for vx in (-5, 5):
                b = Projectile("enemy", pygame.Rect(0,0,20,12), vx, SPEEDS["boss_zigzag"], None, RED)
                b.set_center(self.rect.midbottom)
                enemy_bullets.append(b)
            lbl = random.choice(self.specials)
            c = Projectile("enemy", pygame.Rect(0,0,38,14), 0, 7, lbl, RED)
            c.set_center(self.rect.midbottom)
            enemy_bullets.append(c)
        self.pattern_index += 1

    def maybe_fire(self, enemy_bullets):
        now = pygame.time.get_ticks()
        if now - self.last_fire >= self.cooldown:
            self.last_fire = now
            self.fire_pattern(enemy_bullets)
            if SND_ENEMY_SHOOT:
                SND_ENEMY_SHOOT.play()

    def hit(self):
        self.hp -= 1
        return self.hp <= 0

class PowerUp:
    def __init__(self, kind, pos):
        self.kind = kind
        self.rect = pygame.Rect(0,0,28,18)
        self.rect.center = pos
        self.vy = 2.2

    def update(self):
        self.rect.y += self.vy

    def draw(self, surface):
        color = GREEN if self.kind == "double" else CYAN if self.kind == "shield" else YELLOW
        glow = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        glow.fill((*color, 70))
        surface.blit(glow, self.rect.topleft)
        pygame.draw.rect(surface, color, self.rect, 2, border_radius=6)
        label = {
            "double": "2x",
            "shield": "S",
            "slow": "⏳",
        }[self.kind]
        text = FONT_SMALL.render(label, True, WHITE)
        surface.blit(text, text.get_rect(center=self.rect.center))

class WaveManager:
    def __init__(self, stage_idx):
        self.stage_idx = stage_idx
        self.cfg = STAGES[stage_idx]
        self.enemies = []
        self.direction = 1
        self.speed = self.cfg["enemy_speed"]
        self.drop = self.cfg["enemy_drop"]
        self.shoot_chance = self.cfg["enemy_shoot_chance"]
        self.enemy_hp = self.cfg["enemy_hp"]
        self.boss = None
        self.boss_hp_total = self.cfg["boss"]["hp"]
        self.spawn_boss = False
        margin_x, margin_y = 80, 80
        spacing_x = 64
        spacing_y = 52
        for row in range(self.cfg["enemy_rows"]):
            for col in range(self.cfg["enemy_cols"]):
                x = margin_x + col * spacing_x
                y = margin_y + row * spacing_y
                self.enemies.append(
                    Enemy(x, y, self.cfg["color"], self.enemy_hp, self.cfg["enemy_sprite"])
                )

    def update(self, slow_factor):
        if self.boss:
            self.boss.update(slow_factor)
        if not self.enemies and not self.boss and not self.spawn_boss:
            bcfg = self.cfg["boss"]
            self.boss = Boss(
                self.cfg["color"],
                bcfg["name"],
                bcfg["hp"],
                bcfg["specials"],
                bcfg["cooldown"],
                bcfg.get("sprite"),
                bcfg["patterns"],
            )
            self.spawn_boss = True
            return
        if not self.enemies:
            return
        leftmost = min(e.rect.left for e in self.enemies)
        rightmost = max(e.rect.right for e in self.enemies)
        edge_hit = (rightmost >= WIDTH - 20 and self.direction == 1) or (leftmost <= 20 and self.direction == -1)
        if edge_hit:
            self.direction *= -1
            for e in self.enemies:
                e.rect.y += self.drop
        for e in self.enemies:
            e.rect.x += self.direction * (self.speed * slow_factor)

    def maybe_enemy_fire(self, enemy_bullets):
        if self.boss:
            self.boss.maybe_fire(enemy_bullets)
        for e in self.enemies:
            if random.random() < self.shoot_chance:
                b = Projectile("enemy", pygame.Rect(0,0,38,14), 0, SPEEDS["enemy"], self.cfg["ext"], RED)
                b.set_center(e.rect.midbottom)
                enemy_bullets.append(b)
                if SND_ENEMY_SHOOT:
                    SND_ENEMY_SHOOT.play()

    def draw(self, surface):
        for e in self.enemies:
            e.draw(surface)
        if self.boss:
            surface.blit(self.boss.image, self.boss.rect)

    def all_cleared(self):
        return (not self.enemies) and (self.spawn_boss and self.boss is None)

class Game:
    def __init__(self, highscore):
        self.player = Player()
        self.stage = 0
        self.wave = WaveManager(self.stage)
        play_music(STAGES[self.stage]["name"])
        self.player_bullets = []
        self.enemy_bullets = []
        self.powerups = []
        self.paused = False
        self.game_over = False
        self.pause_index = 0
        self.highscore = highscore

    def reset_stage(self, *, renew_lives=False):
        self.player_bullets.clear()
        self.enemy_bullets.clear()
        self.powerups.clear()
        self.wave = WaveManager(self.stage)
        self.player.rect.midbottom = (WIDTH // 2, HEIGHT - 30)
        if renew_lives:
            self.player.lives = self.player.max_lives
        play_music(STAGES[self.stage]["name"])

    def update(self):
        if self.paused or self.game_over:
            return
        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        if keys[pygame.K_SPACE] and self.player.can_shoot(now):
            self.player.shoot(
                self.player_bullets,
                STAGES[self.stage]["player_projectile_speed"],
                now,
            )
        for b in self.player_bullets:
            b.update()
        slow_factor = 0.5 if now < self.player.slow_until else 1.0
        for b in self.enemy_bullets:
            b.update(slow_factor)
        for p in self.powerups:
            p.update()
        self.player_bullets = [b for b in self.player_bullets if b.rect.bottom > 0]
        self.enemy_bullets = [b for b in self.enemy_bullets if b.rect.top < HEIGHT and -40 < b.rect.left < WIDTH+40]
        self.powerups = [p for p in self.powerups if p.rect.top < HEIGHT]
        self.wave.update(slow_factor)
        self.wave.maybe_enemy_fire(self.enemy_bullets)
        for b in list(self.player_bullets):
            if self.wave.boss and b.rect.colliderect(self.wave.boss.rect):
                if self.wave.boss.hit():
                    self.player.score += 200
                    if SND_EXPLODE:
                        SND_EXPLODE.play()
                    self.wave.boss = None
                self.player_bullets.remove(b)
                continue
            for e in list(self.wave.enemies):
                if b.rect.colliderect(e.rect):
                    if e.hit():
                        self.player.score += 10
                        if SND_EXPLODE:
                            SND_EXPLODE.play()
                        if random.random() < 0.12:
                            kind = random.choice(["double","shield","slow"])
                            self.powerups.append(PowerUp(kind, e.rect.center))
                        self.wave.enemies.remove(e)
                    if b in self.player_bullets:
                        self.player_bullets.remove(b)
                    break
        for b in list(self.enemy_bullets):
            if b.rect.colliderect(self.player.rect):
                self.enemy_bullets.remove(b)
                if self.player.has_shield(now):
                    self.player.shield_until = now
                else:
                    self.player.lives -= 1
                    if self.player.lives <= 0:
                        if SND_LOSE and not self.game_over:
                            SND_LOSE.play()
                        self.game_over = True
                        self.highscore = max(self.highscore, self.player.score)
            elif b.rect.top > HEIGHT:
                if b in self.enemy_bullets:
                    self.enemy_bullets.remove(b)
        for p in list(self.powerups):
            if p.rect.colliderect(self.player.rect):
                if p.kind == "double":
                    self.player.apply_power("double", 7000, now)
                elif p.kind == "shield":
                    self.player.apply_power("shield", 6000, now)
                elif p.kind == "slow":
                    self.player.apply_power("slow", 4500, now)
                if SND_POWER:
                    SND_POWER.play()
                self.powerups.remove(p)
        for e in self.wave.enemies:
            if e.rect.bottom >= HEIGHT - 80:
                if SND_LOSE and not self.game_over:
                    SND_LOSE.play()
                self.game_over = True
                self.highscore = max(self.highscore, self.player.score)
                break
        if self.wave.all_cleared():
            if self.stage < len(STAGES) - 1:
                self.stage += 1
                self.reset_stage(renew_lives=True)
            else:
                self.game_over = True
                self.highscore = max(self.highscore, self.player.score)

    def draw_hud(self):
        hud_rect = pygame.Rect(0, 0, WIDTH, HUD_HEIGHT)
        pygame.draw.rect(screen, (24, 24, 34), hud_rect)
        pygame.draw.line(screen, (70, 70, 80), hud_rect.bottomleft, hud_rect.bottomright, 2)

        padding = 16
        top_y = hud_rect.top + 10
        name = STAGES[self.stage]["name"]
        icon = STAGE_ICON_SURFACES.get(name, DEFAULT_STAGE_ICON)
        icon_rect = icon.get_rect()
        icon_rect.x = padding
        icon_rect.centery = hud_rect.top + 24
        screen.blit(icon, icon_rect)

        stage_text = FONT.render(f"{T('stage')}: {name}", True, WHITE)
        stage_rect = stage_text.get_rect(midleft=(icon_rect.right + 12, icon_rect.centery))
        screen.blit(stage_text, stage_rect)

        score_text = FONT.render(f"{T('score')}: {self.player.score}", True, WHITE)
        score_rect = score_text.get_rect(topright=(WIDTH - padding, top_y))
        screen.blit(score_text, score_rect)

        highscore_text = FONT_SMALL.render(f"{T('highscore')}: {self.highscore}", True, WHITE)
        highscore_rect = highscore_text.get_rect(topright=(WIDTH - padding, score_rect.bottom + 6))
        screen.blit(highscore_text, highscore_rect)

        lives_label = FONT_SMALL.render(T("lives"), True, WHITE)
        life_gap = 8
        icons_width = 0
        if self.player.lives:
            icons_width = self.player.lives * LIFE_ICON.get_width() + (self.player.lives - 1) * life_gap
        lives_group_width = lives_label.get_width() + (12 if self.player.lives else 0) + icons_width
        group_center_x = WIDTH // 2
        group_start = group_center_x - lives_group_width // 2
        lives_center_x = group_start + lives_group_width // 2
        lives_label_rect = lives_label.get_rect(topleft=(group_start, hud_rect.bottom - 30))

        if self.wave.boss:
            boss_label = FONT_SMALL.render(self.wave.boss.name, True, ORANGE)
            boss_bar_width = max(110, int(WIDTH * 0.2))
            boss_bar_height = 10
            boss_bar_rect = pygame.Rect(0, 0, boss_bar_width, boss_bar_height)
            boss_bar_rect.midbottom = (lives_center_x, lives_label_rect.top - 6)

            boss_label_rect = boss_label.get_rect(midbottom=(boss_bar_rect.centerx, boss_bar_rect.top - 4))
            screen.blit(boss_label, boss_label_rect)

            pygame.draw.rect(screen, (45, 45, 60), boss_bar_rect, border_radius=6)

            pct = max(0, self.wave.boss.hp) / self.wave.boss_hp_total if self.wave.boss_hp_total else 0
            boss_fill_rect = boss_bar_rect.copy()
            boss_fill_rect.width = max(0, int(boss_bar_width * pct))
            if boss_fill_rect.width:
                pygame.draw.rect(screen, ORANGE, boss_fill_rect, border_radius=6)
            pygame.draw.rect(screen, (20, 20, 30), boss_bar_rect, 1, border_radius=6)

        screen.blit(lives_label, lives_label_rect)

        if self.player.lives:
            icon_y = lives_label_rect.centery - LIFE_ICON.get_height() // 2
            for i in range(self.player.lives):
                offset = i * (LIFE_ICON.get_width() + life_gap)
                screen.blit(LIFE_ICON, (lives_label_rect.right + 12 + offset, icon_y))

        now = pygame.time.get_ticks()
        power_icons = []
        if now < self.player.double_until:
            power_icons.append(POWER_ICONS["double"])
        if now < self.player.slow_until:
            power_icons.append(POWER_ICONS["slow"])
        if self.player.has_shield(now):
            power_icons.append(POWER_ICONS["shield"])

        icon_left = padding
        icon_bottom = hud_rect.bottom - 2
        icon_gap = 10
        for icon in power_icons:
            icon_rect = icon.get_rect()
            icon_rect.left = icon_left
            icon_rect.bottom = icon_bottom
            screen.blit(icon, icon_rect)
            icon_left = icon_rect.right + icon_gap

    def draw(self):
        screen.fill(BLACK)
        grid_color = (20, 20, 20)
        for x in range(0, WIDTH, 40):
            pygame.draw.line(screen, grid_color, (x, HUD_HEIGHT), (x, HEIGHT))
        for y in range(HUD_HEIGHT, HEIGHT, 40):
            pygame.draw.line(screen, grid_color, (0, y), (WIDTH, y))
        self.draw_hud()
        self.player.draw(screen)
        self.wave.draw(screen)
        for b in self.player_bullets:
            b.draw(screen)
        for b in self.enemy_bullets:
            b.draw(screen)
        for p in self.powerups:
            p.draw(screen)
        if self.paused:
            draw_pause_overlay(self.pause_index)
        if self.game_over:
            title = FONT_BIG.render(T('you_win') if (self.stage == len(STAGES)-1 and self.wave.all_cleared()) else T('game_over'), True, WHITE)
            screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 10)))
            tip = FONT.render("ESC", True, (180,180,180))
            screen.blit(tip, tip.get_rect(center=(WIDTH//2, HEIGHT//2 + 34)))

def draw_center_message(text):
    box = pygame.Rect(0, 0, 680, 120)
    box.center = (WIDTH//2, HEIGHT//2)
    pygame.draw.rect(screen, (30, 30, 30), box, border_radius=14)
    pygame.draw.rect(screen, (65, 65, 65), box, 2, border_radius=14)
    label = FONT.render(text, True, WHITE)
    screen.blit(label, label.get_rect(center=box.center))

def draw_title_screen(selected, highscore):
    screen.fill(BLACK)
    title = FONT_BIG.render(T("title"), True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH//2, 120)))
    subtitle = FONT.render(T("subtitle"), True, WHITE)
    screen.blit(subtitle, subtitle.get_rect(center=(WIDTH//2, 170)))
    options = [T("menu_start"), T("menu_controls"), T("menu_language"), T("menu_volume"), T("menu_quit")]
    for i, text in enumerate(options):
        color = WHITE if i == selected else (150, 150, 150)
        surf = FONT.render(text, True, color)
        screen.blit(surf, surf.get_rect(center=(WIDTH//2, 260 + i*44)))
    tip = FONT_SMALL.render(T("tip_nav"), True, (180, 180, 180))
    screen.blit(tip, tip.get_rect(center=(WIDTH//2, HEIGHT - 60)))
    hs = FONT.render(f"{T('highscore')}: {highscore}", True, WHITE)
    screen.blit(hs, (20, 20))

def draw_controls_screen():
    screen.fill(BLACK)
    title = FONT_BIG.render(T("controls_title"), True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH//2, 120)))
    lines = [T("controls_move"), T("controls_shoot"), T("controls_esc"), T("controls_hint")]
    for i, line in enumerate(lines):
        surf = FONT.render(line, True, WHITE)
        screen.blit(surf, surf.get_rect(center=(WIDTH//2, 210 + i*36)))
    tip = FONT_SMALL.render(T("back"), True, (180, 180, 180))
    screen.blit(tip, tip.get_rect(center=(WIDTH//2, HEIGHT - 60)))

def draw_language_screen(selected=0):
    screen.fill(BLACK)
    title = FONT_BIG.render(T("language_title"), True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH//2, 120)))
    options = [("en", T("lang_en")), ("pt_BR", T("lang_pt"))]
    for i, (_, label) in enumerate(options):
        color = WHITE if i == selected else (150, 150, 150)
        surf = FONT.render(label, True, color)
        screen.blit(surf, surf.get_rect(center=(WIDTH//2, 260 + i*44)))
    tip = FONT_SMALL.render(T("back"), True, (180, 180, 180))
    screen.blit(tip, tip.get_rect(center=(WIDTH//2, HEIGHT - 60)))

def draw_volume_screen():
    screen.fill(BLACK)
    title = FONT_BIG.render(T("volume_title"), True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH//2, 120)))

    bar = pygame.Rect(0, 0, 360, 14)
    bar.center = (WIDTH // 2, 260)
    pygame.draw.rect(screen, (60, 60, 60), bar, border_radius=6)
    fill = bar.copy()
    fill.width = int(bar.width * VOLUME)
    if fill.width > 0:
        pygame.draw.rect(screen, GREEN if VOLUME > 0 else (120, 120, 120), fill, border_radius=6)
    knob_x = bar.left + int(bar.width * VOLUME)
    knob_x = max(bar.left, min(bar.right, knob_x))
    pygame.draw.circle(screen, WHITE, (knob_x, bar.centery), 10)

    value = FONT.render(f"{int(round(VOLUME * 100))}%", True, WHITE)
    screen.blit(value, value.get_rect(center=(WIDTH//2, 320)))

    tip = FONT_SMALL.render(T("volume_tip"), True, (180, 180, 180))
    screen.blit(tip, tip.get_rect(center=(WIDTH//2, HEIGHT - 60)))

def draw_pause_overlay(index):
    box = pygame.Rect(0, 0, 420, 220)
    box.center = (WIDTH//2, HEIGHT//2)
    pygame.draw.rect(screen, (30, 30, 30), box, border_radius=14)
    pygame.draw.rect(screen, (65, 65, 65), box, 2, border_radius=14)
    title = FONT_BIG.render(T("paused"), True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 60)))
    options = [T("resume"), T("restart"), T("quit_title")]
    for i, text in enumerate(options):
        color = WHITE if i == index else (160,160,160)
        surf = FONT.render(text, True, color)
        screen.blit(surf, surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 8 + i*40)))

def load_save():
    try:
        with open("save.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            hs = int(data.get("highscore", 0))
            lang = data.get("lang", "en")
            volume = float(data.get("volume", DEFAULT_VOLUME))
            volume = max(0.0, min(1.0, volume))
            return hs, lang, volume
    except Exception:
        return 0, "en", DEFAULT_VOLUME

def write_save(highscore, lang, volume):
    try:
        with open("save.json", "w", encoding="utf-8") as f:
            json.dump({
                "highscore": int(highscore),
                "lang": lang,
                "volume": round(max(0.0, min(1.0, float(volume))), 3),
            }, f)
    except Exception:
        pass

def main():
    global LANG, display

    highscore, saved_lang, saved_volume = load_save()
    LANG = saved_lang if saved_lang in STRINGS else "en"
    set_master_volume(saved_volume)

    screen_state = ScreenState.MENU
    menu_index = 0
    lang_index = 0 if LANG == "en" else 1
    game: Optional[Game] = None

    play_music("menu")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                final_score = highscore if not game else max(highscore, game.highscore)
                write_save(final_score, LANG, VOLUME)
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.VIDEORESIZE:
                display = pygame.display.set_mode(event.size, pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
                if screen_state == ScreenState.MENU:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        menu_index = (menu_index - 1) % 5
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        menu_index = (menu_index + 1) % 5
                    elif event.key == pygame.K_RETURN:
                        if menu_index == 0:
                            game = Game(highscore)
                            screen_state = ScreenState.PLAYING
                        elif menu_index == 1:
                            screen_state = ScreenState.CONTROLS
                        elif menu_index == 2:
                            screen_state = ScreenState.LANGUAGE
                        elif menu_index == 3:
                            screen_state = ScreenState.VOLUME
                        elif menu_index == 4:
                            final_score = highscore if not game else max(highscore, game.highscore)
                            write_save(final_score, LANG, VOLUME)
                            pygame.quit()
                            raise SystemExit
                    elif event.key == pygame.K_ESCAPE:
                        # Ignore escape in the menu to avoid accidental exits
                        pass

                elif screen_state == ScreenState.CONTROLS:
                    if event.key == pygame.K_ESCAPE:
                        screen_state = ScreenState.MENU

                elif screen_state == ScreenState.LANGUAGE:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        lang_index = (lang_index - 1) % 2
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        lang_index = (lang_index + 1) % 2
                    elif event.key == pygame.K_RETURN:
                        LANG = "en" if lang_index == 0 else "pt_BR"
                        screen_state = ScreenState.MENU
                        current_highscore = highscore if not game else max(highscore, game.highscore)
                        write_save(current_highscore, LANG, VOLUME)
                    elif event.key == pygame.K_ESCAPE:
                        screen_state = ScreenState.MENU

                elif screen_state == ScreenState.VOLUME:
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        change_volume(-0.05)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        change_volume(0.05)
                    elif event.key in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_SPACE):
                        current_highscore = highscore if not game else max(highscore, game.highscore)
                        write_save(current_highscore, LANG, VOLUME)
                        screen_state = ScreenState.MENU

                elif screen_state == ScreenState.PLAYING and game:
                    if event.key == pygame.K_ESCAPE:
                        if game.game_over:
                            highscore = max(highscore, game.highscore)
                            write_save(highscore, LANG, VOLUME)
                            screen_state = ScreenState.MENU
                            game = None
                            play_music("menu")
                        elif game.paused:
                            game.paused = False
                        else:
                            game.paused = True
                            game.pause_index = 0

                    elif game.paused:
                        if event.key in (pygame.K_UP, pygame.K_w):
                            game.pause_index = (game.pause_index - 1) % 3
                        elif event.key in (pygame.K_DOWN, pygame.K_s):
                            game.pause_index = (game.pause_index + 1) % 3
                        elif event.key == pygame.K_RETURN:
                            if game.pause_index == 0:
                                game.paused = False
                            elif game.pause_index == 1:
                                game.reset_stage()
                                game.paused = False
                            elif game.pause_index == 2:
                                highscore = max(highscore, game.highscore)
                                write_save(highscore, LANG, VOLUME)
                                screen_state = ScreenState.MENU
                                game = None
                                play_music("menu")
                    elif game.game_over and event.key == pygame.K_RETURN:
                        highscore = max(highscore, game.highscore)
                        write_save(highscore, LANG, VOLUME)
                        screen_state = ScreenState.MENU
                        game = None
                        play_music("menu")

        if screen_state == ScreenState.MENU:
            draw_title_screen(menu_index, highscore)
        elif screen_state == ScreenState.CONTROLS:
            draw_controls_screen()
        elif screen_state == ScreenState.LANGUAGE:
            draw_language_screen(lang_index)
        elif screen_state == ScreenState.VOLUME:
            draw_volume_screen()
        elif screen_state == ScreenState.PLAYING and game:
            game.update()
            game.draw()
            highscore = max(highscore, game.highscore)

        target_size = display.get_size()
        if target_size == (WIDTH, HEIGHT):
            display.blit(screen, (0, 0))
        else:
            pygame.transform.smoothscale(screen, target_size, display)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
