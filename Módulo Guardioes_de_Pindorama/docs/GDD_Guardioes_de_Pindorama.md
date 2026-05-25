# Game Design Document (GDD)
# Guardiões de Pindorama — V20

**Versão do documento:** 2.0  
**Natureza do documento:** documentação técnica de design e desenvolvimento do jogo  
**Projeto vinculado:** TPG System – Trilha Pedagógica Gamificada  
**Plataforma-base do protótipo:** Python + Pygame + API Flask  
**Versão da linguagem:** Python 3.12+

---

# 1. Visão geral do jogo

**Guardiões de Pindorama** é um jogo digital em 2D, de aventura e ação, desenvolvido como módulo do estudante dentro do ecossistema **TPG System**. O projeto foi concebido para integrar narrativa interativa, progressão por mapa, desafios baseados em conhecimento, combate em tempo real, persistência de progresso e mediação pedagógica em uma mesma experiência de uso.

Na versão V20, o projeto amplia sua arquitetura por meio da integração entre:

- jogo em Pygame;
- API REST em Flask;
- persistência relacional;
- sincronização de progresso;
- gerenciamento pedagógico;
- estrutura de dados para dashboards e relatórios.

O jogo constitui a interface de interação do estudante com a trilha pedagógica gamificada, transformando conteúdos, desafios e percursos de aprendizagem em uma experiência ludicamente orientada, estruturada por fases, eventos narrativos, escolhas e provas contextualizadas.

O projeto está voltado ao engajamento de estudantes do 9º ano do Ensino Fundamental, com foco no componente curricular Arte, articulando conhecimentos interdisciplinares e relatórios de acompanhamento pedagógico.

Do ponto de vista técnico, o protótipo já apresenta:

- fluxo funcional de cenas;
- personagem jogável;
- progressão por áreas;
- sistema de diálogos;
- quizzes contextualizados;
- sistema de decisões;
- enfrentamento de boss;
- persistência local;
- integração API;
- suporte a joystick;
- sincronização estrutural de dados.

---

# 2. Finalidade deste documento

Este documento possui como finalidade registrar, de forma técnica e estruturada, os principais componentes de design, arquitetura e funcionamento observados em **Guardiões de Pindorama**, servindo como referência para:

- continuidade do desenvolvimento;
- validação institucional;
- documentação acadêmica;
- organização do pipeline;
- refinamento técnico;
- expansão futura do projeto.

O GDD não substitui o artigo acadêmico do sistema, mas traduz sua proposta pedagógica para a lógica do jogo e de sua arquitetura interativa.

---

# 3. Posicionamento do projeto no TPG System

O **TPG System** é estruturado como uma Trilha Pedagógica Gamificada com elementos de RPG, organizada para promover:

- engajamento;
- desenvolvimento de competências;
- consolidação de habilidades;
- acompanhamento pedagógico;
- monitoramento do estudante.

Dentro desse ecossistema, **Guardiões de Pindorama** ocupa a função de módulo interativo do estudante.

A arquitetura geral do sistema é composta por:

- módulo do estudante;
- módulo gestor do professor;
- API de integração;
- camada de persistência relacional.

---

# 4. Estrutura do Ecossistema

## 4.1 Guardiões de Pindorama

Módulo jogável responsável por:

- exploração;
- narrativa;
- combate;
- quizzes;
- decisões;
- progressão;
- sincronização de progresso.

---

## 4.2 Módulo Gestor

Interface pedagógica voltada para:

- gerenciamento de estudantes;
- gerenciamento de turmas;
- habilidades e competências;
- banco de questões;
- relatórios pedagógicos.

---

## 4.3 API de Integração

A API REST em Flask é responsável por:

- autenticação;
- persistência;
- sincronização;
- integração entre módulos;
- armazenamento relacional;
- comunicação entre jogo e banco de dados.

---

# 5. Gênero, escopo e proposta funcional

## 5.1 Gênero principal

- aventura 2D;
- ação;
- RPG;
- jogo sério educacional.

---

## 5.2 Subgêneros e aproximações

- plataforma lateral;
- exploração;
- narrativa interativa;
- quiz contextualizado;
- progressão por mapa;
- boss fight.

---

## 5.3 Escopo atual do protótipo

A versão V20 contempla:

- tela inicial;
- login;
- menu principal;
- seleção de personagem;
- seleção de áreas;
- mapa com progressão;
- fases jogáveis;
- sistema de diálogos;
- sistema de quiz;
- sistema de decisões;
- sistema de pausa;
- boss fight;
- persistência local;
- integração API.

---

# 6. Objetivos de design

## 6.1 Objetivos pedagógicos

- promover engajamento estudantil;
- integrar narrativa e conteúdo;
- estimular aprendizagem significativa;
- apoiar avaliação diagnóstica;
- registrar progresso do estudante.

---

## 6.2 Objetivos técnicos

