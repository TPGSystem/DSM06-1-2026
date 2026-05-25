# Biblioteca de Decisões

class Decisão_1_2:
    """Biblioteca contendo as decisões narrativas da fase 1_2."""

    decisoes = {
        "Mapinguari": {
            "id": "seguir_vale_luz_sombra",
            "titulo": "Momento de Decisão:",
            "pergunta": "'Será que vale a pena seguir a pista do Mapinguari e ir direto explorar a Região do Vale da Luz e Sombra?'",
            "opcoes": [
                "SIM - Vá direto para a Região do Vale da Luz e Sombra.",
                "NÃO - Explore os territórios livremente e decida para qual localidade quer ir."
            ],
        },

        "Matita_Pereira": {
            "id": "seguir_vale_dos_alecrins",
            "titulo": "Momento de Decisão:",
            "pergunta": "'Será que vale a pena seguir a pista da Matita Pereira e ir direto explorar a Região do Vale dos Alecrins?'",
            "opcoes": [
                "SIM - Vá direto para a Região do Vale dos Alecrins.",
                "NÃO - Explore os territórios livremente e decida para qual localidade quer ir."
            ],
        },
    }

    @classmethod
    def get_decisao(cls, boss_name):
        return cls.decisoes.get(boss_name, cls.decisoes["Mapinguari"])