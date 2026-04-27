# Game Design Document (GDD)
## Guardiões de Pindorama

**Versão do documento:** 1.0  
**Natureza do documento:** documentação técnica de design e desenvolvimento do jogo  
**Projeto vinculado:** TPG System – Trilha Pedagógica Gamificada  
**Plataforma-base do protótipo:** Python + Pygame

---

## 1. Visão geral do jogo

**Guardiões de Pindorama** é um jogo digital em 2D, de aventura e ação, desenvolvido como módulo do estudante dentro do ecossistema **TPG System**. O projeto foi concebido para integrar narrativa interativa, progressão por mapa, desafios baseados em conhecimento, combate em tempo real e mediação pedagógica em uma mesma experiência de uso.

No contexto mais amplo do sistema, o jogo constitui a interface de interação do estudante com a trilha pedagógica gamificada. Seu papel é transformar conteúdos, desafios e percursos de aprendizagem em uma experiência ludicamente orientada, estruturada por fases, eventos narrativos, escolhas e provas contextualizadas. O artigo do projeto explicita que essa proposta está voltada ao engajamento de estudantes do 9º ano do Ensino Fundamental, com foco no componente curricular Arte, articulando também conhecimentos interdisciplinares e relatórios de acompanhamento para o professor.

Do ponto de vista técnico, o protótipo já apresenta fluxo funcional de cenas, personagem jogável, progressão por áreas, sistema de diálogos, quiz contextualizado, enfrentamento de chefe, persistência de estado e integração com dispositivos de entrada alternativos. Esses elementos configuram um projeto jogável e tecnicamente estruturado, apto à documentação formal em GDD.

---

## 2. Finalidade deste documento

Este documento tem por objetivo registrar, de forma clara e técnica, os principais componentes de design, funcionamento e implementação observados em **Guardiões de Pindorama**, servindo como referência para análise, continuidade do desenvolvimento, validação institucional e documentação do projeto.

O GDD não substitui o artigo acadêmico do sistema nem sua fundamentação pedagógica completa. Sua função é traduzir essa proposta para a lógica do jogo, descrevendo como a intencionalidade do projeto se materializa em estrutura jogável, fluxo de interação, organização de sistemas, mecânicas, progressão e interface.

---

## 3. Posicionamento do projeto no TPG System

O artigo define o **TPG System** como uma Trilha Pedagógica Gamificada com elementos de RPG, organizada para promover engajamento, desenvolvimento, consolidação e aprofundamento de habilidades e competências, especialmente no componente Arte, ao mesmo tempo em que integra relatórios diagnósticos e de acompanhamento para professores. O jogo **Guardiões de Pindorama** ocupa, nesse sistema, a função de módulo interativo do estudante.

Assim, o jogo deve ser compreendido como parte de uma arquitetura mais ampla, composta por:

- **módulo do estudante**, representado pelo jogo em Pygame;
- **módulo gestor do professor**, descrito no artigo como interface de monitoramento e geração de relatórios;
- **camada de dados**, voltada ao registro do progresso e apoio à análise pedagógica. 

Esse posicionamento é importante porque determina decisões de design. O jogo não foi planejado apenas como produto de entretenimento, mas como interface operacional de uma trilha gamificada com função formativa e diagnóstica.

---

## 4. Gênero, escopo e proposta funcional

### 4.1 Gênero principal

- aventura 2D;
- ação com progressão narrativa;
- jogo sério de caráter educativo.

### 4.2 Subgêneros e aproximações

- plataforma lateral com exploração;
- narrativa guiada por diálogos e eventos;
- quiz contextualizado;
- progressão por mapa;
- combate em tempo real com boss.

### 4.3 Escopo do protótipo atual

Com base no protótipo documentado anteriormente e na arquitetura observada, o jogo já contempla:

- tela inicial e entrada no sistema;
- menu principal;
- fluxo de seleção e navegação entre cenas;
- mapa com progressão entre áreas;
- fases jogáveis estruturadas;
- personagem jogável com múltiplos estados;
- interação com NPCs;
- sistema de diálogo;
- quizzes e decisões narrativas;
- sistema de pausa;
- enfrentamento de chefe;
- persistência de progresso.

---

## 5. Objetivos de design do jogo

### 5.1 Objetivo geral do módulo jogável

Oferecer ao estudante uma experiência digital interativa capaz de articular ação, narrativa, desafio e conteúdo em uma estrutura de progressão clara, envolvente e tecnicamente consistente.

### 5.2 Objetivos funcionais

