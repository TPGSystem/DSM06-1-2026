import pygame


class PauseInventoryOverlay:
    """
    Overlay de pausa/inventário exibido sobre a cena atual.

    Responsabilidades:
    - desenhar o fundo escurecido
    - exibir inventário
    - exibir opções do menu
    - controlar navegação pelas opções
    - executar callbacks recebidos da cena pai
    """

    def __init__(self, parent_scene, font, small_font, on_resume, on_shop, on_controls, on_settings, on_main_menu):
        """
        parent_scene: referência da cena que abriu o menu
        font: fonte principal
        small_font: fonte menor
        on_resume: função chamada ao escolher "Retomar"
        on_shop: função chamada ao escolher "Escambo (Loja)"
        on_main_menu: função chamada ao escolher "Menu Inicial"
        """
        self.parent_scene = parent_scene
        self.font = font
        self.small_font = small_font

        # Callbacks que a cena pai fornece
        self.on_resume = on_resume
        self.on_shop = on_shop
        self.on_controls = on_controls
        self.on_settings = on_settings
        self.on_main_menu = on_main_menu
        self.mode = "menu"
        self.settings_options = ["Volume Música", "Volume Efeitos", "Voltar"]
        self.settings_selected = 0
        
        # =====================================================
        # Utiliza a instância global compartilhada do controle.
        #
        # Não criamos Controller() aqui.
        # Usamos exatamente o mesmo objeto criado no main.py.
        # =====================================================

        from script.controller import get_controller

        self.controller = get_controller()
            
        self.option_screen = None
        
        # Cache da imagem carregada
        self.controls_image = None
        self.controls_image_type = None
        self.controls_image_size = None    

        # Opções exibidas no menu
        self.options = ["Retomar", "Escambo (Loja)", "Controles", "Configurações", "Menu Inicial"]

        # Índice da opção atualmente selecionada
        self.selected = 0

        # Transparência do fundo escurecido
        self.bg_alpha = 180

        # Título do painel
        self.title_text = "Inventário & Pausa"

        # Dados do inventário (placeholder por enquanto)
        self.inventory_items = self._read_inventory()

    def _read_inventory(self):
        """
        Retorna itens fictícios do inventário.
        Depois você poderá substituir isso por dados reais vindos do STATE.
        """
        return [
            {"nome": "Poção de Cura", "qtd": 2},
            {"nome": "Cogumelo de Energia", "qtd": 1},
            {"nome": "Flecha de Taquara", "qtd": 18},
            {"nome": "Moedas", "qtd": 37},
        ]

    def handle_events(self, event):
        """
        Processa os eventos do menu de pausa.
        """
        if event.type != pygame.KEYDOWN:
            return

        # =====================================================
        # MODO CONTROLES
        # =====================================================
        if self.mode == "controls":

            # ENTER / SPACE / ESC volta para o menu principal do pause
            if event.key in (
                pygame.K_RETURN,
                pygame.K_SPACE,
                pygame.K_ESCAPE
            ):
                self.mode = "menu"

            return

        # =====================================================
        # MODO CONFIGURAÇÕES
        # =====================================================
        if self.mode == "settings":
            if event.key == pygame.K_ESCAPE:
                self.option_screen = None
                self.mode = "menu"
                return

            if self.option_screen:
                self.option_screen.handle_events(event)

                if self.option_screen.request_back_to_pause:
                    self.option_screen = None
                    self.mode = "menu"

            return

        # =====================================================
        # MENU PRINCIPAL DO PAUSE
        # =====================================================

        # Sobe nas opções
        if event.key in (pygame.K_UP, pygame.K_w):
            self.selected = (self.selected - 1) % len(self.options)
            self.parent_scene.play_click()

        # Desce nas opções
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.selected = (self.selected + 1) % len(self.options)
            self.parent_scene.play_click()

        # Confirma opção
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self._activate_selected()

        # Fecha o menu com ESC
        elif event.key == pygame.K_ESCAPE:
            self.on_resume()

    def _activate_selected(self):
        """
        Executa a ação vinculada à opção selecionada.
        """
        option = self.options[self.selected]

        if option == "Retomar":
            self.on_resume()

        elif option == "Escambo (Loja)":
            self.on_shop()

        elif option == "Controles":
            self.mode = "controls"

        elif option == "Configurações":
            from script.scenes.menus.option import Option
            self.option_screen = Option(return_to_pause=True)
            self.mode = "settings"

        elif option == "Menu Inicial":
            self.on_main_menu()

    def update(self, dt):
        """
        Mantido para futuras animações do overlay.
        """
        pass

    def draw(self, display):
        """
        Desenha o overlay na tela.
        """
        width, height = display.get_size()

        # =====================================================
        # MODO CONTROLES
        # =====================================================
        if self.mode == "controls":
            self._draw_controls(display)
            return

        # =====================================================
        # MODO CONFIGURAÇÕES
        # =====================================================
        if self.mode == "settings":
            self._draw_settings(display)
            return

        # =====================================================
        # MENU PRINCIPAL DO PAUSE
        # =====================================================

        # Fundo escurecido
        dim = pygame.Surface((width, height), pygame.SRCALPHA)
        dim.fill((0, 0, 0, self.bg_alpha))
        display.blit(dim, (0, 0))

        # Painel central
        panel_width = int(width * 0.6)
        panel_height = int(height * 0.65)
        panel_rect = pygame.Rect(0, 0, panel_width, panel_height)
        panel_rect.center = (width // 2, height // 2)

        pygame.draw.rect(display, (30, 30, 30), panel_rect, border_radius=16)
        pygame.draw.rect(display, (200, 200, 200), panel_rect, width=2, border_radius=16)

        # Título
        title_surf = self.font.render(self.title_text, True, (240, 240, 240))
        title_rect = title_surf.get_rect(center=(panel_rect.centerx, panel_rect.top + 50))
        display.blit(title_surf, title_rect)

        padding = 28
        col_gap = 24

        # Área do inventário
        left_rect = pygame.Rect(
            panel_rect.left + padding,
            title_rect.bottom + 20,
            int(panel_width * 0.48),
            panel_rect.bottom - (title_rect.bottom + 20) - padding
        )

        # Área das opções
        right_rect = pygame.Rect(
            left_rect.right + col_gap,
            left_rect.top,
            panel_rect.right - padding - (left_rect.right + col_gap),
            left_rect.height
        )

        # Título do inventário
        inv_title = self.small_font.render("Inventário", True, (210, 210, 210))
        display.blit(inv_title, (left_rect.x, left_rect.y))

        # Lista de itens
        y = left_rect.y + 30
        for item in self.inventory_items:
            line = f"- {item['nome']} x{item['qtd']}"
            line_surf = self.small_font.render(line, True, (230, 230, 230))
            display.blit(line_surf, (left_rect.x + 8, y))
            y += 26

        # Título das opções
        opt_title = self.small_font.render("Opções", True, (210, 210, 210))
        display.blit(opt_title, (right_rect.x, right_rect.y))

        # Lista de opções
        y = right_rect.y + 36
        for index, option in enumerate(self.options):
            is_selected = index == self.selected
            color = (255, 255, 255) if is_selected else (200, 200, 200)

            option_surf = self.font.render(option, True, color)
            display.blit(option_surf, (right_rect.x + 8, y))

            if is_selected:
                arrow = self.font.render("▶", True, color)
                display.blit(arrow, (right_rect.x - 36, y))

            y += 48
    
    def _get_controls_image_path(self):
        """
        Retorna qual imagem deve ser exibida
        de acordo com o controle atualmente conectado.
        """

        controller_type = self.controller.get_controller_type()

        if controller_type == "playstation":
            return "assets/controls/Control_PS.png"

        if controller_type == "xbox":
            return "assets/controls/Control_XBOX.png"

        return "assets/controls/Control_Teclado.png"
    
    def _load_controls_image_if_needed(self, width, height):
        """
        Recarrega a imagem somente quando:
        - o tipo do controle muda
        - o tamanho da tela muda
        """

        controller_type = self.controller.get_controller_type()

        if (
            self.controls_image is not None
            and self.controls_image_type == controller_type
            and self.controls_image_size == (width, height)
        ):
            return

        image_path = self._get_controls_image_path()

        image = pygame.image.load(image_path).convert()
        image = pygame.transform.scale(image, (width, height))

        self.controls_image = image
        self.controls_image_type = controller_type
        self.controls_image_size = (width, height)

        print(f"[CONTROLES] Atualizado para: {controller_type}")
            
    def _draw_controls(self, display):
        width, height = display.get_size()

        # Atualiza automaticamente caso
        # o controle seja conectado/desconectado
        self._load_controls_image_if_needed(width, height)

        display.blit(self.controls_image, (0, 0))

        msg = self.small_font.render(
            "ENTER, ESPAÇO ou ESC para voltar",
            True,
            (0, 0, 0)
        )

        msg_rect = msg.get_rect()
        msg_rect.topleft = (40, height - 60)

        box_rect = msg_rect.inflate(30, 18)

        pygame.draw.rect(
            display,
            (255, 255, 255),
            box_rect,
            border_radius=10
        )

        display.blit(msg, msg_rect)


    def _draw_settings(self, display):
        if self.option_screen:
            self.option_screen.update()
            self.option_screen.all_sprites.draw(display)