import os
import pygame

from script.setting import BASE_HEIGHT, GROUND_LEVEL
from script.core.obj import Obj
from script.actors.player.attack import PlayerAttackController


class Player(Obj):
    """
    Classe principal do jogador.

    Responsável por:
    - movimento
    - física
    - roll
    - estados gerais
    - animação
    - vida/morte
    - delegar a lógica de ataque ao PlayerAttackController

    Controles:
    - A / D ou ← / → : mover
    - S / ↓          : agachar
    - SPACE          : pular
    - K              : bloquear
    - Q              : atacar
    - E              : interagir
    - Left Shift     : roll / dash
    """

    # =========================================================
    # ETAPA 1 - CONSTANTES GERAIS DO PLAYER
    # =========================================================

    BUSY_STATES = {
        "aim", "c_aim", "jump_aim",
        "shot", "c_shot", "jump_shot",
        "charge_shot", "c_charge_shot", "jump_charge_shot",
        "block", "c_block", "roll", "dead"
    }

    BLOCK_STATES = {"block", "c_block"}

    DIRLESS_STATES = {
        "idle", "walk", "down", "block", "c_block", "roll", "dead"
    }

    SCREEN_WIDTH = 1280
    SIDE_BUFFER = 75
    WALK_SPEED = 2.8

    GRAVITY = 0.5
    JUMP_POWER = -15
    MAX_FALL_SPEED = 10

    ROLL_KEY = pygame.K_LSHIFT
    ROLL_DURATION_MS = 350
    ROLL_DISTANCE_PX = 200
    ROLL_COOLDOWN_MS = 450

    SPRITE_ROOT = "assets/charsSprite/player/indigenaM/"

    def __init__(self, image_path, position, groups, size=(200, 200),
                 life=25, lives=3, xp=0, has_hole=True):
        super().__init__(image_path, position, groups, size)

        # =========================================================
        # ETAPA 2 - DADOS BÁSICOS DO PLAYER
        # =========================================================
        self.image_path = image_path
        self.size = size
        self.has_hole = has_hole

        self.life = life
        self.lives = lives
        self.xp = xp
        self.gold = 0

        # =========================================================
        # ETAPA 3 - SPRITE INICIAL
        # =========================================================
        self.original_image = pygame.image.load(
            os.path.join(self.SPRITE_ROOT, "R0.png")
        ).convert_alpha()

        self.image = pygame.transform.scale(self.original_image, size)
        self.rect = self.image.get_rect(topleft=position)

        # =========================================================
        # ETAPA 4 - INICIALIZAÇÃO DOS ATRIBUTOS
        # =========================================================
        self._setup_world_state()
        self._setup_movement_state()
        self._setup_roll_state()
        self._setup_animation_state()
        self._setup_dialog_state()

        # =========================================================
        # ETAPA 5 - CONTROLADOR DE ATAQUE
        # =========================================================
        self.attack = PlayerAttackController(self)
        self.shots = self.attack.shots

        # =========================================================
        # ETAPA 6 - ANIMAÇÕES
        # =========================================================
        self._setup_animations(position)

    # =========================================================
    # ETAPA 7 - ESTADOS DO MUNDO
    # =========================================================

    def _setup_world_state(self):
        self.in_hole = False
        self.fall_lock_x_range = None
        self.is_dead = False
        self.on_ground = False
        self.is_jumping = False
        self.exit_mode = False

    # =========================================================
    # ETAPA 8 - ESTADOS DE MOVIMENTO
    # =========================================================

    def _setup_movement_state(self):
        self.facing_right = True
        self.right = False
        self.left = False
        self.crouching = False
        self.blocking = False
        self.rolling = False
        self.invulnerable = False

        self.vel = 5
        self.grav = self.GRAVITY
        self.jump_power = self.JUMP_POWER

    # =========================================================
    # ETAPA 9 - ESTADOS DO ROLL
    # =========================================================

    def _setup_roll_state(self):
        self.roll_key = self.ROLL_KEY
        self.roll_duration_ms = self.ROLL_DURATION_MS
        self.roll_distance_px = self.ROLL_DISTANCE_PX
        self.roll_cooldown_ms = self.ROLL_COOLDOWN_MS

        self.roll_timer = 0
        self._last_tick_ms = 0
        self._last_roll_end_ms = -9999
        self._roll_acc_px = 0.0
        self.roll_moved_px = 0.0

    # =========================================================
    # ETAPA 10 - ESTADOS DE ANIMAÇÃO
    # =========================================================

    def _setup_animation_state(self):
        self.current_frame = 0
        self.animation_speed = 5
        self.ticks = 0
        self.img = 0
        self.state = "idle"

    # =========================================================
    # ETAPA 11 - ESTADOS DE DIÁLOGO
    # =========================================================

    def _setup_dialog_state(self):
        self.dialog_active = False
        self.dialog_npc = None
        self.is_moving = True

    # =========================================================
    # ETAPA 12 - UTILITÁRIOS DE IMAGEM
    # =========================================================

    def _safe_load_image(self, filename):
        path = os.path.join(self.SPRITE_ROOT, filename)
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, self.size)

    def _load_seq_scaled(self, prefix: str, count: int, size=None, root=None):
        size = size or self.size
        root = root or self.SPRITE_ROOT
        frames = []

        for i in range(count):
            found = None

            for pf in (prefix, prefix.replace("_", "")):
                for ext in (".png", ".PNG"):
                    path = os.path.join(root, f"{pf}{i}{ext}")
                    if os.path.exists(path):
                        found = path
                        break
                if found:
                    break

            if not found:
                if i == 0:
                    frames = []
                break

            img = pygame.image.load(found).convert_alpha()
            frames.append(pygame.transform.scale(img, size))

        if frames:
            return frames

        for pf in (prefix, prefix.replace("_", "")):
            for ext in (".png", ".PNG"):
                one = os.path.join(root, f"{pf}{ext}")
                if os.path.exists(one):
                    img = pygame.image.load(one).convert_alpha()
                    return [pygame.transform.scale(img, size)]

        return []

    def _ensure_anim(self, key: str, prefix: str, count: int, fallback_key=None):
        if key in self.animations and self.animations[key]:
            return

        frames = self._load_seq_scaled(prefix, count)

        if frames:
            self.animations[key] = frames
        elif fallback_key and fallback_key in self.animations:
            self.animations[key] = self.animations[fallback_key]
        else:
            self.animations[key] = self.animations["idle"]

    # =========================================================
    # ETAPA 13 - CONFIGURAÇÃO DAS ANIMAÇÕES
    # =========================================================

    def _setup_animations(self, position):
        """
        Registra todas as animações do player.
        """
        idle_frames = [
            self._safe_load_image("R0.png"),
            self._safe_load_image("R1.png"),
        ]

        walk_frames = [
            self._safe_load_image(f"M{i}.png")
            for i in range(8)
        ]

        shot_frames = self._load_seq_scaled("S", 7) or idle_frames
        jump_frames = self._load_seq_scaled("J", 17) or idle_frames
        block_frames = self._load_seq_scaled("B_U", 1) or idle_frames
        c_block_frames = self._load_seq_scaled("B_D", 1) or idle_frames
        c_shot_frames = self._load_seq_scaled("S_D", 7) or shot_frames

        self.animations = {
            "idle": idle_frames,
            "walk": walk_frames,
            "shot": shot_frames,
            "jump": jump_frames,
            "c_idle": [],
            "block": block_frames,
            "c_block": c_block_frames,
            "c_shot": c_shot_frames,
            "roll": c_block_frames,
            "dead": c_block_frames,
        }

        # ---------------------------------------------------------
        # Tiros em ambas as direções
        # ---------------------------------------------------------
        self.animations["shot_right"] = self.animations["shot"]
        self.animations["shot_left"] = [
            pygame.transform.flip(img, True, False)
            for img in self.animations["shot"]
        ]

        # ---------------------------------------------------------
        # Pulo em ambas as direções
        # ---------------------------------------------------------
        self.animations["jump_right"] = self.animations["jump"]
        self.animations["jump_left"] = [
            pygame.transform.flip(img, True, False)
            for img in self.animations["jump"]
        ]

        # ---------------------------------------------------------
        # Tiro agachado nas duas direções
        # ---------------------------------------------------------
        self.animations["c_shot_right"] = self.animations["c_shot"]
        self.animations["c_shot_left"] = [
            pygame.transform.flip(img, True, False)
            for img in self.animations["c_shot"]
        ]

        # ---------------------------------------------------------
        # Estado agachado parado
        # ---------------------------------------------------------
        self.animations["down"] = []

        if not self.animations["c_idle"]:
            self._ensure_anim("c_idle", "R_D", 1, fallback_key="idle")

        self.animations["down"] = self.animations["c_idle"]

        # ---------------------------------------------------------
        # MIRA DO CHARGE SHOT
        # Em pé = frame 3 de S
        # Agachado = frame 3 de S_D
        # ---------------------------------------------------------

        # Mira em pé
        aim_right_frame = self.animations["shot_right"][3] if len(self.animations["shot_right"]) > 3 else self.animations["shot_right"][0]
        aim_left_frame = self.animations["shot_left"][3] if len(self.animations["shot_left"]) > 3 else self.animations["shot_left"][0]

        self.animations["aim_right"] = [aim_right_frame]
        self.animations["aim_left"] = [aim_left_frame]

        # Mira agachado
        c_aim_right_frame = self.animations["c_shot_right"][3] if len(self.animations["c_shot_right"]) > 3 else self.animations["c_shot_right"][0]
        c_aim_left_frame = self.animations["c_shot_left"][3] if len(self.animations["c_shot_left"]) > 3 else self.animations["c_shot_left"][0]

        self.animations["c_aim_right"] = [c_aim_right_frame]
        self.animations["c_aim_left"] = [c_aim_left_frame]

        # Mira no ar
        self.animations["jump_aim_right"] = self.animations["jump_right"]
        self.animations["jump_aim_left"] = self.animations["jump_left"]

        # ---------------------------------------------------------
        # Tiros especiais
        # ---------------------------------------------------------

        # Jump shot usa a sequência normal de tiro
        self.animations["jump_shot_right"] = self.animations["shot_right"]
        self.animations["jump_shot_left"] = self.animations["shot_left"]

        # Charge shot começa a partir do frame 4
        self.animations["charge_shot_right"] = (
            self.animations["shot_right"][4:]
            if len(self.animations["shot_right"]) > 4
            else self.animations["shot_right"]
        )
        self.animations["charge_shot_left"] = (
            self.animations["shot_left"][4:]
            if len(self.animations["shot_left"]) > 4
            else self.animations["shot_left"]
        )

        self.animations["c_charge_shot_right"] = (
            self.animations["c_shot_right"][4:]
            if len(self.animations["c_shot_right"]) > 4
            else self.animations["c_shot_right"]
        )
        self.animations["c_charge_shot_left"] = (
            self.animations["c_shot_left"][4:]
            if len(self.animations["c_shot_left"]) > 4
            else self.animations["c_shot_left"]
        )

        self.animations["jump_charge_shot_right"] = (
            self.animations["shot_right"][4:]
            if len(self.animations["shot_right"]) > 4
            else self.animations["shot_right"]
        )
        self.animations["jump_charge_shot_left"] = (
            self.animations["shot_left"][4:]
            if len(self.animations["shot_left"]) > 4
            else self.animations["shot_left"]
        )

        # Imagem inicial
        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect(topleft=position)

    # =========================================================
    # ETAPA 14 - UTILITÁRIOS DE ESTADO
    # =========================================================

    def _is_busy(self):
        return self.state in self.BUSY_STATES or self.blocking

    def _is_dead_state(self):
        return self.is_dead or self.state == "dead"

    def _roll_ready(self):
        return pygame.time.get_ticks() - self._last_roll_end_ms >= self.roll_cooldown_ms

    # =========================================================
    # ETAPA 15 - UPDATE PRINCIPAL
    # =========================================================

    def update(self):
        super().update()

        # Atualiza a carga do charge shot
        self.attack.update_charge()

        # Física do personagem
        self._update_gravity()

        # Atualiza projéteis já disparados
        self.attack.update_projectiles()

        # Se estiver morto, só toca animação de morte
        if self._is_dead_state():
            self._update_dead()
            return

        # Mantém a mira apenas se o charge já estiver pronto
        if self.attack.attack_holding and self.attack.charge_ready:
            self.attack.update_aim_state()

        # Movimento normal só acontece se não estiver em estado ocupado
        if not self._is_busy() and not self.attack.attack_holding:
            self._update_movement()

        self._update_block_state()
        self.attack.update_attack_animation()
        self._update_crouch_idle_state()
        self._update_roll_state()

        if self.dialog_active:
            return

        self._update_death_check()

    # =========================================================
    # ETAPA 16 - GRAVIDADE
    # =========================================================

    def _update_gravity(self):
        self.vel += self.grav
        self.rect.y += self.vel

        if hasattr(self, "holes"):
            for hole_rect in self.holes:
                if hole_rect.collidepoint(self.rect.centerx, self.rect.bottom):
                    if not self.in_hole:
                        print("[DEBUG] Entrou no buraco!")
                        self.in_hole = True
                        self.fall_lock_x_range = (hole_rect.left, hole_rect.right)
                    break

        if self.vel >= self.MAX_FALL_SPEED:
            self.vel = self.MAX_FALL_SPEED

        if not self.in_hole:
            if self.rect.y >= GROUND_LEVEL - self.rect.height:
                self.rect.y = GROUND_LEVEL - self.rect.height
                self.vel = 0
                self.on_ground = True
                self.is_jumping = False

    def set_holes(self, hole_list):
        self.holes = hole_list

    # =========================================================
    # ETAPA 17 - EVENTOS
    # =========================================================

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            self._handle_keydown(event)
        elif event.type == pygame.KEYUP:
            self._handle_keyup(event)

    def _handle_keydown(self, event):
        pressed = pygame.key.get_pressed()
        crouch_mod = pressed[pygame.K_s] or pressed[pygame.K_DOWN]

        if event.key in (pygame.K_d, pygame.K_RIGHT):
            self.right = True
            self.facing_right = True
            return

        if event.key in (pygame.K_a, pygame.K_LEFT):
            self.left = True
            self.facing_right = False
            return

        if event.key in (pygame.K_s, pygame.K_DOWN):
            self._enter_crouch()
            return

        if event.key == pygame.K_k:
            self._enter_block(crouch_mod)
            return

        if event.key == self.roll_key:
            self._try_start_roll()
            return

        if event.key == pygame.K_SPACE:
            self._try_jump()
            return

        # Q = começa a segurar para decidir entre short e charge
        if event.key == self.attack.ATTACK_KEY:
            self.attack.start_attack_hold()
            return

        if event.key == pygame.K_e:
            if self.dialog_npc:
                self.start_dialogue(self.dialog_npc)

    def _handle_keyup(self, event):
        if event.key in (pygame.K_d, pygame.K_RIGHT):
            self.right = False
            return

        if event.key in (pygame.K_a, pygame.K_LEFT):
            self.left = False
            return

        if event.key in (pygame.K_s, pygame.K_DOWN):
            self.crouching = False

            if self.blocking:
                self.state = "block"
            elif not self.on_ground:
                self.state = "jump"
            else:
                self.state = "idle"
            return

        if event.key == pygame.K_k:
            self.blocking = False
            if self.state in self.BLOCK_STATES:
                self.state = "down" if self.crouching else "idle"
            return

        # Q = ao soltar, decide entre short normal e charge shot
        if event.key == self.attack.ATTACK_KEY:
            self.attack.release_attack_hold()
            return

    # =========================================================
    # ETAPA 18 - AÇÕES DO PLAYER
    # =========================================================

    def _enter_crouch(self):
        self.crouching = True

        if not self.animations["c_idle"]:
            self._ensure_anim("c_idle", "R_D", 1, fallback_key="idle")
            self.animations["down"] = self.animations["c_idle"]

        self.state = "c_block" if self.blocking else "down"

    def _enter_block(self, crouch_mod):
        self.blocking = True
        self.state = "c_block" if (crouch_mod or self.crouching) else "block"

    def _try_start_roll(self):
        if self.rolling or self.blocking or not self._roll_ready() or self.attack.attack_holding:
            return

        self.rolling = True
        self.invulnerable = True
        self.roll_timer = 0
        self._last_tick_ms = pygame.time.get_ticks()
        self.state = "roll"
        self.img = 0
        self.ticks = 0
        self._roll_acc_px = 0.0
        self.roll_moved_px = 0.0

    def _try_jump(self):
        if self.on_ground and not self.blocking and not self.rolling:
            self.vel = self.jump_power
            self.on_ground = False
            self.is_jumping = True
            self.state = "jump"

    # =========================================================
    # ETAPA 19 - MOVIMENTO
    # =========================================================

    def _update_movement(self):
        """
        Atualiza movimento lateral e estados básicos.
        Não deixa o movimento sobrescrever a mira/ataque.
        """
        if self.state in {
            "shot", "c_shot", "jump_shot",
            "charge_shot", "c_charge_shot", "jump_charge_shot",
            "aim", "c_aim", "jump_aim"
        }:
            return

        if self.crouching and not self.left and not self.right and not self.is_jumping:
            if not self.animations["down"]:
                self._ensure_anim("c_idle", "R_D", 1, fallback_key="idle")
                self.animations["down"] = self.animations["c_idle"]

            self.state = "down"
            frames_down = max(1, len(self.animations.get("down", [])))
            self.animate("down", 100, frames_down)
            return

        if self.right:
            self._move_right()
        elif self.left:
            self._move_left()
        else:
            if self.on_ground:
                self.state = "idle"
                self.animate("idle", 100, 1)

        if self.is_jumping or not self.on_ground:
            direction_anim = "jump_right" if self.facing_right else "jump_left"
            self.animate(direction_anim, 50, 17)

    def _move_right(self):
        next_x = self.rect.x + self.WALK_SPEED

        if self.in_hole:
            if self.fall_lock_x_range and next_x + self.rect.width <= self.fall_lock_x_range[1]:
                self.rect.x = next_x
        else:
            if getattr(self, "exit_mode", False):
                self.rect.x = next_x
            else:
                if next_x + self.rect.width - self.SIDE_BUFFER < self.SCREEN_WIDTH:
                    self.rect.x = next_x

        if self.rect.x + self.rect.width - self.SIDE_BUFFER < self.SCREEN_WIDTH:
            self.facing_right = True

        self.state = "walk"
        self.animate("walk", 15, 7)

    def _move_left(self):
        next_x = self.rect.x - self.WALK_SPEED

        if self.in_hole:
            if self.fall_lock_x_range and next_x >= self.fall_lock_x_range[0]:
                self.rect.x = next_x
        else:
            if next_x + self.SIDE_BUFFER > 0:
                self.rect.x = next_x

        if self.rect.x + self.SIDE_BUFFER > 0:
            self.facing_right = False

        self.state = "walk"
        self.animate("walk", 15, 7)

    # =========================================================
    # ETAPA 20 - ESTADOS ESPECIAIS
    # =========================================================

    def _update_block_state(self):
        """
        Mantém a animação de bloqueio sem sobrescrever o ataque.
        """
        if not self.blocking:
            return

        if self.attack.attack_holding:
            return

        if self.state in {
            "shot", "c_shot", "jump_shot",
            "charge_shot", "c_charge_shot", "jump_charge_shot",
            "aim", "c_aim", "jump_aim"
        }:
            return

        self.state = "c_block" if self.crouching else "block"
        self.animate(self.state, 80, 1)

    def _update_crouch_idle_state(self):
        if (
            self.crouching and
            not self.left and
            not self.right and
            not self.is_jumping and
            not self.blocking and
            self.state not in {
                "shot", "c_shot", "jump_shot",
                "charge_shot", "c_charge_shot", "jump_charge_shot",
                "roll", "dead", "aim", "c_aim", "jump_aim"
            }
        ):
            if not self.animations["c_idle"]:
                self._ensure_anim("c_idle", "R_D", 1, fallback_key="idle")
                self.animations["down"] = self.animations["c_idle"]

            self.state = "down"
            frames_down = max(1, len(self.animations.get("down", [])))
            self.animate("down", 100, frames_down)

    def _update_roll_state(self):
        if self.state != "roll":
            return

        now = pygame.time.get_ticks()
        dt_ms = now - (self._last_tick_ms or now)
        self._last_tick_ms = now
        self.roll_timer += dt_ms

        speed_px_per_ms = self.roll_distance_px / max(1, self.roll_duration_ms)
        step = speed_px_per_ms * dt_ms

        remaining = self.roll_distance_px - self.roll_moved_px
        step = min(step, max(0.0, remaining))

        self._roll_acc_px += step
        apply_px = int(self._roll_acc_px)
        self._roll_acc_px -= apply_px

        if apply_px > 0:
            dx = apply_px if self.facing_right else -apply_px
            self._move_x_with_limits(dx)
            self.roll_moved_px += abs(apply_px)

        self.animate("roll", 10, max(1, len(self.animations["roll"])))

        if self.roll_moved_px >= self.roll_distance_px or self.roll_timer >= self.roll_duration_ms:
            self.rolling = False
            self.invulnerable = False
            self.state = "idle"
            self.roll_timer = 0
            self._last_roll_end_ms = pygame.time.get_ticks()
            self._roll_acc_px = 0.0
            self.roll_moved_px = 0.0

    def _update_dead(self):
        self.is_dead = True
        self.animate("dead", 12, max(1, len(self.animations["dead"])))

    def _update_death_check(self):
        if self.check_death():
            if self.lives <= 0:
                self.die()

    # =========================================================
    # ETAPA 21 - MOVIMENTO COM LIMITES
    # =========================================================

    def _move_x_with_limits(self, dx: int):
        if getattr(self, "exit_mode", False):
            self.rect.x += dx
            return

        next_x = self.rect.x + dx

        if self.in_hole and self.fall_lock_x_range:
            left, right = self.fall_lock_x_range
            next_x = max(left, min(next_x, right - self.rect.width))
            self.rect.x = next_x
            return

        if dx > 0:
            if next_x + self.rect.width - self.SIDE_BUFFER < self.SCREEN_WIDTH:
                self.rect.x = next_x
        else:
            if next_x + self.SIDE_BUFFER > 0:
                self.rect.x = next_x

    # =========================================================
    # ETAPA 22 - ANIMAÇÃO
    # =========================================================

    def animate(self, name, ticks, limit):
        """
        Atualiza a animação do player.

        IMPORTANTE:
        - animações de tiro tocam uma única vez
        - animações normais podem entrar em loop
        """
        self.ticks += 1
        if self.ticks >= ticks:
            self.ticks = 0
            self.img += 1

        frames = self.animations.get(name, [])
        num_frames = len(frames)

        if num_frames == 0:
            return

        # Animações de ciclo único
        one_shot_names = {
            "shot_right", "shot_left",
            "c_shot_right", "c_shot_left",
            "jump_shot_right", "jump_shot_left",
            "charge_shot_right", "charge_shot_left",
            "c_charge_shot_right", "c_charge_shot_left",
            "jump_charge_shot_right", "jump_charge_shot_left",
        }

        if name in one_shot_names:
            if self.img >= num_frames:
                self.img = num_frames - 1
        else:
            if self.img >= num_frames:
                self.img = 0

        self.image = frames[self.img]
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

        # Deixa o controlador de ataque verificar se precisa:
        # - soltar a flecha
        # - encerrar a animação
        self.attack.handle_animation_events(name, num_frames)

        if name in self.DIRLESS_STATES and not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    # =========================================================
    # ETAPA 23 - DIÁLOGO
    # =========================================================

    def start_dialogue(self, npc):
        self.dialog_active = True
        print(f"{npc.__class__.__name__}: Bem-vindo, jovem guerreiro! O que procura?")
        self.is_moving = False

    def stop_dialogue(self):
        self.dialog_active = False
        self.is_moving = True
        print("Diálogo finalizado.")

    # =========================================================
    # ETAPA 24 - VIDA / MORTE
    # =========================================================

    def check_death(self):
        if self.rect.y > BASE_HEIGHT:
            self.lives -= 1
            print(f"[DEBUG] Morreu. Vidas restantes: {self.lives}")

            if self.lives > 0:
                self._respawn()
                return True
            else:
                self.die()
                return False

        return False

    def _respawn(self):
        self.rect.x, self.rect.y = 100, 250
        self.vel = 0
        self.on_ground = False
        self.is_jumping = False
        self.in_hole = False
        self.state = "idle"

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.die()

    def die(self):
        self.is_dead = True
        self.state = "dead"
        self.img = 0
        self.ticks = 0