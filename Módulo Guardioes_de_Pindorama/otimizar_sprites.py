"""
otimizar_sprites.py
===================
Redimensiona e otimiza todos os PNGs/JPEGs do projeto
"Guardiões de Pindorama" para o tamanho real de uso.

Como usar:
    1. Coloque este arquivo na RAIZ do projeto (mesma pasta do main.py)
    2. Execute: python otimizar_sprites.py
    3. Um backup é criado automaticamente antes de qualquer alteração
    4. Ao final, um relatório mostra o espaço economizado

Requisito:
    pip install Pillow
"""

import os
import shutil
from pathlib import Path
from PIL import Image

# =============================================================
# CONFIGURAÇÃO — tamanhos alvo por pasta
# =============================================================
# Cada entrada define o tamanho (largura, altura) máximo para
# as imagens daquela pasta. Imagens menores que o alvo NÃO
# são ampliadas (só reduzidas). Proporção original é preservada.

REGRAS = {
    # Sprites do player em jogo — tamanho real usado no Player(size=(200,200))
    "assets/charsSprite/player": (200, 200),

    # HUD do player — ícones pequenos de vida/xp
    "assets/charsSprite/player/Hud": (120, 120),

    # Boss Mapinguari — size=(400,400) no código
    "assets/charsSprite/bosses": (400, 400),

    # Boss Matita Pereira — DEFAULT_SIZE=(275,300)
    "assets/charsSprite/bosses/Matita_Pereira": (275, 300),

    # NPCs
    "assets/charsSprite/npcs": (200, 200),

    # Tela de seleção de personagem — exibidos em janela 1280x720
    # imagens grandes de pose/capa podem ser um pouco maiores
    "assets/charSelect": (512, 512),

    # Sprites de cenário/level — backgrounds e tiles
    "assets/levelSprite": (1280, 720),

    # Menus, login, mapa
    "assets/menu": (1280, 720),
    "assets/login": (1280, 720),
    "assets/mapSelect": (1280, 720),

    # Chat e diálogos — retratos pequenos
    "assets/chatChar": (256, 256),

    # Projéteis — muito pequenos em tela
    "assets/projectiles": (128, 128),

    # Tela de game over
    "assets/gameover.png": (1280, 720),  # arquivo único
}

# Extensões tratadas
EXTENSOES = {".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"}

# Pasta de backup (criada automaticamente)
BACKUP_DIR = Path("assets_backup_original")

# =============================================================
# FUNÇÕES
# =============================================================

def tamanho_legivel(bytes_val):
    """Converte bytes para KB ou MB legível."""
    if bytes_val >= 1_000_000:
        return f"{bytes_val / 1_000_000:.1f} MB"
    return f"{bytes_val / 1_000:.1f} KB"


def fazer_backup(caminho: Path):
    """Copia o arquivo original para a pasta de backup antes de alterar."""
    destino = BACKUP_DIR / caminho
    destino.parent.mkdir(parents=True, exist_ok=True)
    if not destino.exists():
        shutil.copy2(caminho, destino)


def otimizar_imagem(caminho: Path, tamanho_alvo: tuple) -> tuple:
    """
    Redimensiona e salva a imagem se ela for maior que o tamanho alvo.
    Retorna (bytes_antes, bytes_depois).
    Preserva canal alpha (PNG) e proporção original.
    """
    bytes_antes = caminho.stat().st_size

    try:
        img = Image.open(caminho)
        w, h = img.size

        # Só reduz — nunca amplia
        if w <= tamanho_alvo[0] and h <= tamanho_alvo[1]:
            return (bytes_antes, bytes_antes)  # já está no tamanho certo

        # Calcula novo tamanho preservando proporção
        img.thumbnail(tamanho_alvo, Image.LANCZOS)

        # Salva mantendo o formato original
        ext = caminho.suffix.lower()
        if ext == ".png":
            img.save(caminho, format="PNG", optimize=True)
        else:
            # JPEG não suporta alpha — converte se necessário
            if img.mode in ("RGBA", "LA"):
                img = img.convert("RGB")
            img.save(caminho, format="JPEG", quality=90, optimize=True)

        bytes_depois = caminho.stat().st_size
        return (bytes_antes, bytes_depois)

    except Exception as e:
        print(f"  [ERRO] {caminho}: {e}")
        return (bytes_antes, bytes_antes)


