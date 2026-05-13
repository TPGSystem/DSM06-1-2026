import os
import pygame
import random
from script.core.obj import Obj
from script.ui.bosses.hud_mapinguari import BossHudMapinguari


class Boss_Mapinguari(Obj):
    """
    Boss Mapinguari.

    Funções principais deste arquivo:
    - carregar os metadados do boss;
    - carregar sprites de idle, caminhada, investida e morte;
    - localizar automaticamente o Player dentro do grupo de sprites;
    - executar comportamento aleatório entre caminhar e investir contra o jogador;
    - memorizar a posição do Player antes de agir, evitando perseguição contínua;
    - controlar vida, dano, morte e hitboxes.

    IMPORTANTE:
    Como o boss pode ser sorteado pela fase, ele NÃO depende de:
        self.mapinguari.set_target(self.player)

    Em vez disso, o próprio Mapinguari procura automaticamente o Player
    dentro dos grupos de sprites aos quais ele pertence.
    """

    # =========================================================
    # ETAPA 1 - METADADOS DO BOSS
    # =========================================================
    DISPLAY_NAME = "Mapinguari"
    HUD_CLASS = BossHudMapinguari
    DEATH_PORTRAIT = os.path.join(
        "assets", "charsSprite", "bosses", "M_D.png"
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
        # Esta imagem é usada apenas para inicializar o Obj.
        # Depois disso, a imagem exibida passa a ser controlada
        # pelo dicionário self.animations.
        image_path = os.path.join("assets", "charsSprite", "bosses", "M_I1.png")
        super().__init__(image_path, position, groups, size)

        # ---------------------------------------------------------
        # ETAPA 3 - VIDA / ESTADO GERAL
        # ---------------------------------------------------------
        self.max_life = 5
        self.life = 5
        self.dead = False
        self.name = self.DISPLAY_NAME

        # Callback seguro para sincronizar a HUD.
        # Se a HUD ainda não estiver conectada, não causa erro.
        self.on_life_change = lambda v: None

        # ---------------------------------------------------------
        # ETAPA 4 - LOCALIZAÇÃO DO PLAYER
        # ---------------------------------------------------------
        # Como o boss é sorteado pela fase, o Player não é passado
        # manualmente. O Mapinguari irá procurá-lo no grupo de sprites.
        self.target = None

        # ---------------------------------------------------------
        # ETAPA 5 - TEMPOS DE ESPERA
        # ---------------------------------------------------------
        # Espera inicial: o boss aparece na tela, fica parado em idle
        # por alguns segundos e só depois começa a agir.
        self.start_delay_ms = 5000
        self.start_waiting = True
        self.start_wait_time = None

        # Espera após chegar ao ponto marcado: depois de caminhar ou investir,
        # o Mapinguari para, olha para o Player e aguarda antes de sortear
        # uma nova ação.
        self.waiting_at_point = False
        self.wait_start_time = 0
        self.wait_after_arrival_ms = 5000

        # ---------------------------------------------------------
        # ETAPA 6 - MEMÓRIA DE POSIÇÃO
        # ---------------------------------------------------------
        # O Mapinguari NÃO deve perseguir o Player em tempo real.
        # Ele memoriza onde o Player estava no momento da decisão
        # e vai até esse ponto, mesmo que o jogador fuja.
        self.memory_x = None
        self.run_target_x = None

        # Margens pequenas para considerar que o boss chegou ao destino.
        self.arrival_distance = 5
        self.run_arrival_distance = 10

        # ---------------------------------------------------------
        # ETAPA 7 - AÇÕES E VELOCIDADES
        # ---------------------------------------------------------
        # action guarda a ação sorteada no ciclo atual:
        # - "walk": caminhar até o ponto memorizado;
        # - "run_attack": investir/correr até o ponto memorizado.
        self.action = None

        # Velocidades separadas para equilibrar as ações.
        self.walk_speed = 2
        self.run_speed = 8

        # Direção visual inicial.
        # False = olhando para a esquerda; True = olhando para a direita.
        # Suas sprites originais estão voltadas para a esquerda,
        # então só fazemos flip quando facing_right for True.
        self.facing_right = False

        # ---------------------------------------------------------
        # ETAPA 8 - ANIMAÇÃO
        # ---------------------------------------------------------
        self.size = size
        self.state = "idle"
        self.current_frame = 0
        self.ticks = 0

        # Velocidade de animação por estado.
        # Quanto menor o valor, mais rápida a troca de frames.
        self.animation_speeds = {
            "idle": 30,
            "walk": 10,
            "run_attack": 8
        }

        # Dicionário central de animações do boss.
        self.animations = {
            "idle": [],
            "walk": [],
            "run_attack": []
        }

        # Carrega todas as animações antes de definir a imagem inicial.
        self._load_animations()

        # Imagem inicial exibida na tela.
        self.image = self.animations[self.state][self.current_frame]
        self.rect = self.image.get_rect(topleft=position)

        # ---------------------------------------------------------
        # ETAPA 9 - DEBUG E HITBOXES
        # ---------------------------------------------------------
        self.debug_hitbox = debug_hitbox
        self.hitboxes = {"normal": [], "critical": []}
        self._rebuild_hitboxes()

        # ---------------------------------------------------------
        # ETAPA 10 - CONFIGURAÇÃO DE MORTE
        # ---------------------------------------------------------
        death_path = self.DEATH_PORTRAIT
        self.death_image = pygame.image.load(death_path).convert_alpha()
        self.death_image = pygame.transform.scale(self.death_image, self.size)

        self.death_alpha = 255
        self.death_duration = 180   # aproximadamente 3 segundos a 60 FPS
        self.death_timer = 0
        self.death_finished = False

    # =========================================================
    # ETAPA 11 - CARREGAMENTO DE ANIMAÇÕES
    # =========================================================

    def _load_animations(self):
        """
        Carrega as animações do Mapinguari.

        Os arquivos precisam estar em:
            assets/charsSprite/bosses/
        """
        # Idle/parado.
        idle_files = [
            "M_I1.png",
            "M_I2.png",
        ]

        # Caminhada normal.
        walk_files = [
            "M_M1.png",
            "M_M2.png",
            "M_M3.png",
            "M_M4.png",
            "M_M5.png",
            "M_M6.png",
        ]

        # Investida/corrida de ataque.
        # Ajuste os nomes se seus arquivos tiverem outro padrão.
        run_attack_files = [
            "M_R1.png",
            "M_R2.png",
        ]

        self.animations["idle"] = self._load_frames(idle_files)
        self.animations["walk"] = self._load_frames(walk_files)
        self.animations["run_attack"] = self._load_frames(run_attack_files)

    def _load_frames(self, filenames):
        """
        Recebe uma lista de nomes de arquivos e devolve uma lista
        de imagens carregadas e redimensionadas.
        """
        frames = []

        for filename in filenames:
            path = os.path.join("assets", "charsSprite", "bosses", filename)
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, self.size)
            frames.append(img)

        return frames

    # =========================================================
    # ETAPA 12 - LOCALIZAÇÃO AUTOMÁTICA DO PLAYER
    # =========================================================

    def find_player(self):
        """
        Procura automaticamente o Player dentro dos grupos de sprites.

        Requisito:
        - Player e Mapinguari precisam estar em pelo menos um mesmo grupo,
          normalmente self.all_sprites.
        """
        if self.target is not None:
            return

        for group in self.groups():
            for sprite in group:
                if sprite is self:
                    continue

                # Evita import circular.
                # Em vez de importar Player, verificamos o nome da classe.
                if sprite.__class__.__name__ == "Player":
                    self.target = sprite
                    return

    def set_target(self, player):
        """
        Método opcional.

        Pode ser usado caso, futuramente, você queira definir o Player
        manualmente. Para boss sorteado, find_player() já resolve.
        """
        self.target = player

    # =========================================================
    # ETAPA 13 - COMPORTAMENTO PRINCIPAL DO BOSS
    # =========================================================

    def follow_player(self):
        """
        Comportamento do Mapinguari:

        1. Espera 5 segundos no início.
        2. Sorteia uma ação:
           - caminhar até a posição memorizada do Player;
           - investir correndo até a posição memorizada do Player.
        3. Executa a ação sem recalcular o destino no meio do caminho.
        4. Para por 5 segundos olhando para o Player.
        5. Limpa a ação e sorteia uma nova no próximo ciclo.
        """
        self.find_player()

        if not self.target:
            self.state = "idle"
            return

        now = pygame.time.get_ticks()

        # ---------------------------------------------------------
        # 13.1 - ESPERA INICIAL REAL
        # ---------------------------------------------------------
        # A espera começa no primeiro update real do boss,
        # e não necessariamente no momento em que o objeto foi criado.
        if self.start_waiting:
            self._look_at_player()
            self.state = "idle"

            if self.start_wait_time is None:
                self.start_wait_time = now
                return

            if now - self.start_wait_time < self.start_delay_ms:
                return

            self.start_waiting = False

        # ---------------------------------------------------------
        # 13.2 - ESPERA APÓS CHEGAR AO DESTINO
        # ---------------------------------------------------------
        # Enquanto espera, não recalcula ação nem destino.
        # Apenas fica parado em idle olhando para o Player.
        if self.waiting_at_point:
            self._look_at_player()
            self.state = "idle"

            if now - self.wait_start_time >= self.wait_after_arrival_ms:
                self._reset_action_cycle()

            return

        # ---------------------------------------------------------
        # 13.3 - SORTEIO DE AÇÃO
        # ---------------------------------------------------------
        # Só sorteia uma ação quando não existe uma ação ativa.
        # Neste momento, grava a posição atual do Player.
        if self.action is None:
            self.action = random.choice(["walk", "run_attack"])

            self.memory_x = self.target.rect.centerx
            self.run_target_x = self.target.rect.centerx

        # ---------------------------------------------------------
        # 13.4 - EXECUÇÃO DA AÇÃO SORTEADA
        # ---------------------------------------------------------
        if self.action == "walk":
            self._walk_to_memory_point(now)
        elif self.action == "run_attack":
            self._run_attack_to_memory_point(now)

    def _reset_action_cycle(self):
        """
        Limpa a ação atual para permitir que o boss sorteie
        uma nova ação no próximo ciclo.
        """
        self.waiting_at_point = False
        self.memory_x = None
        self.run_target_x = None
        self.action = None

    def _look_at_player(self):
        """
        Vira o Mapinguari para olhar para o Player.
        Usado durante idle inicial e espera após chegar ao destino.
        """
        if not self.target:
            return

        self.facing_right = self.target.rect.centerx > self.rect.centerx

    def _start_wait_at_point(self, now):
        """
        Coloca o Mapinguari em estado de espera após chegar
        ao ponto memorizado.
        """
        self._look_at_player()
        self.state = "idle"
        self.waiting_at_point = True
        self.wait_start_time = now
        self._rebuild_hitboxes()

    def _walk_to_memory_point(self, now):
        """
        Caminha até a posição memorizada do Player.
        A posição NÃO é atualizada durante o deslocamento.
        """
        distance_x = self.memory_x - self.rect.centerx

        if abs(distance_x) <= self.arrival_distance:
            self.rect.centerx = self.memory_x
            self._start_wait_at_point(now)
            return

        if distance_x > 0:
            self.rect.x += self.walk_speed
            self.facing_right = True
        else:
            self.rect.x -= self.walk_speed
            self.facing_right = False

        self.state = "walk"
        self._rebuild_hitboxes()

    def _run_attack_to_memory_point(self, now):
        """
        Faz o Mapinguari investir correndo até a posição memorizada do Player.
        Ele NÃO recalcula a posição durante a corrida.
        """
        distance_x = self.run_target_x - self.rect.centerx

        if abs(distance_x) <= self.run_arrival_distance:
            self.rect.centerx = self.run_target_x
            self._start_wait_at_point(now)
            return

        if distance_x > 0:
            self.rect.x += self.run_speed
            self.facing_right = True
        else:
            self.rect.x -= self.run_speed
            self.facing_right = False

        self.state = "run_attack"
        self._rebuild_hitboxes()

    # =========================================================
    # ETAPA 14 - FACTORY / DADOS DO BOSS
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
        Retorna o caminho da imagem de morte.
        """
        return cls.DEATH_PORTRAIT

    # =========================================================
    # ETAPA 15 - HITBOXES
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

        self.hitboxes["normal"] = [
            R(0.30, 0.22, 0.40, 0.25),  # tronco/peito
            R(0.20, 0.42, 0.60, 0.22),  # abdômen
            R(0.18, 0.64, 0.64, 0.30),  # pernas
        ]

        self.hitboxes["critical"] = [
            R(0.44, 0.08, 0.12, 0.08),  # olho
            R(0.36, 0.30, 0.30, 0.22),  # boca
        ]

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
    # ETAPA 16 - COMBATE
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
    # ETAPA 17 - LOOP PRINCIPAL DO BOSS
    # =========================================================

    def update(self):
        """
        Atualiza o boss a cada frame.
        """
        if self.state == "dying":
            self._update_death()
            return

        if self.dead:
            return

        self.follow_player()
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

        Preserva o midbottom para evitar que a sprite "pule"
        quando troca de frame, principalmente se as imagens tiverem
        tamanhos diferentes.
        """
        if name not in self.animations or not self.animations[name]:
            return

        speed = self.animation_speeds.get(name, 60)

        self.ticks += 1

        if self.ticks >= speed:
            self.ticks = 0
            self.current_frame = (self.current_frame + 1) % len(self.animations[name])

            old_midbottom = self.rect.midbottom
            self.image = self.animations[name][self.current_frame]

            # A sprite original do Mapinguari está virada para a esquerda.
            # Por isso, só espelhamos quando ele precisa olhar para a direita.
            if self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

            self.rect = self.image.get_rect()
            self.rect.midbottom = old_midbottom

            self._rebuild_hitboxes()

    # =========================================================
    # ETAPA 18 - INTERAÇÃO
    # =========================================================

    def interact(self, player):
        """
        Interação básica do boss com o jogador.
        """
        if self.rect.colliderect(player.rect):
            print("Mapinguari: VOCÊ ATRAVESSOU OS LIMITES! PREPARE-SE PARA LUTAR.")
