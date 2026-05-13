# ============================================================
#  CHATBOX — Sistema de Diálogo, Quiz e Decisão
#  ---------------------------------------------
#  Exibe:
#   - mensagens de diálogo
#   - perguntas de quiz com resposta correta
#   - decisões narrativas sem certo/errado
#
#  Esta versão foi ajustada para:
#   1. manter compatibilidade com o sistema atual
#   2. permitir decisões do tipo "SIM / NÃO"
#   3. evitar conflito entre quiz e decisão
# ============================================================

import os
import pygame
from script.setting import *

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def draw_text_shadow(screen, font, text, pos,
                     text_color=(0, 0, 0),
                     shadow_color=(0, 0, 0),
                     offset=(2, 2),
                     alpha=120):
    """
    Desenha um texto com sombra leve.
    """
    x, y = pos
    shadow = font.render(text, True, shadow_color).convert_alpha()
    shadow.set_alpha(alpha)
    screen.blit(shadow, (x + offset[0], y + offset[1]))

    surf = font.render(text, True, text_color)
    screen.blit(surf, (x, y))


class ChatBox:
    """Classe para exibir mensagens, quizzes e decisões narrativas."""

    def __init__(self, font=None, position=(0, 0), size=(600, 200)):
        """
        Inicializa a caixa de diálogo.

        Parâmetros:
          font      → fonte principal usada nos textos
          position  → posição (x, y) da caixa
          size      → tamanho da caixa (largura, altura)
        """

        self.frame_offset = 0

        # ------------------------------------------------------------
        # CAMADA ESCURA DE FUNDO (efeito semelhante ao pause overlay)
        # ------------------------------------------------------------
        self.bg_alpha = 180
        self.dim_color = (0, 0, 0)

        # Pasta das imagens de diálogo (frames por fala)
        self.dialog_images_dir = None

        # Área do papiro / chatbox
        self.dialog_text_rect = pygame.Rect(100, 410, 1080, 250)

        # Cache das imagens carregadas
        self._frame_cache = {}

        # ============================================================
        #  QUIZ: Frames visuais (Pergunta / Correta / Errada)
        # ============================================================
        self.quiz_frame_question_path = os.path.join(
            BASE_DIR, "assets/chatChar/level_1_1/Pergunta.png"
        )

        self.quiz_frame_correct_path = os.path.join(
            BASE_DIR, "assets/chatChar/level_1_1/Resposta_Correta.png"
        )

        self.quiz_frame_wrong_path = os.path.join(
            BASE_DIR, "assets/chatChar/level_1_1/Resposta_Errada.png"
        )

        self.quiz_frame_question = None
        self.quiz_frame_correct = None
        self.quiz_frame_wrong = None
        self._quiz_frames_scaled = False

        # ------------------------------------------------------------
        # FONTES
        # ------------------------------------------------------------
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 27)
        self.dialog_font = pygame.font.Font(None, 42)
        self.speaker_font = pygame.font.Font(None, 34)
        self.speaker_font.set_italic(True)

        # ------------------------------------------------------------
        # POSIÇÃO / TAMANHO
        # ------------------------------------------------------------
        self.position = position
        self.size = size
        self.rect = pygame.Rect(position, size)

        # ------------------------------------------------------------
        # CORES
        # ------------------------------------------------------------
        self.color = BLACK_COLOR
        self.text_color = BLACK_COLOR

        # ------------------------------------------------------------
        # ESTADO DO DIÁLOGO
        # ------------------------------------------------------------
        self.messages = []
        self.current_message = 0
        self.active = False

        # ------------------------------------------------------------
        # ESTADO DE INTERAÇÃO (quiz ou decisão)
        # ------------------------------------------------------------
        self.option_index = 0        # índice da opção selecionada
        self.score = 0
        self.title = ""
        self.question = ""
        self.options = []

        # Quiz tradicional
        self.correct_answers = []
        self.current_points = 1

        # Controle do tipo de interação:
        # "quiz"     -> há resposta correta
        # "decision" -> não há resposta correta
        self.interaction_mode = None

        # Estado visual / avaliação
        self.answer_submitted = False
        self.selection_correct = None
        self.selected_option_text = None

    # ============================================================
    #  COMPATIBILIDADE
    # ============================================================

    @property
    def selected_option(self):
        """
        Alias de compatibilidade.
        Permite usar self.selected_option como sinônimo de option_index.
        """
        return self.option_index

    @selected_option.setter
    def selected_option(self, value):
        self.option_index = value

    # ============================================================
    #  CONFIGURAÇÕES DE FRAME / IMAGEM
    # ============================================================

    def set_frame_offset(self, offset: int):
        self.frame_offset = max(0, int(offset))

    def get_frame_offset(self) -> int:
        return int(getattr(self, "frame_offset", 0))

    def set_dialog_images(self, images_dir: str, text_rect: pygame.Rect | None = None):
        self.dialog_images_dir = images_dir
        if text_rect is not None:
            self.dialog_text_rect = text_rect

    def _get_dialog_frame(self, index: int):
        """
        Carrega a imagem cujo nome começa com '{index}_' (cacheado).
        """
        if not self.dialog_images_dir:
            return None

        if index in self._frame_cache:
            return self._frame_cache[index]

        prefix = f"{index}_"
        path = None
        for fn in os.listdir(self.dialog_images_dir):
            if fn.startswith(prefix) and fn.lower().endswith(".png"):
                path = os.path.join(self.dialog_images_dir, fn)
                break

        if path is None:
            return None

        img = pygame.image.load(path).convert_alpha()
        self._frame_cache[index] = img
        return img

    def _load_quiz_frames_if_needed(self):
        """
        Carrega os frames usados em quizzes.
        """
        if self.quiz_frame_question is None:
            self.quiz_frame_question = pygame.image.load(self.quiz_frame_question_path).convert_alpha()
        if self.quiz_frame_correct is None:
            self.quiz_frame_correct = pygame.image.load(self.quiz_frame_correct_path).convert_alpha()
        if self.quiz_frame_wrong is None:
            self.quiz_frame_wrong = pygame.image.load(self.quiz_frame_wrong_path).convert_alpha()

    def _ensure_quiz_frames_scaled(self, screen):
        """
        Escala os frames do quiz para o tamanho atual da tela.
        """
        self._load_quiz_frames_if_needed()
        if self._quiz_frames_scaled:
            return

        w, h = screen.get_size()
        self.quiz_frame_question = pygame.transform.smoothscale(self.quiz_frame_question, (w, h))
        self.quiz_frame_correct = pygame.transform.smoothscale(self.quiz_frame_correct, (w, h))
        self.quiz_frame_wrong = pygame.transform.smoothscale(self.quiz_frame_wrong, (w, h))
        self._quiz_frames_scaled = True

    # ============================================================
    #  CONTROLE DE ESTADO
    # ============================================================

    def clear_interaction_state(self):
        """
        Limpa o estado de quiz / decisão.
        Use antes de alternar entre pergunta e diálogo.
        """
        self.title = ""
        self.question = ""
        self.options = []
        self.correct_answers = []
        self.option_index = 0
        self.interaction_mode = None

        self.answer_submitted = False
        self.selection_correct = None
        self.selected_option_text = None
        self.current_points = 0

    # ============================================================
    #  MÉTODOS DE EXIBIÇÃO
    # ============================================================

    def display_messages(self, messages):
        """
        Exibe um conjunto de mensagens simples (modo diálogo).
        """
        out = []
        for m in messages:
            if isinstance(m, (list, tuple)) and len(m) == 2:
                speaker, text = m
                speaker = str(speaker).strip().replace(":", "")
                text = str(text).strip()
                out.append(f"{speaker}: {text}")
            else:
                out.append(str(m))

        self.messages = out
        self.current_message = 0
        self.active = True

        # Ao entrar em diálogo, limpa qualquer interação anterior
        self.clear_interaction_state()

    def display_question(self, title, question, options, correct_answer=None, pontos=1):
        """
        Exibe uma pergunta de quiz.

        Se houver correct_answer, a interação é tratada como QUIZ.
        """
        self.title = title
        self.question = question
        self.options = options[:] if options else []
        self.option_index = 0

        self.correct_answers = [correct_answer] if correct_answer is not None else []
        self.current_points = pontos or 0

        self.answer_submitted = False
        self.selection_correct = None
        self.selected_option_text = None

        self.interaction_mode = "quiz"
        self.active = True

    def display_decision(self, title, question, options):
        """
        Exibe uma decisão narrativa.

        Não há resposta certa ou errada.
        """
        self.title = title
        self.question = question
        self.options = options[:] if options else []
        self.option_index = 0

        # Em decisão, não existe resposta correta
        self.correct_answers = []
        self.current_points = 0

        self.answer_submitted = False
        self.selection_correct = None
        self.selected_option_text = None

        self.interaction_mode = "decision"
        self.active = True

    def next_message(self):
        """
        Avança para a próxima fala no modo diálogo.
        """
        if self.options:
            return
        self.current_message += 1

    def validate_answer(self):
        """
        Verifica se a opção selecionada é a resposta correta.
        Só faz sentido para quiz.
        """
        if self.options and self.correct_answers:
            selected = self.options[self.option_index]
            if selected == self.correct_answers[0]:
                self.score += self.current_points
                print("✅ Resposta correta!")
            else:
                print("❌ Resposta errada.")
            self.active = False

    def submit_answer(self):
        """
        Marca a resposta selecionada e avalia o resultado.
        Só deve ser usado em modo quiz.
        """
        if not self.options or self.answer_submitted:
            return

        # Em decisão narrativa, não usamos submit_answer
        if self.interaction_mode == "decision":
            return

        self.selected_option_text = self.options[self.option_index]
        correct = False

        if self.correct_answers:
            correct = (self.selected_option_text == self.correct_answers[0])

        self.selection_correct = bool(correct)
        if correct:
            self.score += self.current_points

        self.answer_submitted = True

    def previous_option(self):
        """
        Seleciona a opção anterior.
        """
        if self.options:
            self.option_index = (self.option_index - 1) % len(self.options)

    def next_option(self):
        """
        Seleciona a próxima opção.
        """
        if self.options:
            self.option_index = (self.option_index + 1) % len(self.options)

    def select_option(self):
        """
        Retorna o texto da opção atualmente selecionada.
        Funciona tanto para quiz quanto para decisão.
        """
        return self.options[self.option_index] if self.options else None

    def is_active(self):
        """
        Retorna True se a chatbox estiver ativa.
        """
        return self.active

    def was_answer_submitted(self):
        """
        Retorna True se a resposta do quiz já foi enviada.
        """
        return bool(self.answer_submitted)

    def was_answer_correct(self):
        """
        Retorna True se a resposta enviada em modo quiz estava correta.
        """
        return bool(self.selection_correct)

    # ============================================================
    #  RENDERIZAÇÃO
    # ============================================================

    def draw(self, screen):
        if not self.active:
            return

        # 0) Overlay opaco
        w, h = screen.get_size()
        dim = pygame.Surface((w, h), pygame.SRCALPHA)
        dim.fill((0, 0, 0, self.bg_alpha))
        screen.blit(dim, (0, 0))

        # =========================================================
        # QUIZ: frame fixo (Pergunta / Correta / Errada)
        # =========================================================
        if self.options and self.interaction_mode == "quiz":
            self._ensure_quiz_frames_scaled(screen)

            if not self.answer_submitted:
                frame = self.quiz_frame_question
            else:
                frame = self.quiz_frame_correct if self.selection_correct else self.quiz_frame_wrong

            screen.blit(frame, (0, 0))

        # 1) Frame do diálogo narrativo
        if self.messages and not self.options and not self.question and self.current_message < len(self.messages):
            frame_index = self.frame_offset + self.current_message
            frame = self._get_dialog_frame(frame_index)
            if frame:
                screen.blit(frame, (0, 0))

        # 1.1) Frame específico para decisão narrativa
        if self.options and self.interaction_mode == "decision":
            frame_index = self.frame_offset
            frame = self._get_dialog_frame(frame_index)
            if frame:
                screen.blit(frame, (0, 0))

        # 2) Base do texto
        rect = self.dialog_text_rect
        margin = 0
        available_width = rect.width - 2 * margin
        available_height = rect.height - 2 * margin
        x = rect.x + margin
        y = rect.y + margin

        # --- Título + pergunta ---
        if self.title or self.question:
            formatted_title = self.title.strip()

            if formatted_title.startswith("Questão:"):
                core_title = formatted_title.replace("Questão:", "", 1).strip()
                if core_title.endswith("-"):
                    core_title = core_title[:-1].strip()
                formatted_title = f'Questão: "{core_title}" -'

            full_question_text = f"{formatted_title} {self.question}".strip()

            for line in self.wrap_text(full_question_text, available_width, self.font):
                if available_height < 20:
                    break
                surf = self.font.render(line, True, BLACK_COLOR)
                screen.blit(surf, (x, y))
                y += 24
                available_height -= 24

        # --- Opções (quiz ou decisão) ---
        if self.options:
            y += 20
            available_height -= 20

            # Modo decisão: sempre mostra opções normais, sem certo/errado
            if self.interaction_mode == "decision":
                for i, opt in enumerate(self.options):
                    wrapped = self.wrap_text(str(opt), available_width, self.small_font)

                    for line in wrapped:
                        if available_height < 20:
                            break

                        if i == self.option_index:
                            draw_text_shadow(
                                screen,
                                self.small_font,
                                line,
                                (x, y),
                                text_color=GOLD,
                                shadow_color=BLACK_COLOR,
                                offset=(2, 2),
                                alpha=140
                            )
                        else:
                            surf = self.small_font.render(line, True, BLACK_COLOR)
                            screen.blit(surf, (x, y))

                        y += 20
                        available_height -= 20

                    if i < len(self.options) - 1:
                        y += 10
                        available_height -= 10

                return

            # Modo quiz
            if not self.answer_submitted:
                for i, opt in enumerate(self.options):
                    wrapped = self.wrap_text(str(opt), available_width, self.small_font)

                    for line in wrapped:
                        if available_height < 20:
                            break

                        if i == self.option_index:
                            draw_text_shadow(
                                screen,
                                self.small_font,
                                line,
                                (x, y),
                                text_color=GOLD,
                                shadow_color=BLACK_COLOR,
                                offset=(2, 2),
                                alpha=140
                            )
                        else:
                            surf = self.small_font.render(line, True, BLACK_COLOR)
                            screen.blit(surf, (x, y))

                        y += 20
                        available_height -= 20

                    if i < len(self.options) - 1:
                        y += 10
                        available_height -= 10

            else:
                correct_text = self.correct_answers[0] if self.correct_answers else None
                chosen_text = self.selected_option_text

                to_render = []
                if self.selection_correct:
                    to_render = [(chosen_text, DARK_GREEN)]
                else:
                    if correct_text:
                        to_render.append((correct_text, DARK_GREEN))
                    if chosen_text and chosen_text != correct_text:
                        to_render.append((chosen_text, DARK_RED))

                for text_val, c in to_render:
                    wrapped = self.wrap_text(str(text_val), available_width, self.small_font)
                    for line in wrapped:
                        if available_height < 20:
                            break
                        surf = self.small_font.render(line, True, c)
                        screen.blit(surf, (x, y))
                        y += 25
                        available_height -= 25

                    y += 15
                    available_height -= 15

            return

        # --- Diálogo simples ---
        if self.messages and self.current_message < len(self.messages):
            current_text = self.messages[self.current_message]

            if ":" in current_text:
                speaker, message = current_text.split(":", 1)
                speaker = speaker.strip()
                message = message.strip()
            else:
                speaker = ""
                message = current_text.strip()

            if speaker.startswith("Cacique"):
                color = BLACK_COLOR
            elif speaker.startswith(("Player", "Jogador", "Jovem Guerreiro")):
                color = BLACK_COLOR
            else:
                color = self.text_color

            # Nome de quem fala
            speaker_top_y = rect.y + 10

            if speaker:
                speaker_surf = self.speaker_font.render(speaker, True, color)

                right_speakers = {"Cacique", "???", "Mapinguari"}
                left_speakers = {"Jovem Guerreiro"}

                if speaker in right_speakers:
                    speaker_x = rect.right - speaker_surf.get_width() - 20
                elif speaker in left_speakers:
                    speaker_x = rect.x + 20
                else:
                    speaker_x = rect.x + (rect.width - speaker_surf.get_width()) // 2

                screen.blit(speaker_surf, (speaker_x, speaker_top_y))

            # Fala centralizada
            text_area_top = rect.y + 55
            text_area_height = rect.height - 70

            lines = self.wrap_text(message, available_width - 40, self.dialog_font)

            line_height = 42
            total_text_height = len(lines) * line_height
            start_y = text_area_top + max(0, (text_area_height - total_text_height) // 2)

            current_y = start_y
            for line in lines:
                if line == "":
                    current_y += line_height
                    continue

                line_surf = self.dialog_font.render(line, True, color)
                line_x = rect.x + (rect.width - line_surf.get_width()) // 2
                screen.blit(line_surf, (line_x, current_y))
                current_y += line_height

    # ============================================================
    #  UTILITÁRIOS DE TEXTO
    # ============================================================

    def wrap_text(self, text, max_width, font=None):
        """
        Divide o texto em múltiplas linhas para caber dentro da largura.
        Respeita \\n como quebra manual.
        """
        if text is None:
            return []

        font = font or self.font
        final_lines = []
        manual_lines = str(text).split("\n")

        for manual_line in manual_lines:
            words = manual_line.split()

            if not words:
                final_lines.append("")
                continue

            current_line = []

            for word in words:
                test_line = " ".join(current_line + [word])

                if font.size(test_line)[0] > max_width:
                    if current_line:
                        final_lines.append(" ".join(current_line))
                    current_line = [word]
                else:
                    current_line.append(word)

            if current_line:
                final_lines.append(" ".join(current_line))

        return final_lines