- integrar jogo + API + banco de dados;
- estruturar persistência híbrida;
- implementar arquitetura modular;
- consolidar sincronização online/offline.

---

# 7. Público-alvo

## Público pedagógico

- estudantes do 9º ano do Ensino Fundamental;
- componente curricular Arte;
- linguagens artísticas.

---

## Público técnico

- pesquisadores;
- desenvolvedores;
- avaliadores acadêmicos;
- pesquisadores de jogos sérios e gamificação.

---

# 8. Conceito de jogo

O conceito central de **Guardiões de Pindorama** se organiza como uma jornada de travessia, restauração e enfrentamento.

O jogador assume o papel de um jovem guardião responsável por restaurar o equilíbrio espiritual de diferentes regiões ameaçadas por forças corrompidas.

O conceito se apoia em quatro eixos:

## 8.1 Jornada narrativa

A progressão é estruturada como percurso contínuo.

---

## 8.2 Progressão por conquista

O avanço depende da superação de desafios, áreas e eventos específicos.

---

## 8.3 Integração entre ação e conhecimento

Quizzes e decisões fazem parte da progressão narrativa.

---

## 8.4 Identidade cultural

A ambientação reforça referências culturais brasileiras, ancestralidade e folclore nacional.

---

# 9. Estrutura macro da experiência

O fluxo principal do jogador ocorre por meio de:

1. entrada no sistema;
2. menu principal;
3. seleção de personagem;
4. acesso ao mapa;
5. escolha de área;
6. exploração;
7. combate;
8. quizzes e decisões;
9. boss fight;
10. progressão;
11. retorno ao mapa.

---

# 10. Estrutura de cenas

## 10.1 Tela inicial / Login

Responsável pelo acesso ao sistema e preparação da experiência.

---

## 10.2 Menu principal

Centraliza:
- iniciar jogo;
- opções;
- saída.

---

## 10.3 Seleção de personagem

Permite escolha de:
- etnias;
- profissões;
- gênero;
- status.

---

## 10.4 Mapa

O mapa funciona como sistema macro de progressão.

Responsável por:
- desbloqueio de regiões;
- controle de conclusão;
- navegação entre áreas.

A área final **Propugnáculo Além-Mar** permanece bloqueada até a conclusão das demais regiões principais.

---

## 10.5 Fases jogáveis

Concentram:
- exploração;
- narrativa;
- combate;
- quizzes;
- decisões.

---

## 10.6 Sistema de pausa

Sobreposição funcional responsável por:
- interrupção temporária;
- acesso rápido a opções;
- gerenciamento de fluxo.

---

# 11. Personagem jogável

O personagem principal funciona como avatar do jogador.

## 11.1 Funções principais

- deslocamento;
- interação;
- combate;
- progressão narrativa;
- exploração.

---

## 11.2 Ações implementadas

- movimentação lateral;
- salto;
- ataque;
- defesa;
- roll/dash;
- disparos;
- charge shot;
- interação;
- progressão de diálogo.

---

# 12. Mecânicas principais

## 12.1 Exploração

Permite:
- deslocamento;
- descoberta de eventos;
- interação com NPCs;
- acesso a desafios.

---

## 12.2 Interação narrativa

Narrativa transmitida por:
- diálogos;
- eventos;
- imagens;
- NPCs;
- escolhas.

---

## 12.3 Quiz contextualizado

Os quizzes atuam como:
- validação de conhecimento;
- progressão narrativa;
- desafio pedagógico.

---

## 12.4 Decisão narrativa

As decisões permitem:
- bifurcação de fluxo;
- alteração de eventos;
- mudanças narrativas.

---

## 12.5 Combate

O combate funciona como:
- prova de domínio;
- tensão dramática;
- reforço da progressão.

---

# 13. Sistema de combate

O combate é estruturado em tempo real.

## 13.1 Componentes principais

- ataque;
- defesa;
- movimentação tática;
- projéteis;
- colisão;
- boss fight.

---

## 13.2 Boss de fase

O boss principal atual é o **Mapinguari**.

Funções no design:
- clímax narrativo;
- desafio mecânico;
- consolidação temática;
- aumento de tensão.

---

## 13.3 Comportamento do Mapinguari

O boss opera por:
- perseguição dinâmica;
- marcação de posição;
- deslocamento orientado;
- pausa estratégica;
- ataques de corrida.

---

## 13.4 Estados de comportamento

- idle inicial;
- movimentação orientada;
- idle pós-movimento;
- investida;
- movimentação aleatória controlada.

---

## 13.5 Ajustes implementados

- refinamento de velocidade;
- correção esquerda/direita;
- ajustes de animação;
- aumento de velocidade de corrida;
- refinamento de investida.

---

## 13.6 Implementações futuras previstas

- hitbox;
- sistema de colisão refinado;
- dano no jogador;
- feedback visual no HUD.

---

# 14. Sistema pós-combate

