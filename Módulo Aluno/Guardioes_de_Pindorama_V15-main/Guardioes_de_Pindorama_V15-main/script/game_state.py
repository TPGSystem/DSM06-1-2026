# ===============================================================
#  GERENCIADOR DE ESTADO GLOBAL DO JOGO
#  ------------------------------------
#  Este arquivo centraliza todas as variáveis que controlam o
#  progresso do jogador no jogo, como:
#     - Personagem selecionado
#     - Áreas (fases) concluídas
#     - Inventário (itens, moedas, etc.)
#     - Flags (marcadores de eventos ou condições)
#
#  O objetivo é ter um único local de referência para o "estado
#  do jogo", evitando dados espalhados por várias classes.
#  Assim, se o jogador voltar para o menu principal, basta
#  chamar STATE.reset() para limpar tudo e recomeçar do zero.
#
#  ► Integração recomendada:
#     - Title.on_enter(): STATE.reset() (ou somente em "Novo Jogo")
#     - Level quando vence: STATE.complete_area("Level_1_2"); STATE.save()
#     - Map ao abrir: consultar STATE.is_area_completed() e STATE.is_area_unlocked()
#     - Em qualquer interação: STATE.add_item(), STATE.set_flag(), etc.
# ===============================================================

from __future__ import annotations

# dataclass facilita classes de dados (gera __init__, __repr__, etc.)
from dataclasses import dataclass, field
from pathlib import Path
import json
import tempfile
import os
from typing import Any


# =========================
# Persistência / versão
# =========================
STATE_VERSION = 1                    # versão do "schema" salvo no JSON (permite migrações futuras)
SAVE_PATH = Path("save/state.json")  # caminho único do arquivo de save

# Centralize aqui os nomes das áreas necessárias para liberar a área final.
# DICA: mantenha essa lista atualizada quando novas fases forem adicionadas.
REQUIRED_FOR_FINAL = {
    "Level_1_1",
    "Level_1_2",
    # acrescente as demais áreas necessárias...
}
# Nome exato da última área (bloqueada até concluir as anteriores)
FINAL_AREA_NAME = "Propugnáculo Além-Mar"

