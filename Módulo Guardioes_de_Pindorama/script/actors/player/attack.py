import random
import pygame
from script.combat.projectiles import Shot


class PlayerAttackController:
    """
    Classe responsável por controlar toda a lógica de ataque do jogador.

    Esta classe cuida de:
    - identificar a postura do ataque
    - iniciar o tiro normal
    - iniciar a preparação do charge shot
    - liberar o charge shot ao soltar o botão
    - controlar a animação de disparo
    - criar a flecha real
    """

    # =========================================================
    # ETAPA 1 - CONFIGURAÇÕES GERAIS DO ATAQUE
    # =========================================================

    # Tecla de ataque
    ATTACK_KEY = pygame.K_q

    # Tempo mínimo para considerar o disparo como carregado
    CHARGE_THRESHOLD_MS = 350

    # Tempo máximo de carga
    MAX_CHARGE_MS = 1200

    # Dano do tiro normal
    NORMAL_SHOT_DAMAGE = 1

    # Dano aleatório do charge shot
    CHARGE_SHOT_MIN_DAMAGE = 2
    CHARGE_SHOT_MAX_DAMAGE = 4

    def __init__(self, player):
        """
        Inicializa o controlador de ataque.

        player:
            referência para a classe Player
        """
        self.player = player

        # =========================================================
        # ETAPA 2 - GRUPO DE PROJÉTEIS
        # =========================================================

        # Grupo que armazena todas as flechas disparadas
        self.shots = pygame.sprite.Group()

        # =========================================================
        # ETAPA 3 - CONTROLE DO BOTÃO DE ATAQUE
        # =========================================================

        # Indica se o botão de ataque está pressionado
        self.attack_holding = False

        # Armazena o instante em que o botão foi pressionado
        self.attack_press_time = 0

        # Tempo atual de carga do disparo
        self.attack_charge_time = 0

        # Informa se já passou do limiar de Charge Shot
        self.charge_ready = False

        # Indica se o sistema entrou em modo de mira
        self.aim_started = False

        # =========================================================
        # ETAPA 4 - CONTROLE DE DISPARO
        # =========================================================

        # Evita criar dois projéteis na mesma animação
        self.shot_released = False

        # Guarda dados do disparo que será criado
        self.pending_shot_data = None

        # =========================================================
        # ETAPA 5 - OFFSETS E VELOCIDADES
        # =========================================================

        # Define a posição em que a flecha nasce em relação ao player
        self.shot_offsets = {
            "stand": {
                "right": (80, 60),
                "left": (30, 60)
            },
            "crouch": {
                "right": (70, 105),
                "left": (20, 90)
            },
            "jump": {
                "right": (80, 55),
                "left": (30, 55)
            },
        }

        # Define a velocidade do projétil em cada postura
        self.shot_speed = {
            "stand": 7,
            "crouch": 6,
            "jump": 7
        }

    # =========================================================
    # ETAPA 6 - IDENTIFICAR A POSTURA DO DISPARO
    # =========================================================

    def get_shot_stance(self):
        """
        Retorna a postura atual do disparo:

        - "stand"  -> em pé
        - "crouch" -> agachado
        - "jump"   -> no ar / pulando
        """
        if self.player.is_jumping or not self.player.on_ground:
            return "jump"
        if self.player.crouching:
            return "crouch"
        return "stand"

    # =========================================================
    # ETAPA 7 - TIRO NORMAL
    # =========================================================

    def start_attack(self):
        """
        Inicia o tiro normal.

        Este método é usado para:
        - clique curto
        - sem passar pelo estado de mira
        - executa um ciclo único de animação
        """
        if (
            self.player.blocking
            or self.player.rolling
            or self.player.is_dead
            or self.attack_holding
            or self.player.state in {
                "aim", "c_aim", "jump_aim",
                "shot", "c_shot", "jump_shot",
                "charge_shot", "c_charge_shot", "jump_charge_shot",
            }
        ):
            return

        stance = self.get_shot_stance()

        # Define o estado visual do tiro normal
        if stance == "jump":
            self.player.state = "jump_shot"
        elif stance == "crouch":
            self.player.state = "c_shot"
        else:
            self.player.state = "shot"

        # Guarda os dados do projétil
        self.pending_shot_data = {
            "stance": stance,
            "charged": False,
        }

        # Reinicia o ciclo da animação
        self.shot_released = False
        self.player.img = 0
        self.player.ticks = 0

    # =========================================================
    # ETAPA 8 - INÍCIO DO CHARGE SHOT
    # =========================================================

    def start_attack_hold(self):
        """
        Inicia a preparação do charge shot ao pressionar Q.

        IMPORTANTE:
        - ainda NÃO entra em mira imediatamente
        - apenas começa a contar o tempo segurando o botão
        """
        if (
            self.player.blocking
            or self.player.rolling
            or self.player.is_dead
            or self.attack_holding
            or self.player.state in {
                "aim", "c_aim", "jump_aim",
                "shot", "c_shot", "jump_shot",
                "charge_shot", "c_charge_shot", "jump_charge_shot",
            }
        ):
            return

        self.attack_holding = True
        self.attack_press_time = pygame.time.get_ticks()

        self.attack_charge_time = 0
        self.charge_ready = False
        self.aim_started = False

        self.shot_released = False
        self.pending_shot_data = None

    # =========================================================
    # ETAPA 9 - SOLTAR O CHARGE SHOT
    # =========================================================

    def release_attack_hold(self):
        """
        Resolve o ataque ao soltar Q.

        Regras:
        - se NÃO carregou o suficiente -> vira tiro normal
        - se carregou -> libera o charge shot
        """
        if not self.attack_holding:
            return

        self.attack_holding = False

        now = pygame.time.get_ticks()
        held_ms = now - self.attack_press_time
        is_charge = held_ms >= self.CHARGE_THRESHOLD_MS

        stance = self.get_shot_stance()

        # Se não virou charge, executa o tiro curto
        if not is_charge:
            self.charge_ready = False
            self.aim_started = False
            self.start_attack()
            return

        # Se virou charge, agora solta o disparo carregado
        if stance == "jump":
            self.player.state = "jump_charge_shot"
        elif stance == "crouch":
            self.player.state = "c_charge_shot"
        else:
            self.player.state = "charge_shot"

        self.pending_shot_data = {
            "stance": stance,
            "charged": True,
        }

        self.shot_released = False
        self.player.img = 0
        self.player.ticks = 0
        self.aim_started = False

    # =========================================================
    # ETAPA 10 - ATUALIZAR TEMPO DE CARGA
    # =========================================================

    def update_charge(self):
        """
        Atualiza o tempo de carga enquanto Q estiver pressionado.

        Quando passa do limiar:
        - entra em modo de mira
        - trava na pose S3 / S_D3
        """
        if not self.attack_holding:
            return

        now = pygame.time.get_ticks()
        self.attack_charge_time = min(now - self.attack_press_time, self.MAX_CHARGE_MS)

        # Quando cruza o limiar, entra em mira uma única vez
        if not self.charge_ready and self.attack_charge_time >= self.CHARGE_THRESHOLD_MS:
            self.charge_ready = True
            self.aim_started = True

            stance = self.get_shot_stance()

            if stance == "jump":
                self.player.state = "jump_aim"
            elif stance == "crouch":
                self.player.state = "c_aim"
            else:
                self.player.state = "aim"

            self.player.img = 0
            self.player.ticks = 0

    # =========================================================
    # ETAPA 11 - MANTER A MIRA
    # =========================================================

    def update_aim_state(self):
        """
        Mantém o estado de mira apenas quando o charge já está pronto.
        """
        if not self.attack_holding or not self.charge_ready:
            return

        stance = self.get_shot_stance()

        if stance == "jump":
            self.player.state = "jump_aim"
        elif stance == "crouch":
            self.player.state = "c_aim"
        else:
            self.player.state = "aim"

    # =========================================================
    # ETAPA 12 - ATUALIZAR ANIMAÇÃO DE ATAQUE
    # =========================================================

    def update_attack_animation(self):
        """
        Atualiza a animação de mira e disparo.
        """
        p = self.player

        # ---------------------------------------------------------
        # Miras
        # ---------------------------------------------------------

        # Mira em pé = sprite S3
        if p.state == "aim":
            p.animate("aim_right" if p.facing_right else "aim_left", 80, 1)

        # Mira agachado = sprite S_D3
        elif p.state == "c_aim":
            p.animate("c_aim_right" if p.facing_right else "c_aim_left", 80, 1)

        # Mira no ar
        elif p.state == "jump_aim":
            p.animate("jump_aim_right" if p.facing_right else "jump_aim_left", 80, 1)

        # ---------------------------------------------------------
        # Tiros normais
        # ---------------------------------------------------------

        elif p.state == "shot":
            p.animate("shot_right" if p.facing_right else "shot_left", 3, 7)

        elif p.state == "c_shot":
            p.animate("c_shot_right" if p.facing_right else "c_shot_left", 3, 7)

        elif p.state == "jump_shot":
            p.animate("jump_shot_right" if p.facing_right else "jump_shot_left", 3, 7)

        # ---------------------------------------------------------
        # Charge Shots
        # ---------------------------------------------------------

        # O charge shot já começa em S4 / S_D4
        elif p.state == "charge_shot":
            p.animate("charge_shot_right" if p.facing_right else "charge_shot_left", 5, 7)

        elif p.state == "c_charge_shot":
            p.animate("c_charge_shot_right" if p.facing_right else "c_charge_shot_left", 5, 7)

        elif p.state == "jump_charge_shot":
            p.animate("jump_charge_shot_right" if p.facing_right else "jump_charge_shot_left", 5, 7)

    # =========================================================
    # ETAPA 13 - EVENTOS DA ANIMAÇÃO
    # =========================================================

    def handle_animation_events(self, anim_name, num_frames):
        """
        Trata eventos especiais da animação.

        Regras:
        - tiro curto: flecha sai no frame 4
        - charge shot: flecha sai no frame 0 da sequência pós-mira
        - ao terminar a animação, volta ao estado adequado
        """
        short_shot_anim_names = {
            "shot_right", "shot_left",
            "c_shot_right", "c_shot_left",
            "jump_shot_right", "jump_shot_left",
        }

        charge_shot_anim_names = {
            "charge_shot_right", "charge_shot_left",
            "c_charge_shot_right", "c_charge_shot_left",
            "jump_charge_shot_right", "jump_charge_shot_left",
        }

        all_shot_anim_names = short_shot_anim_names | charge_shot_anim_names

        # ---------------------------------------------------------
        # Tiro curto: dispara no frame 4
        # ---------------------------------------------------------
        if (
            anim_name in short_shot_anim_names
            and self.player.img == 4
            and not self.shot_released
        ):
            self.real_shot()
            self.shot_released = True

        # ---------------------------------------------------------
        # Charge shot: dispara no primeiro frame da sequência pós-mira
        # ---------------------------------------------------------
        if (
            anim_name in charge_shot_anim_names
            and self.player.img == 0
            and not self.shot_released
        ):
            self.real_shot()
            self.shot_released = True

        # ---------------------------------------------------------
        # Fim da animação: volta ao estado adequado
        # ---------------------------------------------------------
        if self.player.img >= num_frames - 1 and anim_name in all_shot_anim_names:
            self.shot_released = False

            if self.player.crouching and self.player.on_ground:
                self.player.state = "down"
            elif not self.player.on_ground:
                self.player.state = "jump"
            else:
                self.player.state = "idle"

    # =========================================================
    # ETAPA 14 - CRIAR A FLECHA REAL
    # =========================================================

    def real_shot(self):
        """
        Cria a flecha real.

        Regras:
        - tiro normal = 1 de dano
        - charge shot = random entre 2 e 4
        """
        if not self.pending_shot_data:
            stance = self.get_shot_stance()
            charged = self.player.state in {
                "charge_shot", "c_charge_shot", "jump_charge_shot"
            }
        else:
            stance = self.pending_shot_data["stance"]
            charged = self.pending_shot_data["charged"]

        side = "right" if self.player.facing_right else "left"
        dx, dy = self.shot_offsets[stance][side]
        speed = self.shot_speed.get(stance, 7)

        if charged:
            damage = random.randint(
                self.CHARGE_SHOT_MIN_DAMAGE,
                self.CHARGE_SHOT_MAX_DAMAGE
            )
        else:
            damage = self.NORMAL_SHOT_DAMAGE

        print(f"[DEBUG] stance={stance} | charged={charged} | state={self.player.state}")

        shot_x = self.player.rect.x + dx
        shot_y = self.player.rect.y + dy
        direction = 1 if self.player.facing_right else -1

        shot = Shot(
            shot_x,
            shot_y,
            direction,
            self.shots,
            size=(80, 25),
            speed=speed,
            damage=damage,
            charged=charged
        )

        self.shots.add(shot)
        self.pending_shot_data = None

    # =========================================================
    # ETAPA 15 - ATUALIZAR PROJÉTEIS
    # =========================================================

    def update_projectiles(self):
        """
        Atualiza todas as flechas disparadas pelo jogador.
        """
        self.shots.update()