Após o confronto com o boss ocorre:

- diálogo final;
- sistema de decisão;
- alteração narrativa;
- atualização de estados globais.

---

# 15. NPCs e personagens relevantes

## 15.1 Cacique

Responsável por:
- orientação narrativa;
- contextualização;
- mediação do conflito.

---

## 15.2 Mapinguari

Representa:
- antagonismo;
- desafio dramático;
- identidade mítica do jogo.

---

## 15.3 Jovem Guerreiro

Protagonista responsável pela travessia narrativa e integração entre:
- combate;
- exploração;
- aprendizagem.

---

# 16. Narrativa e ambientação

A narrativa se estrutura a partir de:

- ancestralidade;
- cultura brasileira;
- etnias;
- folclore nacional;
- restauração espiritual;
- equilíbrio do mundo.

---

# 17. Sistema de desafios pedagógicos

O sistema integra:

- quizzes;
- desafios;
- perguntas contextualizadas;
- validação de progresso;
- registro de desempenho.

---

# 18. Progressão e estrutura do mundo

## 18.1 Progressão por áreas

Cada região representa:
- uma etapa narrativa;
- um conjunto de desafios;
- uma condição de avanço.

---

## 18.2 Bloqueios e desbloqueios

A progressão depende da conclusão de áreas anteriores.

---

# 19. Interface e HUD

## Elementos implementados

- menu principal;
- molduras;
- HUD do jogador;
- HUD do boss;
- ChatBox;
- feedbacks visuais;
- pause overlay.

---

# 20. Controles e entrada do jogador

## 20.1 Teclado

| Ação | Tecla |
|---|---|
| Movimentação | A / D |
| Pulo | Espaço |
| Ataque | Q |
| Interação | E |
| Defesa | K |
| Dash / Roll | Shift |
| Pausa | ESC |

---

## 20.2 Controle (Xbox / PS4)

O sistema possui suporte para:
- D-Pad;
- analógicos;
- botões de ação;
- navegação em menus.

---

# 21. Direção de arte

A proposta visual utiliza:
- pixel art;
- ambientação folclórica;
- referências indígenas;
- cenários naturais;
- estética narrativa regional.

---

# 22. Estrutura técnica do protótipo

## 22.1 Base tecnológica

- Python 3.12+
- Pygame
- Flask
- SQLAlchemy
- MySQL
- PyMySQL
- JSON

---

## 22.2 Estrutura arquitetural observada

- sistema de cenas;
- estado global;
- persistência;
- HUD;
- módulos de diálogo;
- módulos de decisão;
- API REST;
- persistência relacional.

---

# 23. Persistência e estado global

## Persistência local

Atualmente baseada em:
- JSON;
- save/state.json.

---

## Persistência remota

Estruturada para:
- MySQL;
- sincronização API;
- armazenamento relacional.

---

# 24. Estrutura da API

## Recursos integrados

- students;
- teachers;
- classes;
- skills;
- questions;
- reports;
- play;
- gamesChallenges;
- gamesMatches;
- gamesQuestions;
- gamesSteps.

---

# 25. Expansão Web

O projeto já passou por testes utilizando:
- Pygbag;
- WebAssembly;
- adaptação para navegador.

---

# 26. Metodologia de desenvolvimento

O desenvolvimento adota:
- Scrum;
- organização em sprints;
- refinamento contínuo;
- testes iterativos.

---

# 27. Estado atual do desenvolvimento

## Sistemas consolidados

- combate;
- mapa;
- diálogos;
- quizzes;
- decisões;
- boss;
- persistência local;
- integração API inicial;
- joystick.

---

## Sistemas em refinamento

- sincronização online completa;
- analytics;
- dashboards pedagógicos;
- otimização Web;
- balanceamento de gameplay.

---

# 28. Perspectivas futuras

Planejamentos futuros:
- multiplayer pedagógico;
- dashboards inteligentes;
- analytics;
- expansão de regiões;
- novos bosses;
- novos personagens;
- versão Web otimizada.

---

# 29. Equipe do Projeto

## Raphael Pedretti da Silva
- UI/UX Designer
- Game Designer
- Desenvolvimento do módulo jogável
- Integração narrativa e pedagógica

---

## Gilberto de Sousa Satyro
- Backend
- API
- Banco de Dados
- Arquitetura de Sistema

---

## Pedro Xavier da Veiga
- Front-end
- Interfaces
- Estrutura visual

---

## Renato José Valente
- Organização documental
- Apoio visual
- Estruturação modular

---

# 30. Considerações finais

A versão V20 representa uma evolução estrutural significativa do projeto, especialmente pela consolidação da integração entre:

- gameplay;
- persistência;
- API;
- relatórios;
- trilhas pedagógicas;
- sincronização de dados.

O projeto amplia seu potencial técnico e pedagógico ao integrar jogo, monitoramento e persistência em um ecossistema gamificado educacional.
