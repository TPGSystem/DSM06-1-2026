import random
import pygame

# Importa a classe base dos levels
from .level_base import Level

# Importa o registro geral de bosses do jogo
from script.data.bosses.boss_registry import BOSS_REGISTRY

# Importa os diálogos específicos desta fase
from script.data.dialogs.dialog_1_2 import Dialogo_1_2
from script.data.dialogs.dialog_1_3 import Dialogo_1_3

# Importa a decisão narrativa específica desta fase
from script.data.decisions.decision_1_2 import Decisão_1_2

# Importa as classes de camadas visuais
from script.layer_anim import StaticLayer, FlipLayer

# Importa constantes do projeto
from script.setting import *

# Importa a cena de Game Over
from ..gameover import GameOver

# Importa o estado global do jogo
from script.game_state import STATE


class Level_VC_1_2(Level):
    """
    Fase 1_2 da região Vilarejo de Canaã.

    Fluxo desta fase:
    1. Diálogo inicial
    2. Combate contra o boss
    3. Diálogo final antes da decisão
    4. Decisão narrativa (SIM / NÃO)
    5. Diálogo final após a escolha
    6. Retorno ao mapa com a decisão salva no STATE
    """

    def __init__(self, player_data=None, hud_data=None):
        # Inicializa a estrutura base do level
        super().__init__(player_data, hud_data)

        # ---------------------------------------------------------
        # ETAPA 1 - CONTROLE GERAL DA FASE
        # ---------------------------------------------------------
        # Impede a saída automática da classe base
        self.disable_auto_exit = True

        # A saída só será liberada após derrotar o boss
        self.exit_enabled = False

        # O player não pode atravessar a tela até a saída ser liberada
        setattr(self.player, "exit_mode", False)

        # Enquanto o diálogo inicial estiver ativo, não há combate
        self.combat_enabled = False

        # ---------------------------------------------------------
        # ETAPA 2 - CAMADAS DO CENÁRIO
        # ---------------------------------------------------------
        base_path = "assets/levelSprite/Level_1_2/"

        # Fundo principal
        self.layers.add(
            "level_1_2",
            StaticLayer(f"{base_path}level_1_2.png", z=0, plane="back", pos=(0, 0))
        )

        # Camada complementar de fundo
        self.layers.add(
            "level_1_2a",
            StaticLayer(f"{base_path}level_1_2a.png", z=10, plane="back", pos=(0, 0))
        )

        # Água animada
        self.layers.add(
            "level_1_2ba_bb",
            FlipLayer(
                f"{base_path}level_1_2ba.png",
                f"{base_path}level_1_2bb.png",
                fps=4.0,
                z=20,
                plane="back",
                pos=(0, 0)
            )
        )

        # Camada frontal
        self.layers.add(
            "level_1_2c",
            StaticLayer(f"{base_path}level_1_2c.png", z=10, plane="front", pos=(0, 0))
        )

        # ---------------------------------------------------------
        # ETAPA 3 - POSIÇÃO INICIAL DO PLAYER
        # ---------------------------------------------------------
        self.player.rect.x = 100
        self.player.rect.y = 250

        # ---------------------------------------------------------
        # ETAPA 4 - CHATBOX DA FASE
        # ---------------------------------------------------------
        self.chatbox.set_dialog_images(
            "assets/chatChar/level_1_2",
            pygame.Rect(100, 410, 1080, 250)
        )

        # ---------------------------------------------------------
        # ETAPA 5 - CONTROLE DO FLUXO NARRATIVO
        # ---------------------------------------------------------
        # Diálogo inicial
        self.intro_started = False
        self.intro_finished = False
        self.intro_dialogue = Dialogo_1_2.falas

        # Diálogo final em partes
        self.final_dialogue_before_choice = Dialogo_1_3.falas_antes_decisao
        self.final_dialogue_after_yes = Dialogo_1_3.falas_depois_sim
        self.final_dialogue_after_no = Dialogo_1_3.falas_depois_nao

        # Estrutura de decisão narrativa
        self.final_choice_data = Decisão_1_2.perguntas[0]

        # Flags de controle do fechamento da fase
        self.final_dialogue_started = False
        self.final_dialogue_finished = False
        self.choice_started = False
        self.choice_finished = False

        # Guarda a decisão tomada pelo jogador
        self.player_choice = None

        # ---------------------------------------------------------
        # ETAPA 6 - SORTEIO DO BOSS
        # ---------------------------------------------------------
        BossClass = random.choice(BOSS_REGISTRY)

        self.boss_name = BossClass.get_display_name()
        self.death_portrait = BossClass.get_death_portrait()
        HudClass = BossClass.get_hud_class()

        # ---------------------------------------------------------
        # ETAPA 7 - INSTÂNCIA DO BOSS
        # ---------------------------------------------------------
        self.boss = BossClass(
            [850, 100],
            [self.all_sprites],
            size=(400, 400)
        )

        # ---------------------------------------------------------
        # ETAPA 8 - HUD DO BOSS
        # ---------------------------------------------------------
        self.boss_hud = HudClass(position=(0, 0), size=(1280, 720))
        self.boss_hud.set(getattr(self.boss, "life", 5))

        if hasattr(self.boss, "on_life_change"):
            self.boss.on_life_change = self.boss_hud.set

        self.boss_name_font = pygame.font.Font("assets/font/Primitive.ttf", 28)
        self.boss_name_text = self.boss_name_font.render(self.boss_name, True, (0, 0, 0))
        self.boss_name_pos = (880, 600)

        # ---------------------------------------------------------
        # ETAPA 9 - CONTROLE DE MORTE DO BOSS
        # ---------------------------------------------------------
        self.boss_defeated = False
        self.boss_dying = False

        self.boss_corpse = None
        self.boss_corpse_rect = None
        self.boss_corpse_alpha = 255
        self.boss_corpse_fade_frames = 180
        self._boss_corpse_timer = 0

        self._load_boss_corpse()

        # ---------------------------------------------------------
        # ETAPA 10 - INICIAR DIÁLOGO AUTOMATICAMENTE
        # ---------------------------------------------------------
        self.start_intro_dialogue()

    def _load_boss_corpse(self):
        """
        Carrega a imagem de morte do boss.
        """
        try:
            corpse_img = pygame.image.load(self.death_portrait).convert_alpha()
            corpse_img = pygame.transform.scale(corpse_img, (400, 400))
            self.boss_corpse = corpse_img
        except Exception as e:
            print("[WARN] Não foi possível carregar a imagem de morte do boss:", e)
            self.boss_corpse = None
            
    def get_boss_hurtbox(self):
        """
        Retorna uma hurtbox menor que o rect total do boss,
        aproximando a colisão da área central do desenho.
        """
        if not self.boss:
            return pygame.Rect(0, 0, 0, 0)

        # Começa com o rect visual do boss
        rect = self.boss.rect.copy()

        # Ajuste fino da área de acerto:
        # - reduz laterais
        # - reduz topo
        # - reduz base
        #
        # Ajuste estes valores conforme o tamanho real do sprite
        rect.x += 135
        rect.y += 55
        rect.width -= 210
        rect.height -= 110

        return rect        

    def start_intro_dialogue(self):
        """
        Inicia automaticamente o diálogo introdutório da fase.
        """
        formatted_dialogue = [
            f"{speaker}: {message}" for speaker, message in self.intro_dialogue
        ]

        # Garante que o chatbox esteja em modo de diálogo
        self.chatbox.options = []
        self.chatbox.title = ""
        self.chatbox.question = ""

        self.chatbox.set_frame_offset(0)
        self.chatbox.display_messages(formatted_dialogue)
        self.chatbox.active = True

        self.intro_started = True
        self.intro_finished = False
        self.combat_enabled = False

    def start_final_dialogue_before_choice(self):
        """
        Inicia o diálogo final ANTES da decisão do jogador.
        """
        formatted_dialogue = [
            f"{speaker}: {message}" for speaker, message in self.final_dialogue_before_choice
        ]

        # Garante que o chatbox esteja em modo de diálogo
        self.chatbox.options = []
        self.chatbox.title = ""
        self.chatbox.question = ""

        self.chatbox.set_frame_offset(12)
        self.chatbox.display_messages(formatted_dialogue)
        self.chatbox.active = True

        self.final_dialogue_started = True
        self.final_dialogue_finished = False
        self.choice_started = False

        # Durante o diálogo final, trava a saída
        self.exit_enabled = False
        setattr(self.player, "exit_mode", False)

    def start_final_choice(self):
        """
        Abre a tomada de decisão narrativa SIM / NÃO.
        Aqui não existe resposta correta: apenas escolha do jogador.
        """
        self.chatbox.set_frame_offset(20)
        self.chatbox.display_decision(
            self.final_choice_data["titulo"],
            self.final_choice_data["pergunta"],
            self.final_choice_data["opcoes"]
        )
        self.choice_started = True

    def start_final_dialogue_after_choice(self):
        """
        Inicia o diálogo final DEPOIS da escolha do jogador.
        O texto e o frame_offset mudam conforme a decisão tomada.
        """
        choice = (self.player_choice or "").strip().upper()

        if choice.startswith("SIM"):
            selected_dialogue = self.final_dialogue_after_yes
            frame_offset = 21
        else:
            selected_dialogue = self.final_dialogue_after_no
            frame_offset = 23

        formatted_dialogue = [
            f"{speaker}: {message}" for speaker, message in selected_dialogue
        ]

        # Limpa o modo de decisão antes de voltar ao modo diálogo
        self.chatbox.options = []
        self.chatbox.title = ""
        self.chatbox.question = ""

        # Define o bloco correto de sprites para cada escolha
        self.chatbox.set_frame_offset(frame_offset)
        self.chatbox.display_messages(formatted_dialogue)
        self.chatbox.active = True

    def save_player_choice(self):
        """
        Salva a decisão do jogador no estado global do jogo.
        O mapa poderá usar essa flag depois.
        """
        choice = (self.player_choice or "").strip().upper()

        if choice.startswith("SIM"):
            STATE.set_flag("seguir_vale_luz_sombra", True)
        else:
            STATE.set_flag("seguir_vale_luz_sombra", False)

    def handle_events(self, event):
        """
        Processa os eventos da fase:
        - diálogo inicial
        - tomada de decisão
        - diálogo final após a escolha
        """
        super().handle_events(event)

        if self.overlay:
            return

        if self.chatbox and self.chatbox.is_active():
            if event.type == pygame.KEYDOWN:

                # -------------------------------------------------
                # MODO DECISÃO (quando existem opções SIM / NÃO)
                # -------------------------------------------------
                if self.chatbox.options:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.chatbox.previous_option()
                        return

                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.chatbox.next_option()
                        return

                    elif event.key == pygame.K_RETURN:
                        # Guarda a opção escolhida
                        self.player_choice = self.chatbox.select_option()
                        if self.player_choice:
                            self.player_choice = self.player_choice.strip().upper()

                        # Limpa o modo de decisão
                        self.chatbox.options = []
                        self.chatbox.title = ""
                        self.chatbox.question = ""

                        # Fecha a caixa atual
                        self.chatbox.active = False

                        # Marca a decisão como concluída
                        self.choice_finished = True
                        return

                # -------------------------------------------------
                # MODO DIÁLOGO COMUM
                # -------------------------------------------------
                elif event.key == pygame.K_RETURN:
                    self.chatbox.next_message()

                    if self.chatbox.current_message >= len(self.chatbox.messages):
                        self.chatbox.active = False

                        # Fim do diálogo inicial → libera combate
                        if not self.intro_finished and not self.final_dialogue_started:
                            self.intro_finished = True
                            self.combat_enabled = True

                        # Fim do diálogo final antes da decisão → abre decisão
                        elif self.final_dialogue_started and not self.choice_started:
                            self.start_final_choice()

                        # Fim do diálogo após a escolha → prepara retorno ao mapa
                        elif self.choice_started:
                            self.final_dialogue_finished = True

            return

    def _handle_boss_damage(self):
        """
        Verifica se alguma flecha acertou a hurtbox do boss.
        """
        # Só pode tomar dano depois do diálogo inicial
        if not self.combat_enabled:
            return

        if self.boss_defeated or not self.boss or not self.boss.alive():
            return

        boss_hurtbox = self.get_boss_hurtbox()

        for shot in list(self.player.shots):
            if shot.rect.colliderect(boss_hurtbox):
                self.boss.take_damage(shot.damage)
                print(f"[DEBUG] Boss HP: {self.boss.life}/{self.boss.max_life} | dano={shot.damage}")
                shot.kill()

                if getattr(self.boss, "life", 0) <= 0 and not self.boss_dying:
                    self._start_boss_defeat()
                    break

    def _start_boss_defeat(self):
        """
        Inicia a sequência de derrota do boss.
        """
        self.boss_defeated = True
        self.exit_enabled = True
        setattr(self.player, "exit_mode", True)

        self._boss_hud_use_death_portrait()

        if self.boss_corpse:
            self.boss_corpse_rect = self.boss_corpse.get_rect()
            self.boss_corpse_rect.midbottom = self.boss.rect.midbottom
            self.boss_corpse_rect.y += 40
            self._boss_corpse_timer = 0
            self.boss_corpse_alpha = 255
            self.boss_dying = True

        try:
            self.boss.kill()
        except Exception:
            pass

        print("[DEBUG] Boss derrotado! Saída liberada.")

    def _boss_hud_use_death_portrait(self):
        """
        Tenta atualizar a HUD do boss para o estado visual de morte.
        """
        try:
            self.boss_hud.set(0)
        except Exception:
            pass

        if hasattr(self.boss_hud, "use_death_portrait"):
            try:
                self.boss_hud.use_death_portrait()
                return
            except Exception:
                pass

        if hasattr(self.boss_hud, "set_portrait"):
            try:
                self.boss_hud.set_portrait(self.death_portrait)
            except Exception:
                pass

    def _update_boss_corpse(self):
        """
        Atualiza o fade da imagem de morte do boss.
        """
        if self.boss_dying and self.boss_corpse and self.boss_corpse_rect:
            self._boss_corpse_timer += 1
            step = int(255 / max(1, self.boss_corpse_fade_frames))
            self.boss_corpse_alpha = max(0, self.boss_corpse_alpha - step)

    def update(self):
        """
        Atualiza a fase.
        """
        super().update()

        # Se o chatbox estiver ativo, pausa o combate
        if self.chatbox and self.chatbox.is_active():
            return

        # Se o jogador acabou de tomar a decisão,
        # abre o diálogo correspondente à escolha
        if self.choice_finished:
            self.choice_finished = False
            self.start_final_dialogue_after_choice()
            return

        # Se terminou o diálogo final após a escolha,
        # salva a decisão e volta ao mapa
        if self.final_dialogue_finished:
            self.save_player_choice()
            self.complete_area_and_return_to_map("Level_VC_1_2")
            return

        self._handle_boss_damage()
        self._update_boss_corpse()

        if not self.boss_defeated and self.boss and self.boss.alive():
            self.boss_hud.set(getattr(self.boss, "life", 0))

        # Após derrotar o boss e sair da tela,
        # abre o diálogo final antes da decisão
        if self.exit_enabled and self.player.rect.right >= BASE_WIDTH + 200:
            if not self.final_dialogue_started:
                self.start_final_dialogue_before_choice()
            return

        if self.player.lives <= 0:
            self.change_scene(GameOver())

    def draw(self, screen):
        """
        Desenha a cena completa.
        """
        screen.fill((0, 0, 0))

        self.layers.draw_back(screen)

        if not self.boss_defeated and self.boss and self.boss.alive() and not self.boss_dying:
            screen.blit(self.boss.image, self.boss.rect)
        else:
            if self.boss_dying and self.boss_corpse and self.boss_corpse_rect:
                try:
                    self.boss_corpse.set_alpha(self.boss_corpse_alpha)
                except Exception:
                    pass
                screen.blit(self.boss_corpse, self.boss_corpse_rect)

        screen.blit(self.player.image, self.player.rect)

        self.layers.draw_front(screen)
        self.player.shots.draw(screen)

        screen.blit(self.hudbk.image, self.hudbk.rect)
        screen.blit(self.hud.image, self.hud.rect)

        self.boss_hud.draw(screen)
        screen.blit(self.boss_name_text, self.boss_name_pos)

        if self.chatbox:
            self.chatbox.draw(screen)

        if self.overlay:
            self.overlay.draw(screen)
        
        

        pygame.display.update()