- permitir navegação por fluxo de cenas e áreas do mapa;
- oferecer uma jornada estruturada por etapas, desafios e validações de progresso;
- integrar diálogos, quizzes e decisões ao avanço da experiência;
- sustentar combate, exploração e interação em uma mesma base jogável;
- registrar estados de avanço do jogador.

### 5.3 Objetivos relacionados ao sistema ampliado

O artigo indica que o sistema busca permitir identificação de níveis de proficiência, diagnóstico de habilidades não consolidadas, acompanhamento do progresso e oferta de desafios adequados ao desenvolvimento individual do estudante. Dentro dessa lógica, o jogo funciona como ambiente de execução desses desafios e de coleta de evidências de percurso. 

---

## 6. Público-alvo do jogo

No plano educacional do sistema, o artigo aponta estudantes do **9º ano do Ensino Fundamental** como público de referência, com foco no componente curricular **Arte** e nas linguagens artísticas, sem excluir articulações interdisciplinares. Também identifica os professores como usuários indiretos, responsáveis pela leitura dos resultados e pelo planejamento pedagógico a partir dos dados gerados.

No plano técnico-jogável, o público imediato do módulo é o jogador-estudante, que interage com personagens, desafios, quizzes, combates e deslocamento por áreas. Já no plano institucional, o projeto também se dirige a avaliadores acadêmicos, docentes e equipes interessadas em **Jogos Sério**s e **Gamificação Pedagógica**.

---

## 7. Conceito de jogo

O conceito central de **Guardiões de Pindorama** se organiza como uma aventura de travessia, restauração e enfrentamento. O jogador assume o papel de um protagonista jovem inserido em um território simbólico marcado por referências culturais brasileiras, por personagens orientadores e por ameaças que precisam ser superadas para restabelecer um equilíbrio comprometido.

Em termos de design, o conceito do jogo se apoia em quatro eixos:

### 7.1 Jornada narrativa
A progressão é construída como percurso. O jogador não apenas executa ações isoladas, mas percorre um mundo em que narrativa, contexto e desafios se articulam.

### 7.2 Progressão por conquista
O avanço é condicionado à superação de áreas, à resolução de desafios e ao cumprimento de objetivos específicos, reforçando a percepção de campanha.

### 7.3 Integração entre ação e conhecimento
Os quizzes e as decisões não aparecem como elementos externos à jogabilidade, mas como pontos de validação e continuidade do próprio fluxo.

### 7.4 Identidade cultural
A ambientação, os personagens e a nomeação do universo reforçam uma identidade temática ligada a referências culturais brasileiras e à ancestralidade, o que dá singularidade ao projeto.

---

## 8. Estrutura macro da experiência

A experiência do jogador pode ser representada por um ciclo macro de navegação:

1. entrada no sistema;
2. passagem pela tela inicial e menu;
3. preparação e seleção;
4. acesso ao mapa;
5. escolha de área/fase;
6. exploração, narrativa e desafios locais;
7. conclusão da etapa;
8. registro do progresso e retorno ao mapa.

Esse fluxo é importante porque organiza a experiência como percurso contínuo, e não como conjunto fragmentado de telas. O mapa funciona como articulador de campanha, enquanto as fases concentram a densidade de interação.

---

## 9. Estrutura de cenas

### 9.1 Tela inicial / Login
A entrada no sistema exerce função de acesso, organização do primeiro contato e preparação do fluxo subsequente. Ainda que, em versões de teste, os sistemas de autenticação possam estar simplificados, essa cena mantém sua função estrutural como ponto de entrada institucional do módulo.

### 9.2 Menu principal
O menu principal organiza o acesso às funções fundamentais do jogo. Nele se concentram ações de início, navegação inicial e encerramento. Sua importância está na mediação entre identidade visual e usabilidade.

### 9.3 Seleções e preparação
O projeto contempla telas ligadas à preparação do percurso, como seleção de personagem e, em alguns fluxos, passagem para o mapa ou escolha de áreas.

### 9.4 Mapa
O mapa atua como sistema de progressão macro. É nele que o jogador visualiza áreas disponíveis, áreas concluídas e regiões ainda bloqueadas. A referência à área final **Propugnáculo Além-Mar** indica uma estrutura de bloqueio por requisitos e um objetivo de campanha de longo alcance.

### 9.5 Fases jogáveis
As fases concentram movimentação, diálogos, decisões, quizzes e combate. São o núcleo da jogabilidade e da execução do conteúdo.

