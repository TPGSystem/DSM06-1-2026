import pygame
from ..base import Scene
from script.core.obj import Obj
from script.setting import *
from ..menus.title import Title
from script.services.api_client import login
from script.game_state import STATE


# Criando Tela de Login de Usuário
class Login(Scene):
    """Classe para a tela de Login."""
    
    def __init__(self):
        super().__init__()  # Chama o construtor da classe base
        
        # Carregando imagens de fundo e botões
        self.background = Obj("assets/login/background.png", [0, 0], [self.all_sprites])
        self.form_body = Obj("assets/login/FormBody.png", [428, 55], [self.all_sprites])
        self.login_button = Obj("assets/login/Button.png", [541, 460], [self.all_sprites])  # Botão de Login
                
        # Configuração de fontes
        self.title_font = pygame.font.Font(None, 40)  # Fonte para o título da tela
        self.label_font = pygame.font.Font(None, 30)  # Fonte para as labels de texto
        self.font = pygame.font.Font(None, 30)  # Fonte para campos de entrada
                
        # Campos de entrada
        self.RA_rect = pygame.Rect(470, 235, 340, 40)  # Campo de RA
        self.password_rect = pygame.Rect(470, 337, 340, 40)  # Campo de Senha
        self.active_field = None  # Para controlar qual campo está ativo
        self.login_button_rect = self.login_button.rect  # Retângulo do botão de login
        self.active_field = "RA"  # Inicia com o campo RA como ativo
        self.RA_text = ""
        self.password_text = ""
        self.message = ""
        
        # Cores para campos de entrada
        self.color_active = pygame.Color('dodgerblue')
        self.color_inactive = pygame.Color('gray')
        
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_interval = 30
    
    def validate_login(self):
        """Valida se o RA e Senha correspondem aos dados cadastrados."""
        return self.RA_text == self.correct_login and self.password_text == self.correct_password
    
    def try_login(self):
        result = login(self.RA_text.strip(), self.password_text.strip())

        if result and result.get("authenticated"):
            print("LOGIN REALIZADO!")
            print(result)

            STATE.student_id = result["student"]["id"]
            STATE.student_name = result["student"]["name"]
            STATE.student_ra = result["student"]["ra"]

            STATE.class_id = result["class"]["id"]
            STATE.class_name = result["class"]["dsYearSerie"]
            STATE.teacher_name = result["class"]["dsTeacher"]
            STATE.school_year = result["class"]["schoolYear"]

            STATE.save()
            self.change_scene(Title())

        else:
            self.message = "RA ou senha incorretos"

    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário."""

        # ---------------------------------------------------------
        # EVENTOS DE TECLADO
        # ---------------------------------------------------------
        if event.type == pygame.KEYDOWN:

            # TAB alterna:
            # RA -> Senha -> Login -> RA
            if event.key == pygame.K_TAB:

                if self.active_field == "RA":
                    self.active_field = "Senha"

                elif self.active_field == "Senha":
                    self.active_field = "Login"

                elif self.active_field == "Login":
                    self.active_field = "RA"

                return

            # -----------------------------------------------------
            # CAMPO RA
            # -----------------------------------------------------
            elif self.active_field == "RA":

                if event.key == pygame.K_BACKSPACE:
                    self.RA_text = self.RA_text[:-1]

                elif event.key == pygame.K_RETURN:
                    self.active_field = "Senha"

                elif event.unicode and event.unicode.isprintable():
                    self.RA_text += event.unicode

                return

            # -----------------------------------------------------
            # CAMPO SENHA
            # -----------------------------------------------------
            elif self.active_field == "Senha":

                if event.key == pygame.K_BACKSPACE:
                    self.password_text = self.password_text[:-1]

                elif event.key == pygame.K_RETURN:
                    self.try_login()

                elif event.unicode and event.unicode.isprintable():
                    self.password_text += event.unicode

                return

            # -----------------------------------------------------
            # BOTÃO LOGIN
            # -----------------------------------------------------
            elif self.active_field == "Login":

                if event.key == pygame.K_RETURN:
                    self.try_login()

                return

        # ---------------------------------------------------------
        # EVENTOS DE MOUSE
        # ---------------------------------------------------------
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if self.RA_rect.collidepoint(event.pos):
                self.active_field = "RA"
                return

            elif self.password_rect.collidepoint(event.pos):
                self.active_field = "Senha"
                return

            elif self.login_button.rect.collidepoint(event.pos):
                self.active_field = "Login"
                self.try_login()
                return

        return
    
    def draw(self, surface):
        """Renderiza a tela de login."""
        surface.fill((0, 0, 0))  # Limpa a tela com uma cor de fundo

        # Desenha todos os sprites (background e botões)
        self.all_sprites.draw(surface)

        # Título da tela
        title_surface = self.title_font.render("Venha para a Aventura!", True, pygame.Color(BLACK_COLOR))
        title_rect = title_surface.get_rect(center=(surface.get_width() // 2, 120))  # Centraliza no eixo X e ajusta o eixo Y
        surface.blit(title_surface, title_rect.topleft)  # Usa o canto superior esquerdo do retângulo

        # Labels para os campos de entrada
        RA_label_surface = self.label_font.render("Digite seu RA:", True, pygame.Color(BLACK_COLOR))
        RA_label_rect = RA_label_surface.get_rect(topleft=(470, 209))  # Define posição inicial do texto RA
        surface.blit(RA_label_surface, RA_label_rect.topleft)

        password_label_surface = self.label_font.render("Digite sua Senha:", True, pygame.Color(BLACK_COLOR))
        password_label_rect = password_label_surface.get_rect(topleft=(470, 310))  # Define posição inicial do texto Senha
        surface.blit(password_label_surface, password_label_rect.topleft)

        # Desenha campos de texto
        RA_color = self.color_active if self.active_field == "RA" else self.color_inactive
        password_color = self.color_active if self.active_field == "Senha" else self.color_inactive

        pygame.draw.rect(surface, RA_color, self.RA_rect, 2)  # Contorno do campo RA
        pygame.draw.rect(surface, password_color, self.password_rect, 2)  # Contorno do campo Senha

        # Renderiza o texto digitado
        RA_surface = self.font.render(self.RA_text, True, pygame.Color(BLACK_COLOR))
        password_surface = self.font.render("*" * len(self.password_text), True, pygame.Color(BLACK_COLOR))  # Oculta senha com asteriscos

        # Centraliza verticalmente o texto dentro dos campos
        RA_text_rect = RA_surface.get_rect(
            midleft=(self.RA_rect.x + 8, self.RA_rect.centery)
        )

        password_text_rect = password_surface.get_rect(
            midleft=(self.password_rect.x + 8, self.password_rect.centery)
        )

        surface.blit(RA_surface, RA_text_rect)
        surface.blit(password_surface, password_text_rect)

        # ---------------------------------------------------------
        # Cursor piscando no campo selecionado
        # ---------------------------------------------------------
        if self.cursor_visible:

            if self.active_field == "RA":
                cursor_x = RA_text_rect.right + 3
                cursor_y = RA_text_rect.y
                cursor_h = RA_text_rect.height

                pygame.draw.line(
                    surface,
                    pygame.Color(BLACK_COLOR),
                    (cursor_x, cursor_y),
                    (cursor_x, cursor_y + cursor_h),
                    2
                )

            elif self.active_field == "Senha":
                cursor_x = password_text_rect.right + 3
                cursor_y = password_text_rect.y
                cursor_h = password_text_rect.height

                pygame.draw.line(
                    surface,
                    pygame.Color(BLACK_COLOR),
                    (cursor_x, cursor_y),
                    (cursor_x, cursor_y + cursor_h),
                    2
                )

        if self.message:
            msg_surface = self.font.render(
                self.message,
                True,
                pygame.Color("red")
            )

            surface.blit(msg_surface, (470, 420))
        
        # Destacar o botão de login quando estiver focado
        if self.active_field == "Login":
            pygame.draw.rect(surface, self.color_active, self.login_button_rect, 2)
        
    def update(self):
        """Atualiza a lógica da tela."""
        self.all_sprites.update()

        self.cursor_timer += 1
        if self.cursor_timer >= self.cursor_interval:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0