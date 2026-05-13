import pygame
from ..base import Scene, PauseInventoryOverlay
from script.core.obj import Obj
from script.layer_anim import LayerStack, StaticLayer, FlipLayer
from script.game_state import STATE

from ..levels.level_vc_1_1 import Level_VC_1_1


# Criando Tela de Mapa
class Map(Scene):
    """Classe para a tela do mapa com desenho por layers e áreas travadas quando concluídas."""
    
    def __init__(self):
        super().__init__()  # Chama o construtor da classe pai
        
        # -----------------------------
        #  LAYERS ESTÁTICOS DO CENÁRIO
        # -----------------------------
        try:
            # (opcional/estético) mar ao fundo — está no all_sprites, mas não é parte da ordem principal
            self.mar = Obj("assets/mapSelect/Mar.jpg", [0, 0], [self.all_sprites], size=(1280, 720))
            
            # 1) 00Papiro  (primeiro a ser desenhado)
            self.papiro = Obj("assets/mapSelect/00Papiro.png", [0, 0], [self.all_sprites], size=(1280, 720))
            
            # 2) 02Mapa_NovaPindorama_Fundo (base do mapa)
            self.bgMap  = Obj("assets/mapSelect/02Mapa_NovaPindorama_Fundo.png", [0, 0], [self.all_sprites], size=(1280, 720))
            
            # (extra) contorno do mapa – desenhado depois do layer dinâmico para ficar por cima, se você quiser
            self.contMap = Obj("assets/mapSelect/01Mapa_NovaPindorama_Contorno.png", [0, 0], [self.all_sprites], size=(1280, 720))
            
            # Moldura (último de todos)
            self.bg_mold = Obj("assets/mapSelect/Moldura_V1.png", [0, 0], [self.all_sprites], size=(1280, 720))
        except pygame.error as e:
            print(f"Erro ao carregar a imagem de fundo ou moldura: {e}")

        # -----------------------------
        #  ÁREAS / SELEÇÃO / PROGRESSO
        # -----------------------------
        self.areas = self.initialize_areas()  # lista com caminhos e posições
        self.completed_areas_status = [False] * len(self.areas)  # status de conclusão por índice

        # Cursor
        self.cursor = Obj("assets/mapSelect/Cursor.png", [1070, 100], [self.all_sprites], size=(30, 48))
        self.cursor_positions = [area["cursor_position"] for area in self.areas]

        # Índice selecionado (mantemos compatibilidade com seu código antigo)
        self.cursor_choose = 0
        self.current_index = self.cursor_choose
        self.force_vale_luz_sombra = False

        # Overlay do Vilarejo Canaã COMPLETO (layer 3 quando concluído)
        # ⚠️ carregamos como Surface isolada para NÃO depender do all_sprites (que é limpo pelo load_area)
        try:
            self.overlay_vilarejo_complete = pygame.image.load(
                "assets/mapSelect/00Vilarejo_Canaa_Complete.png"
            ).convert_alpha()
            # se precisar de escala fixa:
            self.overlay_vilarejo_complete = pygame.transform.scale(self.overlay_vilarejo_complete, (1280, 720))
        except Exception as e:
            print("[Map] Falha ao carregar 00Vilarejo_Canaa_Complete.png:", e)
            self.overlay_vilarejo_complete = None

        # Aplica progresso global (trava concluídas e posiciona cursor)
        self.apply_world_progress()

        # Carrega a camada dinâmica da área selecionada inicialmente
        self.load_area(self.current_index)  # usa regra "selected vs completed" da própria área

        # 🔽 Menu de pausa (como no seu original)
        from script.setting import FONT_BIG, FONT_SMALL
        self.pause_menu = PauseInventoryOverlay(
            parent_scene=self,
            font=FONT_BIG,
            small_font=FONT_SMALL,
            on_resume=self.resume_game,
            on_shop=self.goto_shop,
            on_main_menu=self.goto_menu
        )

        self.next = None

    # -----------------------------------------------------
    #  DEFINIÇÃO DAS ÁREAS (ordem do seu array de seleção)
    # -----------------------------------------------------
    def initialize_areas(self):
        """Inicializa as áreas do mapa com suas respectivas informações."""
        return [
            {  # 0 - Vilarejo Canaã (Level_1_2) -> fica TRAVADO quando concluído
                "image_selected": "assets/mapSelect/00Vilarejo_Canaa.png",
                "area_completed": "assets/mapSelect/00Vilarejo_Canaa_Complete.png",
                "position": [0, 0],
                "cursor_position": (1070, 100)
            },
            {  # 1 - Vila da Enseada do Rio (próximo ponto)
                "image_selected": "assets/mapSelect/01Vila_Enseada_Rio.png",
                "area_completed": "assets/mapSelect/01Vila_Enseada_Rio_Complete.png",
                "position": [0, 0],
                "cursor_position": (500, 130)
            },
            {  # 2 - Povoado Cadastro
                "image_selected": "assets/mapSelect/02Povoado_Cadastro.png",
                "area_completed": "assets/mapSelect/02Povoado_Cadastro_Complete.png",
                "position": [0, 0],
                "cursor_position": (650, 240)
            },
            {  # 3 - Vilarejo Grandes Pássaros
                "image_selected": "assets/mapSelect/03Vilarejo_Grandes_Passaros.png",
                "area_completed": "assets/mapSelect/03Vilarejo_Grandes_Passaros_Complete.png",
                "position": [0, 0],
                "cursor_position": (760, 180)
            },
            {  # 4 - Vale Luz & Sombra
                "image_selected": "assets/mapSelect/04Vale_Luz_Sombra.png",
                "area_completed": "assets/mapSelect/04Vale_Luz_Sombra_Complete.png",
                "position": [0, 0],
                "cursor_position": (850, 370)
            },
            {  # 5 - Freguesia Rio Peixes
                "image_selected": "assets/mapSelect/05Freguesia_Rio_Peixes.png",
                "area_completed": "assets/mapSelect/05Freguesia_Rio_Peixes_Complete.png",
                "position": [0, 0],
                "cursor_position": (450, 310)
            },
            {  # 6 - Vilarejo Praia Pequena
                "image_selected": "assets/mapSelect/06Vilarejo_Praia_Pequena.png",
                "area_completed": "assets/mapSelect/06Vilarejo_Praia_Pequena_Complete.png",
                "position": [0, 0],
                "cursor_position": (350, 230)
            },
            {  # 7 - Vila Pássaro Vermelho
                "image_selected": "assets/mapSelect/07Vila_Passaro_Vermelho.png",
                "area_completed": "assets/mapSelect/07Vila_Passaro_Vermelho_Complete.png",
                "position": [0, 0],
                "cursor_position": (880, 200)
            },
            {  # 8 - Vilarinho Pedras Fluem
                "image_selected": "assets/mapSelect/08Vilarinho_Pedras_Fluem.png",
                "area_completed": "assets/mapSelect/08Vilarinho_Pedras_Fluem_Complete.png",
                "position": [0, 0],
                "cursor_position": (250, 100)
            },
            {  # 9 - Barragem Arco-Íris
                "image_selected": "assets/mapSelect/09Barragem_Arco_Iris.png",
                "area_completed": "assets/mapSelect/09Barragem_Arco_Iris_Complete.png",
                "position": [0, 0],
                "cursor_position": (600, 380)
            },
            {  # 10 - Vale Alecrins
                "image_selected": "assets/mapSelect/10Vale_Alecrins.png",
                "area_completed": "assets/mapSelect/10Vale_Alecrins_Complete.png",
                "position": [0, 0],
                "cursor_position": (170, 160)
            },
            {  # 11 - Bosque Cajas
                "image_selected": "assets/mapSelect/11Bosque_Cajas.png",
                "area_completed": "assets/mapSelect/11Bosque_Cajas_Complete.png",
                "position": [0, 0],
                "cursor_position": (960, 260)
            },
        ]

    # -----------------------------------------------------
    #  PROGRESSO GLOBAL → TRAVAR + POSICIONAR CURSOR
    # -----------------------------------------------------
    def apply_world_progress(self):
        """
        Lê STATE.completed_areas e marca áreas concluídas.
        Também posiciona o cursor conforme o progresso do jogo
        e conforme a decisão tomada no Level_VC_1_2.
        """
        done = STATE.completed_areas
        print("[DEBUG][MAP] Áreas concluídas (STATE):", sorted(list(done)))

        # Marca áreas concluídas no mapa
        level_to_index = {
            "Level_VC_1_2": 0,
        }

        for level_id in done:
            idx = level_to_index.get(level_id)
            if idx is not None and 0 <= idx < len(self.completed_areas_status):
                self.completed_areas_status[idx] = True

        # -----------------------------------------------------
        # DECISÃO NARRATIVA:
        # se o jogador escolheu seguir a pista para o Vale da Luz e Sombra,
        # o cursor fica travado nessa área
        # -----------------------------------------------------
        seguir_vale = False

        if hasattr(STATE, "get_flag"):
            seguir_vale = STATE.get_flag("seguir_vale_luz_sombra", False)
        elif hasattr(STATE, "flags"):
            seguir_vale = STATE.flags.get("seguir_vale_luz_sombra", False)

        VALE_LUZ_SOMBRA_IDX = 4
        VILA_ENSEADA_IDX = 1

        if seguir_vale:
            self.force_vale_luz_sombra = True
            self.current_index = VALE_LUZ_SOMBRA_IDX

        else:
            self.force_vale_luz_sombra = False

            # comportamento normal após concluir Vilarejo de Canaã
            if "Level_VC_1_2" in done and 0 <= VILA_ENSEADA_IDX < len(self.areas):
                self.current_index = VILA_ENSEADA_IDX
            else:
                if self.completed_areas_status[self.current_index]:
                    self.current_index = self._next_unlocked_index(self.current_index, step=+1)

        self.cursor_choose = self.current_index
        self.update_cursor_position()

    def _next_unlocked_index(self, start, step=+1):
        """
        Retorna o próximo índice NÃO concluído a partir de 'start',
        caminhando em 'step' (+1 direita, -1 esquerda).
        Se TODAS estiverem concluídas, retorna o próprio start.
        """
        n = len(self.areas)
        i = start
        for _ in range(n):
            i = (i + step) % n
            if not self.completed_areas_status[i]:
                return i
        return start

    def _is_locked(self, idx: int) -> bool:
        """Travado = já concluído."""
        return bool(self.completed_areas_status[idx])

    # -----------------------------------------------------
    #  CARREGAR LAYER DINÂMICO DA ÁREA SELECIONADA
    # -----------------------------------------------------
    def load_area(self, index):
        """
        Carrega a IMAGEM da área selecionada (layer dinâmico por cima do fundo).
        OBS: mantém sua lógica de limpar e repor sprites da área;
        por isso o overlay de 'Vilarejo_Canaa_Complete' foi carregado como Surface separada.
        """
        # limpa somente sprites de ÁREA, preservando os estáticos já desenhados por draw()
        # (para manter seu comportamento original, deixamos como estava:)
        self.all_sprites.empty()

        area = self.areas[index]
        # Se a área está concluída, usamos a arte 'Complete' como layer dinâmico
        area_image_path = area["image_selected"] if not self.completed_areas_status[index] else area["area_completed"]
        Obj(area_image_path, area["position"], [self.all_sprites])

        # atualiza posição do cursor
        self.update_cursor_position()

    def mark_area_as_completed(self):
        """Marca a área atual como completada (caso precise em outra lógica)."""
        self.completed_areas_status[self.cursor_choose] = True

    # -----------------------------------------------------
    #  ENTRAR NA ÁREA SELECIONADA (somente se desbloqueada)
    # -----------------------------------------------------
    def _enter_current_area(self):
        """
        Troca para a cena correspondente ao índice atual.
        ⚠️ Só é chamado se NÃO estiver travada.
        """
        idx = self.current_index

        # Mapeie aqui: indice -> cena
        if idx == 0:
            # Vilarejo Canaã (Level_1_1) — normalmente travado após concluir
            self.change_scene(Level_VC_1_1())
        elif idx == 1:
            # Vila da Enseada do Rio -> troque pela cena correta quando existir
            # self.change_scene(Level_X_Y())
            print("[Map] TODO: vincular cena da Vila da Enseada do Rio (idx=1)")
        else:
            print(f"[Map] TODO: vincular cena para índice {idx}")

    # -----------------------------------------------------
    #  EVENTOS: NAVEGAÇÃO + ENTRAR (pulando travadas)
    # -----------------------------------------------------
    def handle_events(self, event):
        # Delegue para Scene (abre pausa com ESC, etc.)
        super().handle_events(event)

        if self.overlay:
            return

        if event.type == pygame.KEYDOWN:

            # -------------------------------------------------
            # SE O CURSOR ESTIVER FORÇADO NO VALE DA LUZ E SOMBRA,
            # BLOQUEIA A NAVEGAÇÃO ENTRE ÁREAS
            # -------------------------------------------------
            if self.force_vale_luz_sombra:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_e, pygame.K_SPACE):
                    if not self._is_locked(self.current_index):
                        self._enter_current_area()
                    else:
                        print("[Map] Área concluída/travada — não pode entrar.")
                return

            # -------------------------------------------------
            # NAVEGAÇÃO NORMAL DO MAPA
            # -------------------------------------------------
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                self.current_index = self._next_unlocked_index(self.current_index, step=+1)
                self.cursor_choose = self.current_index
                self.load_area(self.current_index)

            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.current_index = self._next_unlocked_index(self.current_index, step=-1)
                self.cursor_choose = self.current_index
                self.load_area(self.current_index)

            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_e, pygame.K_SPACE):
                if not self._is_locked(self.current_index):
                    self._enter_current_area()
                else:
                    print("[Map] Área concluída/travada — não pode entrar.")

    # -----------------------------------------------------
    #  CURSOR
    # -----------------------------------------------------
    def update_cursor_position(self):
        """Atualiza a posição do cursor com base na área selecionada (índice atual)."""
        # mantém compatibilidade com self.cursor_choose
        self.cursor_choose = self.current_index
        cursor_x, cursor_y = self.cursor_positions[self.current_index]
        self.cursor.rect.topleft = (cursor_x, cursor_y)

    # (mantém compatibilidade; não é usada diretamente na nova confirmação)
    def confirm_selection(self):
        """Confirma a seleção da área atual (compatibilidade)."""
        if not self.completed_areas_status[self.cursor_choose]:
            selected_area = self.areas[self.cursor_choose]["image_selected"]
            print(f"Área selecionada: {selected_area}")
            self.next = Level_VC_1_1()
        else:
            print("Esta área já foi completada.")

    # -----------------------------------------------------
    #  DESENHO POR LAYERS — ORDEM EXATA
    # -----------------------------------------------------
    def draw(self, screen):
        """Desenha a tela do mapa na ordem correta, deixando o pause overlay por último."""

        # 1) mar
        self.mar.draw(screen)

        # 2) papiro
        self.papiro.draw(screen)

        # 3) fundo do mapa
        self.bgMap.draw(screen)

        # 4) overlay da área concluída
        if self.overlay_vilarejo_complete and self.completed_areas_status[0]:
            screen.blit(self.overlay_vilarejo_complete, (0, 0))

        # 5) desenha apenas os sprites da área selecionada
        self.all_sprites.draw(screen)

        # 6) cursor
        self.cursor.draw(screen)

        # 7) moldura
        self.bg_mold.draw(screen)

        # 8) pause overlay SEMPRE por último
        if self.overlay:
            self.overlay.draw(screen)

       
    # -----------------------------------------------------
    #  PAUSA / SAÍDAS
    # -----------------------------------------------------
    def resume_game(self):
        print("[DEBUG] Jogo retomado.")
        self.overlay = None

    def goto_shop(self):
        print("[DEBUG] A funcionalidade de escambo ainda será implementada.")

    def goto_menu(self):
        print("[DEBUG] Retornando ao menu principal e resetando progresso...")
        from script.game_state import STATE
        from ..menus.title import Title
        STATE.reset()
        self.change_scene(Title())