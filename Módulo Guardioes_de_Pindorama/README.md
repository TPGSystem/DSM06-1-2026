# Guardiões de Pindorama — V20

> Jogo sério educacional desenvolvido em Python + Pygame, integrado ao ecossistema TPG System por meio de API REST, com foco em trilhas pedagógicas gamificadas, narrativa interativa e monitoramento pedagógico.

---

## 📌 Sobre o Projeto

Guardiões de Pindorama é um jogo digital 2D desenvolvido como módulo do estudante dentro do ecossistema TPG System (Trilha Pedagógica Gamificada).

O projeto integra:

- exploração de mapa;
- narrativa interativa;
- combate em tempo real;
- quizzes pedagógicos;
- tomadas de decisão;
- progressão por áreas;
- persistência de progresso;
- integração com API;
- monitoramento pedagógico.

A proposta busca unir game design, gamificação e aprendizagem significativa por meio de referências culturais brasileiras, ancestralidade, folclore nacional e linguagens artísticas.

---

## 🎯 Objetivos

O projeto possui como finalidade:

- promover engajamento por meio de jogos digitais;
- integrar conteúdos pedagógicos à experiência narrativa;
- acompanhar o progresso do estudante;
- registrar métricas de jogabilidade;
- auxiliar avaliações diagnósticas e formativas;
- estruturar trilhas pedagógicas gamificadas.

---

## 🧠 Estrutura do Ecossistema TPG System

O sistema é composto por três módulos principais:

### 🎮 Guardiões de Pindorama
Módulo jogável do estudante responsável por:

- gameplay;
- exploração;
- combate;
- quizzes;
- narrativa;
- progressão;
- sincronização de dados.

### 🖥️ Módulo Gestor
Responsável por:

- gerenciamento pedagógico;
- banco de questões;
- habilidades e competências;
- estudantes e turmas;
- relatórios pedagógicos.

### 🌐 API de Integração
Responsável por:

- persistência de dados;
- comunicação entre módulos;
- sincronização de progresso;
- autenticação;
- armazenamento de partidas;
- integração com banco de dados.

---

## ⚙️ Tecnologias Utilizadas

### Jogo
- Python 3.12+
- Pygame
- JSON

### API
- Flask
- SQLAlchemy
- MySQL
- PyMySQL
- Flask-CORS

### Ferramentas
- Git / GitHub
- Figma
- VSCode
- PyCharm
- Pygbag (testes Web)

---

## 🕹️ Funcionalidades Implementadas

### ✅ Sistema de Personagem
- movimentação lateral;
- ataque;
- dash / roll;
- defesa;
- disparos;
- charge shot;
- animações por estado.

### ✅ Sistema de Mapa
- progressão por áreas;
- desbloqueio de regiões;
- controle de conclusão;
- seleção via teclado e joystick.

### ✅ Sistema de Diálogo
- ChatBox customizada;
- identificação de personagens;
- diálogos narrativos;
- eventos condicionais.

### ✅ Sistema de Decisão
- escolhas narrativas;
- bifurcação de fluxo;
- controle de estados.

### ✅ Sistema de Quiz
- perguntas contextualizadas;
- integração pedagógica;
- validação de respostas.

### ✅ Sistema de Boss
- inteligência artificial;
- movimentação dinâmica;
- ataques especiais;
- sistema de dano;
- controle de vida.

### ✅ Sistema de Salvamento
- persistência em JSON;
- gerenciamento de progresso;
- controle de áreas concluídas.

### ✅ Integração API
- comunicação Flask ↔ Pygame;
- persistência relacional;
- sincronização de progresso;
- endpoints REST.

---

## 📁 Estrutura Geral do Projeto

```text
TPGSystem/
│
├── API/
│   ├── app.py
│   ├── models/
│   ├── routes/
│   ├── database/
│   └── templates/
│
├── Guardioes_de_Pindorama/
│   ├── assets/
│   ├── docs/
│   ├── save/
│   ├── script/
│   ├── main.py
│   └── requirements.txt
│
└── README.md
```

---

## 🔧 Requisitos

### Linguagens e Dependências
- Python 3.12+
- PIP atualizado

---

## 🧪 Criar Ambiente Virtual

### Windows
```bash
python -m venv venv
```

### Ativar ambiente virtual
```bash
venv\Scripts\activate
```

---

## 📦 Instalar Dependências do Jogo

```bash
pip install pygame
```

ou

```bash
pip install -r requirements.txt
```

---

## 📦 Instalar Dependências da API

```bash
pip install flask
pip install flask_sqlalchemy
pip install flask_cors
pip install pymysql
```

---

## ▶️ Executar o Jogo

```bash
python main.py
```

---

## ▶️ Executar a API

```bash
python app.py
```

A API será iniciada em:

```text
http://localhost:5000
```

---

## 🎮 Controles

| Ação | Tecla |
|---|---|
| Movimentação | A / D ou ← → |
| Pular | Espaço |
| Ataque | Q |
| Interação | E |
| Defesa | K |
| Dash / Roll | Shift |
| Pausa | ESC |

---

## 🌐 Integração com API

A versão V20 amplia a arquitetura do projeto por meio da integração entre o jogo e uma API REST baseada em Flask.

### Recursos Integrados
- gerenciamento de estudantes;
- gerenciamento de turmas;
- banco de questões;
- habilidades e competências;
- desafios;
- partidas;
- progresso do jogador;
- relatórios.

---

## 💾 Persistência de Dados

O sistema atualmente utiliza:

- salvamento local em JSON;
- persistência relacional;
- sincronização entre módulos.

---

## 🧾 Estado Atual do Projeto

### ✅ Implementado
- sistema de cenas;
- sistema de mapa;
- combate;
- IA de boss;
- quizzes;
- decisões;
- integração inicial com API;
- persistência local;
- joystick;
- diálogos;
- sistema de pausa.

### 🔄 Em Refinamento
- sincronização completa com banco;
- dashboard pedagógico;
- balanceamento de gameplay;
- otimização Web;
- refinamento de IA;
- integração total entre módulos.

---

## 👥 Equipe do Projeto

### Raphael Pedretti da Silva
- UI/UX Designer
- Game Designer
- Desenvolvimento do módulo jogável
- Integração narrativa e pedagógica

### Gilberto de Sousa Satyro
- Backend
- API
- Banco de Dados
- Arquitetura de Sistema

### Pedro Xavier da Veiga
- Front-end
- Estrutura visual
- Interfaces

### Renato José Valente
- Estruturação documental
- Organização de módulos
- Apoio visual

---

## 📄 Licença

Projeto acadêmico e experimental.

Licenciamento em definição.