def encontrar_regra(caminho: Path) -> tuple | None:
    """
    Encontra a regra de tamanho mais específica para um caminho.
    Regras mais longas (mais específicas) têm prioridade.
    """
    caminho_str = str(caminho).replace("\\", "/")
    melhor = None
    melhor_len = 0

    for pasta, tamanho in REGRAS.items():
        # Suporte a arquivo único (ex: assets/gameover.png)
        if pasta.endswith((".png", ".jpg", ".jpeg")):
            if caminho_str == pasta:
                return tamanho
            continue

        pasta_norm = pasta.rstrip("/") + "/"
        if caminho_str.replace("\\", "/").startswith(pasta_norm):
            if len(pasta) > melhor_len:
                melhor = tamanho
                melhor_len = len(pasta)

    return melhor


def processar_projeto():
    """Percorre todos os assets e aplica as otimizações."""

    print("=" * 60)
    print("  Guardiões de Pindorama — Otimizador de Sprites")
    print("=" * 60)
    print(f"\n📁 Backup será salvo em: {BACKUP_DIR}/")
    print("   (nenhum arquivo original será perdido)\n")

    total_antes = 0
    total_depois = 0
    total_arquivos = 0
    total_reduzidos = 0
    ignorados = 0

    # Percorre todos os arquivos de imagem dentro de assets/
    for caminho in sorted(Path("assets").rglob("*")):
        if caminho.suffix not in EXTENSOES:
            continue

        regra = encontrar_regra(caminho)

        if regra is None:
            ignorados += 1
            continue

        # Faz backup antes de alterar
        fazer_backup(caminho)

        antes, depois = otimizar_imagem(caminho, regra)
        total_antes += antes
        total_depois += depois
        total_arquivos += 1

        if depois < antes:
            economia = antes - depois
            pct = (economia / antes) * 100
            print(f"  ✅ {caminho.name:<40} "
                  f"{tamanho_legivel(antes):>8} → {tamanho_legivel(depois):>8}  "
                  f"(-{pct:.0f}%)")
            total_reduzidos += 1
        else:
            print(f"  ⏭  {caminho.name:<40} {tamanho_legivel(antes):>8}  (já otimizado)")

    # Relatório final
    economia_total = total_antes - total_depois
    print("\n" + "=" * 60)
    print(f"  Arquivos processados : {total_arquivos}")
    print(f"  Arquivos reduzidos   : {total_reduzidos}")
    print(f"  Ignorados (sem regra): {ignorados}")
    print(f"  Tamanho antes        : {tamanho_legivel(total_antes)}")
    print(f"  Tamanho depois       : {tamanho_legivel(total_depois)}")
    print(f"  Economia total       : {tamanho_legivel(economia_total)}")
    if total_antes > 0:
        pct_total = (economia_total / total_antes) * 100
        print(f"  Redução              : {pct_total:.1f}%")
    print("=" * 60)
    print(f"\n✅ Concluído! Backup original em: {BACKUP_DIR}/")
    print("   Se algo não ficou bem, é só copiar de volta do backup.\n")


# =============================================================
# PONTO DE ENTRADA
# =============================================================
if __name__ == "__main__":
    # Garante que está sendo executado na raiz do projeto
    if not Path("assets").exists():
        print("[ERRO] Pasta 'assets' não encontrada.")
        print("       Execute este script na raiz do projeto (mesma pasta do main.py).")
        exit(1)

    if not Path("main.py").exists():
        print("[AVISO] main.py não encontrado — confirme que está na raiz do projeto.")

    processar_projeto()