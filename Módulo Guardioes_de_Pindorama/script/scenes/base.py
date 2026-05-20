import json
import pygame

from script.game_state import STATE
from script.ui.pause_overlay import PauseInventoryOverlay


class Fade:
    """
    Classe responsável pelo efeito de fade.
    Pode ser usada para transições visuais entre cenas.
    """

    def __init__(self, color="black"):
        self.color = color
        self.alpha = 0
        self.enabled = False
        self.speed = 300  # velocidade do fade por segundo

    def reset(self):
        """
        Reinicia o fade.
        """
        self.alpha = 0
        self.enabled = False

    def start(self):
        """
        Ativa o fade.
        """
        self.enabled = True

    def update(self, dt):
        """
        Atualiza o fade com base no delta time.
        """
        if self.enabled:
            self.alpha = min(255, self.alpha + self.speed * dt)

    def draw(self, display):
        """
        Desenha o efeito de fade sobre a tela.
        """
        if self.enabled and self.alpha > 0:
            width, height = display.get_size()
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            surface.fill((0, 0, 0, int(self.alpha)))
            display.blit(surface, (0, 0))


class Scene:
    """
    Classe base de todas as cenas do jogo.

    Responsabilidades:
    - troca de cena
    - grupo principal de sprites
    - fade
    - menu de pausa
    - carregamento/salvamento de JSON
    """

    def __init__(self, font_path="assets/font/Primitive.ttf", font_size=36):
        # A próxima cena começa sendo a própria cena atual
        self.next = self

        # Referência para a superfície principal criada no main.py
        self.display = pygame.display.get_surface()

        # Grupo principal de sprites da cena
        self.all_sprites = pygame.sprite.Group()

        # Efeito de transição
        self.fade = Fade("black")

        # Fonte principal da cena
        self.font = pygame.font.Font(font_path, font_size)

        # Som de clique
        self.sound_click = None
        self._load_click_sound()

        # Dados carregados de configuração
        self.option_data = self.load_file("teste.json", default={})

        # Controle do menu de pausa
        self.paused = False
        self.overlay = None

    def _load_click_sound(self):
        """
        Carrega o som de clique com segurança.
        """
        try:
            self.sound_click = pygame.mixer.Sound("assets/sounds/click.ogg")
            self.sound_click.set_volume(0.25)
        except Exception as e:
            print(f"[WARN] Som de clique não carregado: {e}")
            self.sound_click = None

    def play_click(self):
        """
        Toca o som de clique, se estiver disponível.
        """
        if self.sound_click:
            try:
                self.sound_click.play()
            except Exception as e:
                print(f"[WARN] Falha ao tocar som de clique: {e}")

    def open_pause_menu(self):
        """
        Abre o menu de pausa, criando o overlay.
        """
        if self.overlay is not None:
            return

        try:
            from script.setting import FONT_BIG, FONT_SMALL
            from script.scenes.menus.title import Title

            if not self.display:
                self.display = pygame.display.get_surface()

            def on_resume():
                self.play_click()
                self.overlay = None
                self.paused = False
                self._restore_music_volume()

            def on_shop():
                self.play_click()
                self.change_scene(EscamboScene())

            def on_main_menu():
                self.play_click()
                STATE.reset()
                self.change_scene(Title())

            self.overlay = PauseInventoryOverlay(
                parent_scene=self,
                font=FONT_BIG,
                small_font=FONT_SMALL,
                on_resume=on_resume,
                on_shop=on_shop,
                on_main_menu=on_main_menu
            )

            self.paused = True
            self._lower_music_volume()

        except Exception as e:
            print(f"[WARN] Erro ao abrir menu de pausa: {e}")
            self.overlay = None
            self.paused = False

    def _lower_music_volume(self):
        """
        Reduz o volume da música enquanto o menu de pausa está aberto.
        """
        try:
            volume = self.option_data.get("music_set_volume")
            if volume is not None and pygame.mixer.get_init():
                pygame.mixer.music.set_volume(volume * 0.4)
        except Exception as e:
            print(f"[WARN] Erro ao reduzir volume: {e}")

    def _restore_music_volume(self):
        """
        Restaura o volume original da música.
        """
        try:
            volume = self.option_data.get("music_set_volume")
            if volume is not None and pygame.mixer.get_init():
                pygame.mixer.music.set_volume(volume)
        except Exception as e:
            print(f"[WARN] Erro ao restaurar volume: {e}")

    def start_music(self):
        """
        Inicia a música principal da cena com segurança.
        """
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            volume = self.option_data.get("music_set_volume", 0)
            pygame.mixer.music.load("assets/sounds/music1.mp3")

            if volume:
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(volume)
        except Exception as e:
            print(f"[WARN] Erro ao iniciar música: {e}")

    def handle_events(self, event):
        """
        Processa eventos básicos da cena.

        Se existir overlay de pausa aberto, ele recebe prioridade.
        """
        if self.overlay:
            self.overlay.handle_events(event)
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.open_pause_menu()
            return

    def update(self, dt=0):
        """
        Atualiza a cena.

        Se a cena não estiver pausada:
        - atualiza sprites
        - atualiza fade

        Se estiver pausada:
        - atualiza overlay
        """
        if not self.paused:
            self.all_sprites.update()
            self.fade.update(dt)
        elif self.overlay:
            self.overlay.update(dt)

    def draw(self, display):
        """
        Desenha os elementos principais da cena.
        """
        self.all_sprites.draw(display)
        self.fade.draw(display)

        if self.overlay:
            self.overlay.draw(display)

    def change_scene(self, next_scene):
        """
        Solicita troca de cena.
        """
        self.next = next_scene

    def save_file(self, file_path, data):
        """
        Salva dados em arquivo JSON.
        """
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[WARN] Erro ao salvar arquivo {file_path}: {e}")

    def load_file(self, file_path, default=None):
        """
        Carrega dados de um arquivo JSON.
        Se falhar, retorna o valor default.
        """
        if default is None:
            default = {}

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"[WARN] Erro ao carregar arquivo {file_path}: {e}")
            return default


class EscamboScene(Scene):
    """
    Cena placeholder da loja/escambo.
    """
    def draw(self, display):
        super().draw(display)
        text = self.font.render("ESCAMBO / LOJA (placeholder)", True, (255, 255, 0))
        display.blit(text, (50, 50))


class MenuInicialScene(Scene):
    """
    Cena placeholder do menu inicial.
    """
    def draw(self, display):
        super().draw(display)
        text = self.font.render("MENU INICIAL (placeholder)", True, (255, 255, 0))
        display.blit(text, (50, 50))