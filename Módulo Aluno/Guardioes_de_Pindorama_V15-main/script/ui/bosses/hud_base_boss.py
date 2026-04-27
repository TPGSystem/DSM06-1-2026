import pygame


class BossHudBase:
    """
    HUD base para chefes.

    Responsável por:
    - armazenar imagens por valor de vida
    - trocar a HUD conforme a vida do boss
    - desenhar na tela
    - suportar retrato opcional
    """

    def __init__(self, position=(0, 0), size=(1280, 720), images_by_value=None, initial_value=5):
        self.position = position
        self.size = size
        self.images = images_by_value or {}
        self.value = int(initial_value)

        if self.value not in self.images and self.images:
            self.value = max(self.images.keys())

        self.image = self.images.get(self.value)
        self.rect = self.image.get_rect(topleft=self.position) if self.image else pygame.Rect(position, size)

        # suporte opcional
        self.portrait_surface = None
        self.portrait_path = None

    # =========================================================
    # ETAPA 1 - ATUALIZA O VALOR EXIBIDO
    # =========================================================
    def set(self, value):
        """
        Atualiza a HUD para o valor de vida informado.
        """
        value = int(value)

        if not self.images:
            self.value = value
            return

        min_value = min(self.images.keys())
        max_value = max(self.images.keys())

        self.value = max(min_value, min(max_value, value))
        self.image = self.images[self.value]

    # =========================================================
    # ETAPA 2 - RETRATO OPCIONAL
    # =========================================================
    def set_portrait(self, portrait_path):
        """
        Guarda um retrato opcional. Pode ser usado futuramente se você quiser.
        """
        self.portrait_path = portrait_path
        try:
            self.portrait_surface = pygame.image.load(portrait_path).convert_alpha()
        except Exception as e:
            print(f"[WARN] Não foi possível carregar retrato do boss: {e}")
            self.portrait_surface = None

    # =========================================================
    # ETAPA 3 - DESENHO
    # =========================================================
    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)