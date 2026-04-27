import os
import pygame
from .hud_base_boss import BossHudBase


class BossHudMapinguari(BossHudBase):
    """
    HUD específica do Mapinguari.

    Regras:
    - vida 5 -> Hud_Mapinguari_5.png
    - vida 4 -> Hud_Mapinguari_4.png
    - vida 3 -> Hud_Mapinguari_3.png
    - vida 2 -> Hud_Mapinguari_2.png
    - vida 1 -> Hud_Mapinguari_1.png
    - vida 0 -> Hud_Mapinguari_0.png
    """

    DISPLAY_NAME = "Mapinguari"
    DEATH_PORTRAIT = os.path.join(
        "assets", "charsSprite", "bosses", "Mapinguari_D.png"
    )

    def __init__(self, position=(0, 0), size=(1280, 720)):
        images_by_value = self._load_images(size)

        super().__init__(
            position=position,
            size=size,
            images_by_value=images_by_value,
            initial_value=5
        )

    # =========================================================
    # ETAPA 1 - CARREGA AS IMAGENS DA HUD
    # =========================================================
    def _load_images(self, size):
        images = {}

        for i in range(6):
            path = os.path.join(
                "assets",
                "charsSprite",
                "bosses",
                f"Hud_Mapinguari_{i}.png"
            )

            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, size)
                images[i] = img
            except Exception as e:
                print(f"[WARN] Não foi possível carregar {path}: {e}")

                # fallback visual simples
                fallback = pygame.Surface(size, pygame.SRCALPHA)
                fallback.fill((120, 0, 0, 160))
                images[i] = fallback

        return images

    # =========================================================
    # ETAPA 2 - RETRATO DE MORTE PADRÃO
    # =========================================================
    def use_death_portrait(self):
        """
        Mantém a HUD em 0 e registra o retrato de morte do boss.
        """
        self.set(0)
        self.set_portrait(self.DEATH_PORTRAIT)