### 9.6 Pausa
A pausa atua como sobreposição funcional, interrompendo momentaneamente a ação sem romper a experiência. É recurso importante de usabilidade e expansão futura.

### 9.7 Encerramento / falha
A existência de estados de derrota ou transição reforça a lógica de ciclo de tentativa, correção e retomada.

---

## 10. Personagem jogável

O personagem principal funciona como avatar do jogador e eixo de integração entre narrativa, deslocamento, interação e combate.

### 10.1 Funções principais

- deslocar-se pelas fases;
- interagir com NPCs e gatilhos de evento;
- participar de quizzes e escolhas;
- enfrentar ameaças e chefes;
- atualizar o avanço da campanha.

### 10.2 Ações observáveis no protótipo

A documentação do protótipo e a organização dos estados do personagem indicam ações como:

- movimentação lateral;
- salto;
- ataque;
- defesa/bloqueio;
- roll/dash;
- interação;
- progressão de diálogo.

### 10.3 Papel de design

O personagem jogável foi construído para sustentar variedade de estados sem comprometer a legibilidade da ação. Essa decisão é relevante porque o jogo combina leitura, combate e exploração, exigindo transições compreensíveis e responsivas.

---

## 11. Mecânicas principais

### 11.1 Exploração
A exploração estrutura o avanço espacial do jogador. Seu papel é permitir deslocamento, descoberta de gatilhos, encontros com personagens e acesso aos pontos de desafio.

### 11.2 Interação narrativa
A narrativa é transmitida por meio de diálogos sequenciados, imagens, falas de NPCs e eventos encadeados. Esse sistema guia o jogador e contextualiza tanto a missão quanto os desafios locais.

### 11.3 Quiz contextualizado
O artigo afirma que o sistema utiliza desafios intelectuais como questionários, análise de dados e imagens, quebra-cabeças e batalhas virtuais. No módulo jogável, isso se materializa em quizzes e decisões integradas à narrativa e à progressão.

### 11.4 Decisão narrativa
A presença de escolhas confere agência ao jogador e modula o avanço narrativo. Em termos de design, esse recurso amplia envolvimento e evita que o percurso se reduza a repetição linear de comandos.

### 11.5 Combate
O combate funciona como mecânica de tensão e prova de domínio das ações básicas do personagem. Sua presença dá ritmo à jornada e materializa o conflito do mundo do jogo.

### 11.6 Progressão por mapa
A progressão por mapa fornece uma representação clara do percurso global do jogador e sustenta bloqueio/desbloqueio de áreas com base no avanço registrado.

---

## 12. Sistema de combate

O sistema de combate foi estruturado para oferecer uma base jogável de ação em tempo real compatível com o estágio do protótipo.

### 12.1 Componentes do sistema

- ataque direto;
- defesa/bloqueio;
- mobilidade tática por salto e deslocamento;
- roll/dash como recurso adicional de ação;
- confronto com inimigos e boss.

### 12.2 Boss de fase

A presença do **Mapinguari** como chefe de fase é um marco técnico e dramático importante. Em termos de design, o boss exerce múltiplas funções:

- elevar a exigência mecânica do jogador;
- condensar o conflito narrativo da etapa;
- marcar momentos de clímax;
- reforçar a identidade mítica e cultural do jogo.

### 12.3 Valor sistêmico

O combate evita que o jogo se restrinja a leitura de eventos e resolução de perguntas. Ele amplia o repertório de interação e equilibra os tempos de ação e reflexão.

---

## 13. NPCs e personagens relevantes

### 13.1 Cacique
O **Cacique** exerce função de orientação, convocação narrativa e mediação entre jogador e missão. Sua presença organiza a entrada do protagonista no conflito e fortalece a dimensão simbólica do universo do jogo.

### 13.2 Mapinguari
O **Mapinguari** ocupa posição de antagonismo ou prova dramática relevante. Sua função ultrapassa o simples papel de inimigo, pois também consolida o tom do mundo ficcional e o peso dos confrontos.

### 13.3 Protagonista
O protagonista, frequentemente referido como **Jovem Guerreiro** na documentação do protótipo, funciona como ponto de convergência entre narrativa, ação e aprendizagem.

---

## 14. Narrativa e ambientação

A narrativa de **Guardiões de Pindorama** se estrutura como jornada de restauração em um território simbólico atravessado por ancestralidade, referências culturais brasileiras, conflito e reparação.

### 14.1 Premissa
Um desequilíbrio atinge o mundo do jogo e convoca o protagonista a percorrer áreas, receber orientação, enfrentar ameaças e superar provas para restaurar a ordem comprometida.

