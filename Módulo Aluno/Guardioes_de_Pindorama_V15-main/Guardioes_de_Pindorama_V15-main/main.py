import sys
import traceback

import pygame

# Importa o tradutor de entrada do joystick/controle
from script.controller import Controller

# Importa a primeira cena do jogo (tela de login)
from script.scenes.auth.login import Login

# Importa as configurações principais da janela e FPS
from script.setting import BASE_WIDTH, BASE_HEIGHT, FPS


class Game:
    def __init__(self):
        """
        Construtor principal do jogo.

        Aqui chamamos métodos separados para:
        1. Inicializar o pygame
        2. Criar a janela
        3. Criar objetos de execução (clock, cena, controle)
        """
        self._init_pygame()
        self._init_window()
        self._init_runtime_objects()

    def _init_pygame(self):
        """
        Inicializa os módulos principais do pygame.
        Também tenta iniciar o mixer de áudio
        e definir o título da janela.

        OBS:
        O ícone NÃO deve ser carregado aqui,
        porque o display ainda não foi criado.
        """
        pygame.init()

        # Tenta iniciar o sistema de áudio
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"[WARN] Mixer não inicializado: {e}")

        # Define o título da janela
        pygame.display.set_caption("Guardiões de Pindorama")

    def _init_window(self):
        """
        Cria a janela principal e a tela virtual.

        A janela principal pode ser redimensionada.
        A tela virtual mantém a resolução fixa do jogo, permitindo
        escalonamento com letterbox sem distorcer a imagem.

        IMPORTANTE:
        O ícone do jogo é carregado aqui, depois do set_mode(),
        porque convert_alpha() e set_icon() precisam do display já criado.
        """
        # Flags da janela: redimensionável + double buffer
        self.window_flags = pygame.RESIZABLE | pygame.DOUBLEBUF

        # Janela real exibida ao usuário
        self.display = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), self.window_flags)

        # Tela virtual do jogo, com resolução fixa
        self.virtual_screen = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))

        # Controla se o jogo está ou não em tela cheia
        self.fullscreen = False

        # ---------------------------------------------------------
        # ETAPA - CARREGAR O ÍCONE DA JANELA
        # ---------------------------------------------------------
        try:
            icon = pygame.image.load("assets/menu/Icon.png").convert_alpha()
            pygame.display.set_icon(icon)
        except Exception as e:
            print(f"[WARN] Ícone não carregado: {e}")

    def _init_runtime_objects(self):
        """
        Cria os objetos usados durante a execução do jogo:
        - clock: controla FPS e delta time
        - running: controla o loop principal
        - scene: cena atual do jogo
        - controller: gerencia o joystick/controle
        """
        self.clock = pygame.time.Clock()
        self.running = True

        # Define a primeira cena do jogo
        self.scene = Login()

        # Inicializa o tradutor de controle
        self.controller = Controller()

        # Se a cena possuir o método on_enter, chama ao iniciar
        self._call_scene_hook(self.scene, "on_enter")

    def _call_scene_hook(self, scene, hook_name):
        """
        Método auxiliar para chamar hooks opcionais da cena,
        como on_enter() e on_exit().

        Isso evita repetição de código e protege contra erros.
        """
        if not scene or not hasattr(scene, hook_name):
            return

        try:
            getattr(scene, hook_name)()
        except Exception as e:
            print(f"[WARN] Erro em {scene.__class__.__name__}.{hook_name}(): {e}")

    def toggle_fullscreen(self):
        """
        Alterna entre modo janela e modo tela cheia.

        Em modo janela, usa a resolução base do jogo.
        Em modo fullscreen, usa a resolução do monitor.

        OBS:
        Após recriar a janela, reaplica o ícone.
        """
        if self.fullscreen:
            # Volta para modo janela
            self.display = pygame.display.set_mode(
                (BASE_WIDTH, BASE_HEIGHT),
                pygame.RESIZABLE | pygame.DOUBLEBUF
            )
            self.fullscreen = False
        else:
            # Vai para modo tela cheia
            self.display = pygame.display.set_mode(
                (0, 0),
                pygame.FULLSCREEN | pygame.DOUBLEBUF
            )
            self.fullscreen = True

        # Reaplica o ícone após recriar o display
        try:
            icon = pygame.image.load("assets/menu/Icon.png").convert_alpha()
            pygame.display.set_icon(icon)
        except Exception as e:
            print(f"[WARN] Ícone não recarregado após fullscreen: {e}")

    def handle_quit(self):
        """
        Encerra o loop principal do jogo.
        """
        self.running = False

    def handle_event(self, event):
        """
        Processa um único evento do pygame.

        Etapas:
        1. Verifica se o usuário quer fechar o jogo
        2. Verifica se pressionou F11 para alternar fullscreen
        3. Traduz evento do controle, se necessário
        4. Repassa o evento para a cena atual
        """
        # Fecha a janela do jogo
        if event.type == pygame.QUIT:
            self.handle_quit()
            return

        # Alterna fullscreen ao pressionar F11
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            self.toggle_fullscreen()
            return

        # Por padrão, usamos o evento original
        translated_event = event

        # Tenta traduzir eventos do joystick/controle
        try:
            controller_event = self.controller.process_event(event)
            if controller_event is not None:
                translated_event = controller_event
        except Exception as e:
            print(f"[WARN] Controller.process_event falhou: {e}")

        # Repassa o evento final para a cena atual
        if self.scene and hasattr(self.scene, "handle_events"):
            try:
                self.scene.handle_events(translated_event)
            except Exception as e:
                print(f"[WARN] Erro em {self.scene.__class__.__name__}.handle_events(): {e}")

    def update_scene(self, dt):
        """
        Atualiza a lógica da cena atual.

        Primeiro tenta chamar update(dt), que é o ideal.
        Se a cena ainda estiver no modelo antigo, tenta update() sem argumento.
        """
        if not self.scene or not hasattr(self.scene, "update"):
            return

        try:
            # Modelo novo: update recebe dt
            self.scene.update(dt)
        except TypeError:
            # Compatibilidade com cenas antigas que não recebem dt
            try:
                self.scene.update()
            except Exception as e:
                print(f"[WARN] Erro em {self.scene.__class__.__name__}.update(): {e}")
        except Exception as e:
            print(f"[WARN] Erro em {self.scene.__class__.__name__}.update(dt): {e}")

    def draw_scene(self):
        """
        Desenha a cena atual na tela virtual.

        Antes de desenhar, limpa a tela com preto.
        """
        self.virtual_screen.fill("black")

        if not self.scene or not hasattr(self.scene, "draw"):
            return

        try:
            self.scene.draw(self.virtual_screen)
        except Exception as e:
            print(f"[WARN] Erro em {self.scene.__class__.__name__}.draw(): {e}")

    def switch_scene_if_needed(self):
        """
        Verifica se a cena atual pediu troca de cena.

        Se self.scene.next existir e for diferente da cena atual:
        1. chama on_exit() da cena antiga
        2. troca para a nova cena
        3. chama on_enter() da nova cena
        """
        if not self.scene:
            return

        next_scene = getattr(self.scene, "next", None)

        if next_scene and next_scene is not self.scene:
            self._call_scene_hook(self.scene, "on_exit")
            self.scene = next_scene
            self._call_scene_hook(self.scene, "on_enter")

    def render_with_letterbox(self):
        """
        Renderiza a tela virtual dentro da janela real,
        preservando a proporção original do jogo.

        Se a janela tiver tamanho diferente da resolução base,
        a imagem é escalada e centralizada com barras pretas
        (letterbox) quando necessário.
        """
        # Obtém o tamanho atual da janela real
        current_width, current_height = self.display.get_size()

        # Calcula a escala ideal sem deformar a imagem
        scale = min(current_width / BASE_WIDTH, current_height / BASE_HEIGHT)

        # Novo tamanho proporcional da tela virtual
        new_width = int(BASE_WIDTH * scale)
        new_height = int(BASE_HEIGHT * scale)

        # Calcula o deslocamento para centralizar
        offset_x = (current_width - new_width) // 2
        offset_y = (current_height - new_height) // 2

        # Redimensiona a tela virtual para caber na janela
        scaled_surface = pygame.transform.scale(self.virtual_screen, (new_width, new_height))

        # Limpa a janela real e desenha a imagem escalada centralizada
        self.display.fill("black")
        self.display.blit(scaled_surface, (offset_x, offset_y))

        # Atualiza a tela
        pygame.display.flip()

    def run(self):
        """
        Loop principal do jogo.

        A cada frame:
        1. calcula o dt
        2. atualiza o controle
        3. processa eventos
        4. atualiza a cena
        5. desenha a cena
        6. troca de cena, se necessário
        7. renderiza com letterbox
        """
        try:
            while self.running:
                # Calcula o tempo entre frames em segundos
                dt = self.clock.tick(FPS) / 1000.0

                # Atualiza estados contínuos do controle
                try:
                    self.controller.update()
                except Exception as e:
                    print(f"[WARN] Controller.update() falhou: {e}")

                # Processa todos os eventos da fila
                for event in pygame.event.get():
                    self.handle_event(event)

                # Atualiza lógica da cena
                self.update_scene(dt)

                # Desenha a cena na tela virtual
                self.draw_scene()

                # Verifica se deve trocar de cena
                self.switch_scene_if_needed()

                # Exibe o resultado na janela
                self.render_with_letterbox()

        except SystemExit:
            # Permite encerramento normal
            pass

        except Exception:
            # Captura erro fatal e mostra traceback
            print("\n[ERRO FATAL NO GAME LOOP]")
            traceback.print_exc()
            pygame.time.delay(1200)

        finally:
            # Finalização segura do pygame
            pygame.quit()
            sys.exit()


# Ponto de entrada do programa
if __name__ == "__main__":
    game = Game()
    game.run()