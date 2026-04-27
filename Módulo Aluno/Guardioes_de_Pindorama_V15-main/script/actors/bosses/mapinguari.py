import os
import pygame
from script.core.obj import Obj
from script.ui.bosses.hud_mapinguari import BossHudMapinguari


class Boss_Mapinguari(Obj):
    """
    Boss Mapinguari.

    Este boss carrega consigo:
    - nome de exibição
    - HUD específica
    - retrato de morte
    - diálogo de introdução
    - sprites de idle e morte
    """

    # =========================================================
    # ETAPA 1 - METADADOS DO BOSS
    # =========================================================
    DISPLAY_NAME = "Mapinguari"
    HUD_CLASS = BossHudMapinguari
    DEATH_PORTRAIT = os.path.join(
        "assets", "charsSprite", "bosses", "Mapinguari_D.png"
    )

    INTRO_DIALOGUE = [
        ("Cacique", "Jovem guerreiro, esta terra guarda agora uma presença sombria."),
        ("Cacique", "O Mapinguari se ergue diante de você. Mantenha-se firme."),
        ("Jovem Guerreiro", "Se a floresta clama por equilíbrio, lutarei por ela.")
    ]

    def __init__(self, position, groups, size=(400, 400), debug_hitbox=False):
        # ---------------------------------------------------------
        # ETAPA 2 - IMAGEM BASE
        # ---------------------------------------------------------
        image_path = os.path.join("assets", "charsSprite", "bosses", "Mapinguari_1.png")
        super().__init__(image_path, position, groups, size)

        # ---------------------------------------------------------
        # ETAPA 3 - VIDA / ESTADO
        # ---------------------------------------------------------
        self.max_life = 5
        self.life = 5
        self.dead = False
        self.name = self.DISPLAY_NAME

        # Callback seguro para sincronizar HUD
        self.on_life_change = lambda v: None

        # ---------------------------------------------------------
        # ETAPA 4 - ANIMAÇÃO
        # ---------------------------------------------------------
        self.size = size
        self.state = "idle"
        self.current_frame = 0
        self.ticks = 0
        self.animation_speed = 60

        self.animations = {
            "idle": []
        }

        # Idle com os dois frames iniciais definidos
        idle_files = [
            "Mapinguari_1.png",
            "Mapinguari_2.png",
        ]

        for filename in idle_files:
            path = os.path.join("assets", "charsSprite", "bosses", filename)
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, self.size)
            self.animations["idle"].append(img)

        # Imagem inicial
        self.image = self.animations[self.state][self.current_frame]
        self.rect = self.image.get_rect(topleft=position)

        # ---------------------------------------------------------
        # ETAPA 5 - DEBUG E HITBOXES
        # ---------------------------------------------------------
        self.debug_hitbox = debug_hitbox
        self.hitboxes = {"normal": [], "critical": []}
        self._rebuild_hitboxes()

        # ---------------------------------------------------------
        # ETAPA 6 - CONFIGURAÇÃO DE MORTE
        # ---------------------------------------------------------
        death_path = self.DEATH_PORTRAIT
        self.death_image = pygame.image.load(death_path).convert_alpha()
        self.death_image = pygame.transform.scale(self.death_image, self.size)

        self.death_alpha = 255
        self.death_duration = 180   # ~3s a 60fps
        self.death_timer = 0
        self.death_finished = False

    # =========================================================
    # ETAPA 7 - FACTORY / DADOS DO BOSS
    # =========================================================

    @classmethod
    def get_hud_class(cls):
        """
        Retorna a classe de HUD específica deste boss.
        """
        return cls.HUD_CLASS

    @classmethod
    def get_intro_dialogue(cls):
        """
        Retorna o diálogo de introdução deste boss.
        """
        return cls.INTRO_DIALOGUE

    @classmethod
    def get_display_name(cls):
        """
        Retorna o nome exibido na HUD/arena.
        """
        return cls.DISPLAY_NAME

    @classmethod
    def get_death_portrait(cls):
        """
        Retorna o caminho da imagem de morte deste boss.
        """
        return cls.DEATH_PORTRAIT

    # =========================================================
    # ETAPA 8 - HITBOXES
    # =========================================================

    def _rebuild_hitboxes(self):
        """
        Recalcula hitboxes com base no tamanho atual da sprite.
        """
        w, h = self.rect.size

        def R(rel_x, rel_y, rel_w, rel_h):
            rx = self.rect.left + int(rel_x * w)
            ry = self.rect.top + int(rel_y * h)
            rw = int(rel_w * w)
            rh = int(rel_h * h)
            return pygame.Rect(rx, ry, rw, rh)

        # Áreas de dano normal
        normal = [
            R(0.30, 0.22, 0.40, 0.25),  # tronco/peito
            R(0.20, 0.42, 0.60, 0.22),  # abdômen
            R(0.18, 0.64, 0.64, 0.30),  # pernas
        ]

        # Áreas de dano crítico
        critical = [
            R(0.44, 0.08, 0.12, 0.08),  # olho
            R(0.36, 0.30, 0.30, 0.22),  # boca
        ]

        self.hitboxes["normal"] = normal
        self.hitboxes["critical"] = critical

    def draw_hitboxes(self, screen):
        """
        Desenha hitboxes para debug visual.
        """
        if not self.debug_hitbox:
            return

        for rect in self.hitboxes["normal"]:
            pygame.draw.rect(screen, (0, 255, 0), rect, 2)

        for rect in self.hitboxes["critical"]:
            pygame.draw.rect(screen, (255, 0, 0), rect, 2)

    # =========================================================
    # ETAPA 9 - COMBATE
    # =========================================================

    def take_damage(self, amount=1):
        """
        Aplica dano ao boss.
        """
        if self.dead or amount <= 0:
            return

        self.life = max(0, self.life - amount)

        if callable(self.on_life_change):
            self.on_life_change(self.life)

        if self.life <= 0:
            self.die()

    def die(self):
        """
        Entra no estado de morte.
        """
        self.dead = True
        self.state = "dying"

        self.image = self.death_image.copy()
        self.image.set_alpha(self.death_alpha)

        old_midbottom = self.rect.midbottom
        self.rect = self.image.get_rect()
        self.rect.midbottom = old_midbottom

        self._rebuild_hitboxes()

    # =========================================================
    # ETAPA 10 - LOOP
    # =========================================================

    def update(self):
        """
        Atualiza o boss.
        """
        if self.state == "dying":
            self._update_death()
            return

        self.animate(self.state)

    def _update_death(self):
        """
        Atualiza o fade da morte.
        """
        if self.death_finished:
            return

        self.death_timer += 1

        step = int(255 / max(1, self.death_duration))
        self.death_alpha = max(0, self.death_alpha - step)
        self.image.set_alpha(self.death_alpha)

        if self.death_timer >= self.death_duration:
            self.death_finished = True
            self.kill()

            try:
                self.on_death_finished()
            except Exception:
                pass

    def animate(self, name):
        """
        Atualiza a animação do boss.
        """
        if name not in self.animations or not self.animations[name]:
            return

        self.ticks += 1

        if self.ticks >= self.animation_speed:
            self.ticks = 0
            self.current_frame = (self.current_frame + 1) % len(self.animations[name])

            old_midbottom = self.rect.midbottom
            self.image = self.animations[name][self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.midbottom = old_midbottom

            self._rebuild_hitboxes()

    # =========================================================
    # ETAPA 11 - INTERAÇÃO
    # =========================================================

    def interact(self, player):
        """
        Interação básica do boss com o jogador.
        """
        if self.rect.colliderect(player.rect):
            print("Mapinguari: VOCÊ ATRAVESSOU OS LIMITES! PREPARE-SE PARA LUTAR.")