### 14.2 Temas centrais

- equilíbrio entre natureza e ação humana;
- responsabilidade coletiva;
- travessia e amadurecimento;
- ancestralidade;
- valorização cultural;
- missão e reparação.

### 14.3 Função da narrativa no design

A narrativa não é apenas decorativa. Ela organiza o sentido da exploração, justifica os combates, contextualiza os quizzes e sustenta a progressão da campanha.

---

## 15. Sistema de desafios pedagógicos no jogo

Embora este GDD mantenha foco técnico, é necessário registrar como os desafios de conteúdo se integram ao design, pois isso afeta diretamente a arquitetura do jogo.

O artigo informa que o sistema foi concebido para estimular estudantes por meio de interface digital de jogo, oferecendo questionários, análise de dados e imagens, quebra-cabeças e batalhas virtuais. Também afirma que os resultados serão integrados à interface do professor, apoiando monitoramento e relatórios de habilidades desenvolvidas, recuperadas e consolidadas.

No módulo jogável, essa diretriz se traduz em:

- quizzes inseridos no fluxo da fase;
- validação de avanço por resposta ou decisão;
- articulação entre narrativa e conteúdo;
- feedback sobre acerto e erro;
- continuidade da progressão condicionada ao desempenho do jogador.

Em termos de design de sistema, isso significa que o jogo precisa manter mecanismos de:

- chamada e exibição de questões;
- registro de resposta;
- retorno visual ao jogador;
- encadeamento entre resultado e próximo evento;
- integração entre dados do desafio e estado global do jogo.

---

## 16. Progressão e estrutura do mundo

### 16.1 Áreas e campanha
A progressão do jogo é organizada por áreas acessadas via mapa. Cada área representa uma etapa do percurso e pode conter narrativa local, combate, desafios e registros específicos de conclusão.

### 16.2 Bloqueios e desbloqueios
O sistema utiliza condições de acesso para liberar áreas posteriores. A área final, **Propugnáculo Além-Mar**, atua como destino condicionado ao cumprimento prévio de objetivos nas demais regiões.

### 16.3 Valor técnico
Essa estrutura fortalece:

- clareza de meta para o jogador;
- organização de conteúdo por etapa;
- escalabilidade para expansão futura;
- controle sistêmico do avanço.

---

## 17. Interface, HUD e feedbacks

A interface do jogo é uma camada central de comunicação entre sistema e jogador.

### 17.1 Elementos observados

- menu principal com navegação por cursor;
- molduras e telas de interface;
- retratos e imagens de apoio aos diálogos;
- HUD do jogador;
- HUD do boss;
- feedbacks de resposta correta e incorreta;
- sobreposição de pausa.

### 17.2 Função técnica

A interface organiza a leitura do estado atual do jogo, do resultado das ações e da progressão dos eventos. Em um projeto que mescla combate, leitura e desafios cognitivos, essa camada é decisiva para a usabilidade.

### 17.3 Qualidade de design observada

A presença de assets dedicados à HUD, ao boss, aos diálogos e ao enquadramento visual demonstra preocupação em manter consistência e reconhecimento de estados, o que reforça a identidade do projeto e melhora a experiência de uso.

---

## 18. Controles e entrada do jogador

O projeto foi desenvolvido com suporte a teclado e joystick, o que amplia versatilidade técnica e capacidade de experimentação.

### 18.1 Dispositivos suportados

- teclado;
- controle/joystick;
- integração com joystick analógico via Arduino Leonardo, no contexto ampliado do sistema. O artigo registra explicitamente essa integração IoT como parte do desenvolvimento técnico do projeto.

### 18.2 Implicações de design

O suporte a múltiplos dispositivos exige:

- abstração adequada dos comandos;
- consistência entre entrada e resposta do personagem;
- testes de usabilidade em diferentes perfis de controle;
- previsibilidade de navegação em menus e em ação.

---

## 19. Direção de arte e identidade visual

A direção de arte do jogo constitui um de seus elementos de maior singularidade.

### 19.1 Características gerais

- visual 2D autoral;
- uso de sprites, ilustrações e molduras dedicadas;
- personagens com forte identidade temática;
- ambientação de aventura simbólica e mítica;
- presença de elementos visuais associados à cultura brasileira.

### 19.2 Ferramentas relacionadas à produção visual

O artigo registra que a criação visual do projeto utilizou ferramentas como **Hero Forge**, **Inkscape**, **Krita** e plataformas de IA generativa, além de validação de interface em **Figma** para o módulo gestor. Essas informações ajudam a compreender o pipeline artístico e de prototipação vinculado ao projeto.