# ---------------------------------------------------------------
# Classe principal que armazena o estado do jogo
# ---------------------------------------------------------------
@dataclass(slots=True)
class GameState:
    """
    Representa o estado global do jogo durante a execução.

    Essa classe guarda as informações principais do progresso do jogador
    (como personagem, fases concluídas e inventário) e permite que sejam
    acessadas e modificadas por qualquer parte do código que precise
    dessas informações.

    ► Por que 'slots=True'?
      - Reduz consumo de memória e evita criação acidental de atributos
        não declarados (erros de digitação, por exemplo).
    """

    # Nome/ID do personagem escolhido na seleção (None se ainda não escolheu)
    selected_character: str | None = None

    # Dados do aluno autenticado
    student_id: int | None = None
    student_name: str | None = None
    student_ra: str | None = None

    # Dados da turma
    class_id: int | None = None
    class_name: str | None = None
    teacher_name: str | None = None
    school_year: int | None = None

    # Dados da partida criada pela API
    id_game: int | None = None
    id_match: int | None = None
    id_step: int | None = None
    gold: int = 0

    # Status do personagem
    score_strength: int = 0
    score_agility: int = 0
    score_resistance: int = 0
    score_wisdom: int = 0



    # Áreas concluídas pelo jogador (set evita duplicatas e facilita consulta)
    completed_areas: set[str] = field(default_factory=set)

    # Inventário do jogador: nome -> quantidade (ex.: {"Poção": 2, "Moedas": 37})
    inventory: dict[str, int] = field(default_factory=dict)

    # Flags de progresso/eventos: chave -> bool (ex.: {"falou_com_cacique": True})
    flags: dict[str, bool] = field(default_factory=dict)

    # -----------------------------------------------------------
    # Reset total do progresso (útil em "Novo Jogo" ou ao voltar ao Title)
    # -----------------------------------------------------------
    def reset(self):
        """
        Restaura o estado do jogo ao padrão inicial.
        Essa função é chamada quando o jogador retorna ao menu
        principal ou inicia um novo jogo.

        ► Efeitos:
          - Esquece personagem selecionado
          - Limpa áreas concluídas, inventário e flags
          - Não apaga o arquivo de save; apenas o estado em memória
        """
        self.student_id = None
        self.student_name = None
        self.student_ra = None

        self.class_id = None
        self.class_name = None
        self.teacher_name = None
        self.school_year = None

        self.id_game = None
        self.id_match = None
        self.id_step = None
        self.gold = 0

        self.score_strength = 0
        self.score_agility = 0
        self.score_resistance = 0
        self.score_wisdom = 0
        
        self.selected_character = None
        self.completed_areas.clear()
        self.inventory.clear()
        self.flags.clear()


    # -------------------------
    # Áreas (fases)
    # -------------------------
    def complete_area(self, area_name: str) -> None:
        """Marca a área como concluída (idempotente)."""
        if area_name:
            self.completed_areas.add(area_name)

    def is_area_completed(self, area_name: str) -> bool:
        """Retorna True se a área já foi concluída."""
        return area_name in self.completed_areas

    def is_area_unlocked(self, area: str) -> bool:
        """
        Regras de desbloqueio de áreas.
        ► Por padrão, todas as áreas estão liberadas, EXCETO a área final,
          que só libera após todas as áreas listadas em REQUIRED_FOR_FINAL
          constarem em completed_areas.
        """
        if area == FINAL_AREA_NAME:
            return REQUIRED_FOR_FINAL.issubset(self.completed_areas)
        return True

    # -------------------------
    # Inventário
    # -------------------------
    def add_item(self, name: str, qty: int = 1) -> None:
        """
        Adiciona 'qty' unidades do item 'name' ao inventário.
        Ignora quantidades <= 0 e nomes vazios.
        """
        if qty <= 0 or not name:
            return
        self.inventory[name] = self.inventory.get(name, 0) + qty

    def remove_item(self, name: str, qty: int = 1) -> None:
        """
        Remove 'qty' unidades do item 'name'. Se chegar a 0, remove a chave.
        Ignora se o item não existe ou se qty <= 0.
        """
        if qty <= 0 or name not in self.inventory:
            return
        new_qty = max(0, self.inventory[name] - qty)
        if new_qty == 0:
            del self.inventory[name]
        else:
            self.inventory[name] = new_qty

    # -------------------------
    # Flags (marcadores de progresso/diálogos/eventos)
    # -------------------------
    def set_flag(self, key: str, value: bool = True) -> None:
        """Define (ou atualiza) uma flag booleana."""
        if key:
            self.flags[key] = bool(value)

    def get_flag(self, key: str, default: bool = False) -> bool:
        """Obtém o valor de uma flag (ou 'default' se não existir)."""
        return self.flags.get(key, default)

    # -------------------------
    # Serialização (memória -> dicionário)
    # -------------------------
    def to_dict(self) -> dict[str, Any]:
        """
        Converte o estado atual para um dicionário pronto para salvar em JSON.
        Inclui 'version' para permitir migração de dados no futuro.
        """
                
        return {
            "version": STATE_VERSION,

            "student_id": self.student_id,
            "student_name": self.student_name,
            "student_ra": self.student_ra,

            "class_id": self.class_id,
            "class_name": self.class_name,
            "teacher_name": self.teacher_name,
            "school_year": self.school_year, 

            "id_game": self.id_game,
            "id_match": self.id_match,
            "id_step": self.id_step,
            "gold": self.gold,

            "score_strength": self.score_strength,
            "score_agility": self.score_agility,
            "score_resistance": self.score_resistance,
            "score_wisdom": self.score_wisdom,

            "selected_character": self.selected_character,
            "completed_areas": sorted(self.completed_areas),  # ordena só p/ ficar legível
            "inventory": dict(self.inventory),
            "flags": dict(self.flags),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GameState:
        """
        Constrói um GameState a partir de um dicionário salvo (tolerante a campos faltantes).
        ► Se 'version' do arquivo mudarem no futuro, implemente migrações aqui.
        """
        if not isinstance(data, dict):
            return cls()

        version = data.get("version", 0)
        # Ex.: if version == 0: migrar campos antigos para o novo formato.

        selected_character = data.get("selected_character")
        completed_areas = set(data.get("completed_areas", []))
        inventory = dict(data.get("inventory", {}))
        flags = dict(data.get("flags", {}))

        # Coerção leve de tipos (robustez contra saves antigos/inconsistentes)
        completed_areas = {str(x) for x in completed_areas}
        inventory = {str(k): int(v) for k, v in inventory.items()}
        flags = {str(k): bool(v) for k, v in flags.items()}

        student_id = data.get("student_id")
        student_name = data.get("student_name")
        student_ra = data.get("student_ra")

        class_id = data.get("class_id")
        class_name = data.get("class_name")
        teacher_name = data.get("teacher_name")
        school_year = data.get("school_year")

        id_game = data.get("id_game")
        id_match = data.get("id_match")
        id_step = data.get("id_step")
        gold = data.get("gold", 0)

        score_strength = data.get("score_strength", 0)
        score_agility = data.get("score_agility", 0)
        score_resistance = data.get("score_resistance", 0)
        score_wisdom = data.get("score_wisdom", 0)

        return cls(
            selected_character=(
                selected_character if (selected_character is None or isinstance(selected_character, str))
                else str(selected_character)
            ),
            completed_areas=completed_areas,
            inventory=inventory,
            flags=flags,

            student_id=student_id,
            student_name=student_name,
            student_ra=student_ra,

            class_id=class_id,
            class_name=class_name,
            teacher_name=teacher_name,
            school_year=school_year,

            id_game=id_game,
            id_match=id_match,
            id_step=id_step,
            gold=gold,

            score_strength=score_strength,
            score_agility=score_agility,
            score_resistance=score_resistance,
            score_wisdom=score_wisdom,
        )

    # -------------------------
    # Save / Load (persistência em disco)
    # -------------------------
    def save(self, path: Path = SAVE_PATH) -> None:
        """
        Salva o estado em JSON usando escrita atômica (escreve em arquivo temporário
        e depois substitui o destino). Isso reduz o risco de corrupção do save
        caso o jogo feche no meio do processo.

        ► Dica de uso: chame após eventos relevantes (concluir área, pegar item, etc.).
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_fd, temp_path = tempfile.mkstemp(prefix=".state_tmp_", dir=path.parent)
        try:
            with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
            os.replace(temp_path, path)  # substituição atômica (suportada na maioria dos SOs)
        except Exception:
            # Em caso de erro, remova o temporário e propague a exceção
            try:
                os.remove(temp_path)
            except Exception:
                pass
            raise

    def load(self, path: Path = SAVE_PATH) -> None:
        """
        Carrega o estado salvo, se existir. Em caso de erro de parsing/IO, mantém
        o estado atual e apenas registra um aviso no console.
        ► Importante: copiamos os campos para a instância existente para que
          todas as referências ao STATE global continuem válidas.
        """
        if not path.exists():
            return
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            loaded = self.from_dict(data)

            self.student_id = loaded.student_id
            self.student_name = loaded.student_name
            self.student_ra = loaded.student_ra

            self.class_id = loaded.class_id
            self.class_name = loaded.class_name
            self.teacher_name = loaded.teacher_name
            self.school_year = loaded.school_year

            self.id_game = loaded.id_game
            self.id_match = loaded.id_match
            self.id_step = loaded.id_step
            self.gold = loaded.gold

            self.score_strength = loaded.score_strength
            self.score_agility = loaded.score_agility
            self.score_resistance = loaded.score_resistance
            self.score_wisdom = loaded.score_wisdom

            # Copia campos (mantém o mesmo objeto STATE referenciado pelo projeto)
            self.selected_character = loaded.selected_character
            self.completed_areas = loaded.completed_areas
            self.inventory = loaded.inventory
            self.flags = loaded.flags
        except Exception as e:
            print(f"[WARN] Falha ao carregar estado: {e}")


# ---------------------------------------------------------------
# Instância global única do estado do jogo.
# ---------------------------------------------------------------
# Padrão de uso:
#   from script.game_state import STATE
#   STATE.complete_area("Level_1_2")
#   if STATE.is_area_unlocked("Propugnáculo Além-Mar"): ...
#
# ► Observação:
#   Evite reatribuir STATE = GameState() em outros módulos. Sempre reutilize esta
#   instância compartilhada para não perder referências nas cenas/objetos.
STATE = GameState()
