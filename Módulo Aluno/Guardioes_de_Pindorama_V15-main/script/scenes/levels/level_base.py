import pygame

# Importa a cena base do projeto e o menu de pausa
from ..base import Scene, PauseInventoryOverlay

# Importa o chão físico do cenário
from script.world.ground import Ground

# Importa a HUD do jogador
from script.ui.hud import Hud

# Importa a classe do jogador
from script.actors.player.player import Player

# Importa a caixa de diálogo
from script.ui.chatbox import ChatBox

# Importa constantes gerais do projeto
from script.setting import *

# Importa a pilha de layers (camadas visuais)
from script.layer_anim import LayerStack

# Importa o estado global do jogo
from script.game_state import STATE

# Importa a tela de Game Over
from ..gameover import GameOver


class Level(Scene):
    """
    Base única de todas as fases jogáveis.

    Responsável por:
    - player
    - hud
    - hud de fundo
    - chatbox
    - ground
    - layers
    - pausa
    - transição de dados entre fases
    """

    def __init__(self, player_data=None, hud_data=None):
        # Inicializa a cena base do projeto
        super().__init__()

        # ---------------------------------------------------------
        # ETAPA 1 - ESTRUTURAS BÁSICAS DO LEVEL
        # ---------------------------------------------------------

        # Overlay de pausa / inventário
        self.overlay = None

        # Indica se a saída do level está liberada
        self.exit_enabled = False

        # Permite bloquear a lógica automática de saída da fase
        self.disable_auto_exit = False

        # ---------------------------------------------------------
        # ETAPA 2 - CHÃO DO CENÁRIO
        # ---------------------------------------------------------

        # Cria o chão físico do level
        self.ground = Ground(0, 400, 800, 20)

        # Adiciona o chão ao grupo principal de sprites
        self.all_sprites.add(self.ground)

        # ---------------------------------------------------------
        # ETAPA 3 - CAMADAS VISUAIS
        # ---------------------------------------------------------

        # Estrutura de camadas do cenário
        self.layers = LayerStack()

        # Guarda o tempo do último update das layers
        self._layers_last_ticks = pygame.time.get_ticks()

        # ---------------------------------------------------------
        # ETAPA 4 - HUD DE FUNDO
        # ---------------------------------------------------------

        # Cria a imagem de fundo da HUD do jogador
        self.hudbk = Hud(
            "assets/charsSprite/player/Hud/Hud_Char_Fundo.png",
            [25, 25],
            [self.all_sprites],
            (640, 360)
        )

        # ---------------------------------------------------------
        # ETAPA 5 - PLAYER
        # ---------------------------------------------------------

        # Cria o jogador com dados herdados da fase anterior
        # ou com valores padrão, se não houver dados
        self.player = self._build_player(player_data)

        # ---------------------------------------------------------
        # ETAPA 6 - HUD PRINCIPAL
        # ---------------------------------------------------------

        # Cria a HUD principal do jogador
        self.hud = self._build_hud(hud_data)

        # Sincroniza a HUD com a quantidade atual de vidas do player
        self.hud.update_lives(self.player.lives)

        # ---------------------------------------------------------
        # ETAPA 7 - CHATBOX BASE
        # ---------------------------------------------------------

        # Fonte padrão usada na caixa de diálogo
        base_font = pygame.font.Font(None, 30)

        # Cria a caixa de diálogo base do level
        self.chatbox = ChatBox(base_font, (75, 250), (800, 400))

        # ---------------------------------------------------------
        # ETAPA 8 - ESTADOS COMUNS DE DIÁLOGO
        # ---------------------------------------------------------

        # Índice/estado de fluxo de diálogo
        self.dialogue_stage = -1

        # Indica se o diálogo terminou
        self.dialogue_finished = False

        # Indica se está confirmando alguma resposta
        self.confirming_answer = False

        # Guarda a opção selecionada
        self.selected_option = None

    def _build_player(self, player_data):
        """
        Cria o player.

        Se existir player_data, reaproveita:
        - sprite
        - posição
        - tamanho
        - vida
        - vidas
        - xp

        Caso contrário, cria com valores padrão.
        """
        if player_data:
            return Player(
                image_path=player_data.get(
                    "image_path",
                    "assets/charsSprite/player/indigenaM/R0.png"
                ),
                position=player_data.get("position", [100, 250]),
                groups=[self.all_sprites],
                size=player_data.get("size", (200, 200)),
                life=player_data.get("life", 25),
                lives=player_data.get("lives", 3),
                xp=player_data.get("xp", 0)
            )

        # Criação padrão, caso não haja dados herdados
        return Player(
            "assets/charsSprite/player/indigenaM/R0.png",
            [100, 250],
            [self.all_sprites],
            (200, 200)
        )

    def _build_hud(self, hud_data):
        """
        Cria a HUD principal do jogador.

        Primeiro usa os dados atuais do player.
        Depois, se houver hud_data, sobrescreve com os valores herdados.
        """
        hud = Hud(
            "assets/charsSprite/player/Hud/Hud_Char_Contorno.png",
            [25, 25],
            [self.all_sprites],
            (640, 360)
        )

        # Inicializa com os dados atuais do player
        hud.life = self.player.life
        hud.lives = self.player.lives
        hud.xp = self.player.xp

        # Se houver dados herdados da fase anterior, usa esses valores
        if hud_data:
            hud.gold = hud_data.get("gold", 0)
            hud.life = hud_data.get("life", hud.life)
            hud.lives = hud_data.get("lives", hud.lives)
            hud.xp = hud_data.get("xp", hud.xp)

        return hud

    def get_player_data(self):
        """
        Retorna os dados atuais do player.

        Esses dados são usados para transferir o estado do jogador
        entre uma fase e outra.
        """
        return {
            "image_path": getattr(
                self.player,
                "image_path",
                "assets/charsSprite/player/indigenaM/R0.png"
            ),
            "position": [self.player.rect.x, self.player.rect.y],
            "size": getattr(self.player, "size", (200, 200)),
            "life": self.player.life,
            "lives": self.player.lives,
            "xp": self.player.xp
        }

    def get_hud_data(self):
        """
        Retorna os dados atuais da HUD.

        Esses dados são usados para manter:
        - gold
        - vida
        - vidas
        - xp
        entre as fases.
        """
        return {
            "gold": getattr(self.hud, "gold", 0),
            "life": self.player.life,
            "lives": self.player.lives,
            "xp": self.player.xp
        }

    def open_pause_menu(self):
        """
        Abre o menu de pausa, se ainda não houver um overlay ativo.
        """
        if not self.overlay:
            self.overlay = PauseInventoryOverlay(
                parent_scene=self,
                font=FONT_BIG,
                small_font=FONT_SMALL,
                on_resume=self.on_resume,
                on_shop=self.on_shop,
                on_main_menu=self.on_main_menu
            )

    def on_resume(self):
        """
        Fecha o overlay de pausa e retorna ao jogo.
        """
        self.overlay = None

    def on_shop(self):
        """
        Placeholder para a futura loja / escambo.
        """
        print("[DEBUG] A funcionalidade de escambo ainda será implementada.")

    def on_main_menu(self):
        """
        Retorna ao menu principal e reseta o progresso global.
        """
        print("[DEBUG] Retornando ao menu principal e resetando progresso...")
        STATE.reset()

        # Importa o menu principal apenas quando necessário
        from ..menus.title import Title
        self.change_scene(Title())

    def handle_events(self, event):
        """
        Processa os eventos básicos do level:
        - overlay de pausa
        - tecla ESC
        - eventos do player
        """
        # Se houver overlay ativo, ele recebe prioridade
        if self.overlay:
            self.overlay.handle_events(event)
            return

        # ESC abre o menu de pausa
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.open_pause_menu()
            return

        # Eventos comuns do jogador (movimento, ataque etc.)
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            self.player.events(event)

    def update(self):
        """
        Atualiza a lógica base do level:
        - tempo das layers
        - animação das layers
        - HUD
        - player
        - Game Over
        """
        # Calcula delta time para atualização das layers
        now = pygame.time.get_ticks()
        dt = (now - self._layers_last_ticks) / 1000.0
        self._layers_last_ticks = now

        # Atualiza as camadas do cenário
        if self.layers:
            self.layers.update(dt)

        # Se houver diálogo ativo, congela a atualização principal
        if self.chatbox and self.chatbox.is_active():
            return

        # Atualiza estado do jogador na HUD
        self.player.check_death()
        self.hud.update_life(self.player.life)
        self.hud.update_lives(self.player.lives)
        self.hud.update_xp(self.player.xp)

        # Atualiza o player
        self.player.update()

        # Atualiza a cena base
        super().update(dt)

        # Se não houver mais vidas, vai para Game Over
        if self.player.lives <= 0:
            self.change_scene(GameOver())

    def draw(self, screen):
        """
        Desenha a estrutura visual base do level:
        - fundo preto
        - layers de fundo
        - sprites
        - player
        - layers frontais
        - projéteis
        - HUD
        - chatbox
        - overlay
        """
        # Limpa a tela
        screen.fill((0, 0, 0))

        # Desenha as camadas de fundo
        if self.layers:
            self.layers.draw_back(screen)

        # Desenha os sprites gerais
        self.all_sprites.draw(screen)

        # Desenha o player explicitamente
        screen.blit(self.player.image, self.player.rect)

        # Desenha as camadas frontais
        if self.layers:
            self.layers.draw_front(screen)

        # Desenha os projéteis do player
        self.player.shots.draw(screen)

        # Desenha a HUD do jogador
        screen.blit(self.hudbk.image, self.hudbk.rect)
        screen.blit(self.hud.image, self.hud.rect)

        # Desenha a caixa de diálogo, se existir
        if self.chatbox:
            self.chatbox.draw(screen)

        # Desenha o overlay de pausa, se existir
        if self.overlay:
            self.overlay.draw(screen)

        # Atualiza a tela
        pygame.display.update()

    def handle_level_exit(self, next_scene_cls=None):
        """
        Trata a saída do level.

        Se a saída estiver liberada e o player sair pela direita:
        - vai para a próxima fase, se next_scene_cls existir
        - ou volta ao mapa, se não existir
        """
        # Se a saída automática estiver bloqueada, interrompe
        if self.disable_auto_exit:
            return

        # Se a saída estiver liberada e o player passar da borda direita
        if self.exit_enabled and self.player.rect.x >= 1280:
            if next_scene_cls is not None:
                self.change_scene(
                    next_scene_cls(
                        player_data=self.get_player_data(),
                        hud_data=self.get_hud_data()
                    )
                )
            else:
                from ..map.map_scene import Map
                self.change_scene(Map())

    def complete_area_and_return_to_map(self, area_name):
        """
        Marca a área como concluída no estado global
        e retorna para o mapa.
        """
        STATE.complete_area(area_name)
        print(f"[DEBUG] Área concluída: {area_name} -> {STATE.completed_areas}")

        from ..map.map_scene import Map
        self.change_scene(Map())