### 19.3 Função da arte no design

A arte não é apenas estética. Ela comunica estados, reforça a narrativa, diferencia personagens, sustenta a imersão e contribui para a legibilidade do sistema.

---

## 20. Estrutura técnica do protótipo

### 20.1 Base tecnológica

O artigo informa que o jogo “Guardiões de Pindorama” foi desenvolvido em **Python** com a biblioteca **Pygame**, enquanto o módulo gestor foi implementado em **Flask** e o banco de dados estruturado em **MySQL**. A tabela de ferramentas apresentada na página 6 consolida esse ecossistema de desenvolvimento. fileciteturn2file0L106-L124 fileciteturn2file0L149-L169

### 20.2 Componentes estruturais identificados no jogo

- arquivo principal de inicialização e loop;
- organização por cenas;
- módulos para diálogos, decisões e dados de fase;
- sistema de estado global;
- persistência em arquivo;
- organização de assets por função;
- suporte a HUD e sobreposições.

### 20.3 Qualidade arquitetural

A modularização observada indica preocupação com manutenção, crescimento e clareza funcional. Essa base favorece iteração contínua e refinamento do protótipo.

---

## 21. Persistência e estado global

O sistema de save e estado global é essencial para a coerência da experiência.

### 21.1 Funções principais

- registrar áreas concluídas;
- armazenar condições de desbloqueio;
- manter flags de progressão narrativa;
- sustentar continuidade entre sessões de jogo.

### 21.2 Importância para o design

Sem persistência, a proposta perderia sua natureza de trilha progressiva. O registro do percurso é requisito técnico fundamental para um jogo que depende de campanha, desbloqueio e retorno ao mapa.

---

## 22. Metodologia de desenvolvimento

O artigo informa que o desenvolvimento técnico da aplicação adotou a metodologia ágil **Scrum**, com organização em sprints, revisões iterativas e melhorias contínuas com base em feedbacks de professores e estudantes. Isso ajuda a compreender o estágio do protótipo como resultado de desenvolvimento incremental, e não como construção linear fechada.

Do ponto de vista do GDD, essa informação é importante porque explica:

- a natureza iterativa do projeto;
- a coexistência de sistemas já consolidados e pontos ainda em refinamento;
- a abertura do protótipo à evolução de design, tecnologia e conteúdo.

---

## 23. Estado atual do desenvolvimento

Com base na versão analisada e no artigo, o projeto já apresenta um estágio consistente de prototipação funcional.

### 23.1 Elementos consolidados

- identidade temática definida;
- módulo jogável em Python/Pygame;
- fluxo principal de navegação implementado;
- mapa e progressão por áreas;
- personagem jogável com múltiplos estados;
- diálogos e quizzes integrados à narrativa;
- combate e boss de fase;
- suporte a joystick/IoT no ecossistema do projeto;
- integração planejada com módulo gestor e relatórios.

### 23.2 Aspectos em continuidade

O próprio artigo aponta próximos passos como:

- incorporação de IA para análise de dados e geração personalizada de questões;
- investigação de motores como Unity, Unreal e Godot para aprimoramento gráfico;
- expansão da plataforma para dispositivos móveis.

Em termos de design do jogo, isso sugere continuidade de polimento visual, ampliação de conteúdos, amadurecimento técnico e expansão de alcance da solução.

---

## 24. Considerações finais

**Guardiões de Pindorama** é um jogo tecnicamente estruturado para operar como módulo interativo do estudante dentro do **TPG System**. Sua arquitetura combina narrativa, progressão por mapa, quizzes, combate, interação com NPCs, persistência e interface dedicada, compondo uma base jogável consistente.

O artigo do projeto esclarece que essa implementação não foi concebida como jogo isolado, mas como parte de uma proposta de trilha pedagógica gamificada, direcionada ao componente curricular Arte, ao engajamento de estudantes do 9º ano do Ensino Fundamental e ao apoio à prática docente por meio de relatórios e monitoramento. Esse enquadramento fortalece a leitura técnica do jogo, porque demonstra que sua estrutura de design responde a finalidades concretas de uso.

Como documento técnico, este GDD registra a lógica de funcionamento do jogo, seus sistemas centrais, suas decisões de design e seu posicionamento dentro da solução mais ampla. A continuidade do desenvolvimento tende a fortalecer ainda mais a integração entre arquitetura jogável, qualidade visual, controle de progressão e escalabilidade do projeto.
