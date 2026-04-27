import random
import pygame

# Importa a classe base dos levels
from .level_base import Level

# Importa o NPC do Cacique
from script.actors.npcs.cacique import NPC_Cacique

# Importa os diálogos da fase
from script.data.dialogs.dialog_1_1 import Dialogo_1_1

# Importa as questões do quiz
from script.data.quizzes.questions_1_1 import Questoes_1_1

# Importa as classes de camadas visuais
from script.layer_anim import StaticLayer, FlipLayer

# Importa constantes do projeto
from script.setting import *

# Importa a tela de Game Over
from ..gameover import GameOver


class Level_VC_1_1(Level):
    """
    Fase 1_1 da região Vilarejo de Canaã.

    Esta fase contém:
    - cenário com layers
    - NPC do Cacique
    - diálogo inicial
    - quiz
    - diálogo final
    - transição para a próxima fase
    """

    def __init__(self, player_data=None, hud_data=None):
        # Inicializa a estrutura base do level
        super().__init__(player_data, hud_data)

        # ---------------------------------------------------------
        # ETAPA 1 - CONTROLE GERAL DA FASE
        # ---------------------------------------------------------

        # Impede a saída automática padrão da classe base
        self.disable_auto_exit = True

        # A saída só será liberada após completar diálogo + quiz
        self.exit_enabled = False

        # ---------------------------------------------------------
        # ETAPA 2 - CAMADAS DO CENÁRIO
        # ---------------------------------------------------------

        # Caminho base das imagens do cenário
        base_path = "assets/levelSprite/Level_1_1/"

        # Camada de fundo absoluto
        self.layers.add(
            "level_1_1a",
            StaticLayer(f"{base_path}level_1_1a.png", z=0, plane="back", pos=(0, 0))
        )

        # Camada animada de fundo
        self.layers.add(
            "level_1_1aa_ab",
            FlipLayer(
                f"{base_path}level_1_1aa.png",
                f"{base_path}level_1_1ab.png",
                fps=4.0,
                z=10,
                plane="back",
                pos=(0, 0)
            )
        )

        # Demais camadas de fundo
        self.layers.add(
            "level_1_1b",
            StaticLayer(f"{base_path}level_1_1b.png", z=20, plane="back", pos=(0, 0))
        )
        self.layers.add(
            "level_1_1c",
            StaticLayer(f"{base_path}level_1_1c.png", z=30, plane="back", pos=(0, 0))
        )

        # Camada animada de fundo
        self.layers.add(
            "level_1_1ca_cb",
            FlipLayer(
                f"{base_path}level_1_1ca.png",
                f"{base_path}level_1_1cb.png",
                fps=5.0,
                z=40,
                plane="back",
                pos=(0, 0)
            )
        )

        # Camadas frontais (desenhadas na frente do player/NPC)
        self.layers.add(
            "level_1_1d",
            StaticLayer(f"{base_path}level_1_1d.png", z=10, plane="front", pos=(0, 0))
        )

        # Camada animada frontal
        self.layers.add(
            "level_1_1da_db",
            FlipLayer(
                f"{base_path}level_1_1da.png",
                f"{base_path}level_1_1db.png",
                fps=4.0,
                z=20,
                plane="front",
                pos=(0, 0)
            )
        )

        # Camada animada frontal
        self.layers.add(
            "level_1_1ea_eb",
            FlipLayer(
                f"{base_path}level_1_1ea.png",
                f"{base_path}level_1_1eb.png",
                fps=4.0,
                z=30,
                plane="front",
                pos=(0, 0)
            )
        )

        # Camada frontal estática final
        self.layers.add(
            "level_1_1f",
            StaticLayer(f"{base_path}level_1_1f.png", z=40, plane="front", pos=(0, 0))
        )
        # ---------------------------------------------------------
        # ETAPA 3 - AJUSTES DO PLAYER
        # ---------------------------------------------------------

        # Define a área do buraco desta fase
        hole_rect = pygame.Rect(520, GROUND_LEVEL - 10, 100, 400)
        self.player.set_holes([hole_rect])

        # O player não pode sair da tela até completar a fase
        setattr(self.player, "exit_mode", False)

        # ---------------------------------------------------------
        # ETAPA 4 - NPC DA FASE
        # ---------------------------------------------------------

        # Cria o NPC do Cacique
        self.npc = NPC_Cacique(
            "assets/charsSprite/npcs/Cacique/CR1.png",
            [1000, 285],
            [self.all_sprites],
            (200, 200)
        )

        # ---------------------------------------------------------
        # ETAPA 5 - CHATBOX
        # ---------------------------------------------------------

        # Define as imagens usadas pelo chatbox desta fase
        self.chatbox.set_dialog_images(
            "assets/chatChar/level_1_1",
            pygame.Rect(100, 410, 1080, 250)
        )

        # ---------------------------------------------------------
        # ETAPA 6 - FLUXO DE DIÁLOGO E QUIZ
        # ---------------------------------------------------------

        # Quantidade de falas antes do quiz começar
        self.DIALOGUE_BEFORE_QUIZ = 6

        # Divide os diálogos entre:
        # - diálogo inicial
        # - diálogo final
        self.dialogue = Dialogo_1_1.falas[:self.DIALOGUE_BEFORE_QUIZ]
        self.final_dialogue = Dialogo_1_1.falas[self.DIALOGUE_BEFORE_QUIZ:]

        # Índice da pergunta atual
        self.current_question = 0

        # Estágio atual:
        # 0 = diálogo inicial
        # 1 = quiz
        # 2 = diálogo final
        self.dialogue_stage = 0

        # Controle de recompensas
        self.gold_reward = 0
        self.points_to_gold_conversion = 2

        # Copia e embaralha as perguntas
        self.questions = Questoes_1_1.perguntas[:]
        random.shuffle(self.questions)

    def handle_events(self, event):
        """
        Processa eventos da fase:
        - diálogo
        - quiz
        - interação com NPC
        """
        # Primeiro processa a lógica base
        super().handle_events(event)

        # Se houver overlay de pausa, interrompe o restante
        if self.overlay:
            return

        # ---------------------------------------------------------
        # ETAPA 7 - QUANDO O CHATBOX ESTÁ ATIVO
        # ---------------------------------------------------------
        if self.chatbox and self.chatbox.is_active():
            if event.type == pygame.KEYDOWN:

                # ENTER = avançar diálogo / confirmar quiz
                if event.key == pygame.K_RETURN:

                    # ---------------------------------------------
                    # MODO QUIZ
                    # ---------------------------------------------
                    if self.chatbox.options:
                        current_question = self.questions[self.current_question]

                        # Se ainda não submeteu resposta, envia agora
                        if not self.chatbox.was_answer_submitted():
                            self.chatbox.submit_answer()

                            # Se acertou, converte pontos em gold
                            if self.chatbox.was_answer_correct():
                                points = current_question.get("pontos", 0)
                                if points > 0:
                                    gold_reward = points * self.points_to_gold_conversion
                                    self.hud.update_gold(self.hud.gold + gold_reward)
                                    print(f"✅ Resposta correta! +{gold_reward} gold")
                                else:
                                    print("✅ Resposta correta (sem pontos).")
                            else:
                                print("❌ Resposta errada.")

                        # Se já submeteu, avança para a próxima questão
                        else:
                            self.current_question += 1

                            # Se ainda há perguntas
                            if self.current_question < len(self.questions):
                                question_data = self.questions[self.current_question]
                                shuffled_options = question_data["opcoes"][:]
                                random.shuffle(shuffled_options)

                                self.chatbox.display_question(
                                    question_data["titulo"],
                                    question_data["pergunta"],
                                    shuffled_options,
                                    correct_answer=question_data["resposta_correta"],
                                    pontos=question_data.get("pontos", 1)
                                )

                            # Se acabou o quiz, inicia o diálogo final
                            else:
                                self.dialogue_stage = 2
                                self.chatbox.options = []
                                self.chatbox.title = ""
                                self.chatbox.question = ""
                                self.chatbox.set_frame_offset(self.DIALOGUE_BEFORE_QUIZ)

                                formatted_dialogue = [
                                    f"{speaker.rstrip(':').strip()}: {str(message).lstrip(':').lstrip()}"
                                    for speaker, message in self.final_dialogue
                                ]

                                self.chatbox.display_messages(formatted_dialogue)
                                self.chatbox.active = True

                    # ---------------------------------------------
                    # MODO DIÁLOGO
                    # ---------------------------------------------
                    else:
                        self.chatbox.next_message()

                        # Se terminou o diálogo inicial, começa o quiz
                        if self.dialogue_stage == 0 and self.chatbox.current_message >= self.DIALOGUE_BEFORE_QUIZ:
                            self.dialogue_stage = 1
                            self.current_question = 0

                            question_data = self.questions[self.current_question]
                            shuffled_options = question_data["opcoes"][:]
                            random.shuffle(shuffled_options)

                            self.chatbox.display_question(
                                question_data["titulo"],
                                question_data["pergunta"],
                                shuffled_options,
                                correct_answer=question_data["resposta_correta"],
                                pontos=question_data.get("pontos", 1)
                            )
                            self.chatbox.active = True

                        # Se terminou o diálogo final, libera a saída
                        elif self.dialogue_stage == 2 and self.chatbox.current_message >= len(self.chatbox.messages):
                            self.chatbox.active = False
                            self.exit_enabled = True
                            setattr(self.player, "exit_mode", True)

                        # Segurança: fecha chatbox se acabar mensagem fora do fluxo esperado
                        elif self.chatbox.current_message >= len(self.chatbox.messages):
                            self.chatbox.active = False

                # Navegação do quiz para cima
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and self.chatbox.options:
                    self.chatbox.previous_option()

                # Navegação do quiz para baixo
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.chatbox.options:
                    self.chatbox.next_option()

            return

        # ---------------------------------------------------------
        # ETAPA 8 - INTERAÇÃO COM O NPC
        # ---------------------------------------------------------
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and self.player.rect.colliderect(self.npc.rect):
                self.dialogue_stage = 0
                self.chatbox.set_frame_offset(0)

                formatted_dialogue = [
                    f"{speaker.rstrip(':').strip()}: {str(message).lstrip(':').lstrip()}"
                    for speaker, message in Dialogo_1_1.falas[:self.DIALOGUE_BEFORE_QUIZ]
                ]

                self.chatbox.display_messages(formatted_dialogue)
                self.chatbox.active = True

    def update(self):
        """
        Atualiza a fase:
        - lógica base
        - transição para a próxima fase
        - game over
        """
        # Atualiza a lógica comum do level
        super().update()

        # Se a saída estiver liberada e o player sair pela direita,
        # troca para a fase seguinte
        if self.exit_enabled and self.player.rect.x >= 1280:
            from .level_vc_1_2 import Level_VC_1_2
            self.change_scene(
                Level_VC_1_2(
                    player_data={
                        "image_path": self.player.image_path,
                        "position": [0, 250],
                        "size": self.player.size,
                        "life": self.player.life,
                        "lives": self.player.lives,
                        "xp": self.player.xp
                    },
                    hud_data={
                        "gold": self.hud.gold,
                        "life": self.player.life,
                        "lives": self.player.lives,
                        "xp": self.player.xp
                    }
                )
            )
            return

        # Se não houver mais vidas, vai para Game Over
        if self.player.lives <= 0:
            self.change_scene(GameOver())

    def draw(self, screen):
        """
        Desenha a cena completa:
        - fundo
        - sprites
        - NPC
        - player
        - camadas frontais
        - projéteis
        - HUD
        - chatbox
        - overlay
        """
        # Limpa a tela
        screen.fill((0, 0, 0))

        # Desenha as camadas de fundo
        self.layers.draw_back(screen)

        # Desenha os sprites do grupo principal
        self.all_sprites.draw(screen)

        # Desenha explicitamente NPC e player
        screen.blit(self.npc.image, self.npc.rect)
        screen.blit(self.player.image, self.player.rect)

        # Desenha as camadas da frente
        self.layers.draw_front(screen)

        # Desenha os projéteis do player
        self.player.shots.draw(screen)

        # Desenha a HUD
        screen.blit(self.hudbk.image, self.hudbk.rect)
        screen.blit(self.hud.image, self.hud.rect)

        # Desenha o chatbox se existir
        if self.chatbox:
            self.chatbox.draw(screen)

        # Desenha o overlay de pausa se estiver ativo
        if self.overlay:
            self.overlay.draw(screen)

        # Atualiza a tela
        pygame.display.update()