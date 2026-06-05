import pygame
from ..base import Scene
from script.core.obj import Obj
from ..char_select.char_select import Char_Select
# Utiliza a instância global compartilhada do controle
from script.controller import get_controller


# Criando Tela de Controles
class Control(Scene):
    """Classe para a tela de Controle."""
    
    def __init__(self):
        super().__init__()

        # =====================================================
        # Utiliza a mesma instância criada no main.py
        # =====================================================
        self.controller = get_controller()

        # Guarda o último tipo carregado
        self.current_controller_type = None

        # Imagem atual da tela
        self.img = None

        # Carrega a imagem inicial
        self._update_control_image(force=True)
    
    def _update_control_image(self, force=False):
        """
        Atualiza automaticamente a imagem da tela
        quando o controle é conectado ou desconectado.
        """

        controller_type = self.controller.get_controller_type()

        if not force and controller_type == self.current_controller_type:
            return

        self.current_controller_type = controller_type

        if controller_type == "playstation":
            image_path = "assets/controls/Control_PS.png"

        elif controller_type == "xbox":
            image_path = "assets/controls/Control_XBOX.png"

        else:
            image_path = "assets/controls/Control_Teclado.png"

        self.img = Obj(
            image_path,
            [0, 0],
            [self.all_sprites]
        )

        print(f"[CONTROL SCREEN] Atualizado para: {controller_type}")
    
    
    def handle_events(self, event):
        """Gerencia eventos de entrada do usuário na tela de Game Over."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.change_scene(Char_Select())  # Muda para a tela inicial            
        return super().handle_events(event)
    
    def update(self):
        """
        Verifica continuamente se houve mudança
        no controle conectado.
        """

        self._update_control_image()
    
    def draw(self, surface):
        """Desenha a tela de Game Over."""
        self.img.draw(surface)