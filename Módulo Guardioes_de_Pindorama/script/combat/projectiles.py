import pygame


class Shot(pygame.sprite.Sprite):
    """
    Classe do projétil disparado pelo Player.

    Otimização importante:
    - a imagem da flecha é carregada uma única vez
    - os projéteis reutilizam a imagem já pronta em memória
    """

    # =========================================================
    # ETAPA 1 - CONFIGURAÇÕES GERAIS DO PROJÉTIL
    # =========================================================

    SHOT_IMAGE_PATH = "assets/projectiles/Shot1.png"
    SCREEN_LIMIT_X = 2000

    # Cache compartilhado entre todas as flechas
    _image_cache = {}

    def __init__(
        self,
        x,
        y,
        direction,
        groups,
        size=(80, 25),
        speed=7,
        damage=1.0,
        charged=False
    ):
        super().__init__(groups)

        # =========================================================
        # ETAPA 2 - ATRIBUTOS PRINCIPAIS
        # =========================================================
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.charged = charged
        self.size = size

        # =========================================================
        # ETAPA 3 - IMAGEM OTIMIZADA
        # =========================================================
        self.image = self._get_cached_image()
        self.rect = self.image.get_rect(topleft=(x, y))

    # =========================================================
    # ETAPA 4 - CACHE DE IMAGENS
    # =========================================================

    def _get_cached_image(self):
        """
        Retorna a imagem já pronta do projétil.

        A chave do cache leva em conta:
        - tamanho
        - direção
        - se é charge shot ou não
        """
        cache_key = (self.size, self.direction, self.charged)

        if cache_key in Shot._image_cache:
            return Shot._image_cache[cache_key]

        # Se ainda não existe no cache, cria uma vez
        image = self._build_image()
        Shot._image_cache[cache_key] = image
        return image

    # =========================================================
    # ETAPA 5 - CONSTRUÇÃO VISUAL DO PROJÉTIL
    # =========================================================

    def _build_image(self):
        """
        Monta a imagem da flecha apenas uma vez por combinação.
        """
        try:
            image = pygame.image.load(self.SHOT_IMAGE_PATH).convert_alpha()
            image = pygame.transform.scale(image, self.size)

            if self.direction < 0:
                image = pygame.transform.flip(image, True, False)

            if self.charged:
                image = self._apply_charge_effect(image)

            return image

        except Exception as e:
            print(f"[WARN] Não foi possível carregar a flecha '{self.SHOT_IMAGE_PATH}': {e}")

            fallback = pygame.Surface(self.size, pygame.SRCALPHA)
            fallback.fill((255, 220, 100) if self.charged else (255, 255, 255))
            return fallback

    # =========================================================
    # ETAPA 6 - EFEITO VISUAL DO CHARGE SHOT
    # =========================================================

    def _apply_charge_effect(self, base_image):
        """
        Aplica um brilho simples na flecha carregada.
        """
        image = base_image.copy()

        glow = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        glow.fill((255, 220, 100, 80))
        image.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        return image

    # =========================================================
    # ETAPA 7 - MOVIMENTO
    # =========================================================

    def update(self):
        """
        Move a flecha e remove ao sair da tela.
        """
        self.rect.x += self.speed * self.direction

        if self.rect.right < -200 or self.rect.left > self.SCREEN_LIMIT_X:
            self.kill()