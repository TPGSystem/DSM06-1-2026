from models.database import db, Validations, Components, QuestionsTypes, Regions, Characters, YearsSeries, Teachers, Classes, Students, Themes, Skills, Questions, QuestionsSkills
from datetime import date
from werkzeug.security import generate_password_hash

class DataSeeder:
    @staticmethod
    def run():
        print("Iniciando carga de dados...")
        # 1. Tabelas Independentes (Nível 0)
        DataSeeder.seed_validations()
        DataSeeder.seed_components()
        DataSeeder.seed_question_types()
        DataSeeder.seed_regions()
        DataSeeder.seed_years_series()
        DataSeeder.seed_teachers()
        DataSeeder.seed_themes()
        db.session.commit() # Salva para gerar IDs necessários nas próximas etapas

        # 2. Tabelas Dependentes (Nível 1)
        DataSeeder.seed_characters() # Depende de Validations
        DataSeeder.seed_skills()     # Depende de Components
        DataSeeder.seed_classes()    # Depende de YearsSeries, Components e Teachers
        db.session.commit()

        # 3. Tabelas Dependentes (Nível 2)
        DataSeeder.seed_students()   # Depende de Classes
        DataSeeder.seed_questions()  # Depende de Themes, QuestionsTypes, Validations
        db.session.commit()

        # 4. Tabelas de Associação (Nível 3)
        DataSeeder.seed_questions_skills()
        db.session.commit()

        print("Carga de dados finalizada com sucesso!")
        
    @staticmethod
    def seed_validations():
        print("Populando Validations...")
        items = [Validations('Incorreta'), Validations('Correta'), Validations('Indígena'), Validations('Africano'), Validations('Europeu')]
        db.session.add_all(items)

    @staticmethod
    def seed_components():
        print("Populando Components...")
        db.session.add(Components('Arte'))

    @staticmethod
    def seed_question_types():
        print("Populando QuestionsTypes...")
        items = [QuestionsTypes('Etnia'), QuestionsTypes('Opção')]
        db.session.add_all(items)

    @staticmethod
    def seed_regions():
        print("Populando Regions...")
        names = [
            'Propugnáculo Além-Mar (Ilha Forte)', 'Vilarejo de Canaã', 'Vila da Enseada do Rio',
            'Povoado do Cadastro', 'Vilarejo dos Grandes Pássaros do Rio', 'Vale de Luz e Sombra',
            'Freguesia do Rio dos Peixes', 'Vilarejo de Praia Pequena', 'Vila do Pássaro Vermelho',
            'Vilarinho das Pedras que Fluem', 'Barragem do Arco-Íris', 'Vale dos Alecrins', 'Bosque dos Cajás'
        ]
        db.session.add_all([Regions(name) for name in names])

    @staticmethod
    def seed_characters():
        print("Populando Characters...")
        chars = [
            Characters(1, 3, 5, 15, 10, 10),
            Characters(3, 4, 10, 15, 10, 5),
            Characters(3, 5, 15, 10, 5, 10)
        ]
        db.session.add_all(chars)

    @staticmethod
    def seed_years_series():
        print("Populando YearsSeries...")
        items = [
            YearsSeries(2025, '9º A', '9º ano A'), YearsSeries(2025, '9º B', '9º ano B'),
            YearsSeries(2026, '9º A', '9º ano A'), YearsSeries(2026, '9º B', '9º ano B')
        ]
        db.session.add_all(items)

    @staticmethod
    def seed_teachers():
        print("Populando Teachers...")
        hashed_password = generate_password_hash('123')
        
        db.session.add(Teachers(
            name='Raphael Pedretti', 
            eMail='aphael.silva130fatec.sp.gov.br@gmail.com', # Alterado de 'email' para 'eMail'
            password=hashed_password
        ))
        
    @staticmethod
    def seed_classes():
        print("Populando Classes...")
        # schoolYear, idYearSerie, idComponent, IdTeacher
        items = [
            Classes(2025, 1, 1, 1), 
            Classes(2026, 3, 1, 1), 
            Classes(2026, 4, 1, 1)
        ]
        db.session.add_all(items)

    @staticmethod
    def seed_students():
        print("Populando Students...")
        # name, ra, password, birth, idClass
        items = [
            Students(
                name='Gilberto Satyro', 
                ra='000001', 
                password=generate_password_hash('111'), 
                birth=date(1970, 8, 19), 
                idClass=3
            ),
            Students(
                name='Pedro Xavier', 
                ra='000002', 
                password=generate_password_hash('222'), 
                birth=date(2010, 1, 1), 
                idClass=3
            ),
            Students(
                name='Renato Valente', 
                ra='000003', 
                password=generate_password_hash('333'), 
                birth=date(1990, 7, 1), 
                idClass=3
            )
        ]
        db.session.add_all(items)
        
    @staticmethod
    def seed_themes():
        print("Populando Themes...")
        names = ['Instrumentos Musicais', 'Lutas', 'Escrita', 'Alimentação', 'Cores']
        db.session.add_all([Themes(name) for name in names])

    @staticmethod
    def seed_skills():
        print("Populando Skills...")
        # idComponent, skill, comment, skillCodeCP, skillCodeBNCC
        items = [
            Skills(1, 'Instrumentos musicais', 'Identificar instrumentos musicais', '', ''),
            Skills(1, 'Lutas', 'Identificar as lutas', '', ''),
            Skills(1, 'Escrita', 'Identificar a escrita', '', ''),
            Skills(1, 'Cores', 'Estudo das cores', '', ''),
            Skills(1, 'Alimentação', 'Alimentos', '', '')
        ]
        db.session.add_all(items)

    @staticmethod
    def seed_questions():
        print("Populando Questions...")
        questions_list = []

        # 1. INSTRUMENTOS (ETNIA)
        questions_list.append(Questions(
            idTheme=1, idQuestionType=1, idRegion=None,
            question='Nossa música é mais do que som: é uma oração viva, conectando-nos aos espíritos das matas e rios. Diga-me, jovem guerreiro, quais instrumentos nossos ancestrais utilizam para conversar com os deuses da natureza?',
            response1='Instrumentos de sopro, geralmente feitos de bambu ou ossos de animais.',
            response2='Instrumentos de percussão, feitos de troncos ocos e couro de animais esticados.',
            response3='Instrumentos de corda, como violinos e harpas, com corpo de madeira e cordas de metal.',
            response4='Instrumentos eletrônicos que possuem energia elétrica para funcionar.',
            picture1=None, picture2=None, picture3=None, picture4=None,
            idValidation1=3, idValidation2=4, idValidation3=5, idValidation4=1
        ))

        # 2. LUTAS (ETNIA)
        questions_list.append(Questions(
            idTheme=2, idQuestionType=1, idRegion=None,
            question='Nossa etnia possui muitos guerreiros que utilizam diversos tipos de armas, desde armas de impacto até projetos, mas a luta desarmada também é essencial. Com base nessa reflexão, qual estilo de luta nossa etnia prática?',
            response1='Jiu-jitsu, com foco em agarrões, quedas no solo e ações imobilizadas.',
            response2='Boxe, com socos rápidos e técnicas de defesa.',
            response3='Capoeira, com ginga, golpes de pernas, acrobacias e movimentos rítmicos.',
            response4='Huka-Huka, luta de levantamento, derrubadas, agarrões e imobilizações.',
            picture1=None, picture2=None, picture3=None, picture4=None,
            idValidation1=1, idValidation2=5, idValidation3=4, idValidation4=3
        ))

        # 3. ESCRITA (ETNIA)
        questions_list.append(Questions(
            idTheme=3, idQuestionType=1, idRegion=None,
            question='Antes da chegada de outros povos, nossos ancestrais já narraram histórias com símbolos vivos. Que forma de comunicação usamos para registrar saberes e tradições?',
            response1='Faixas Decorativas com formas geométricas, linhas e tramas em estamparia de roupas, em que as cores também são classificadas como um systema de código e escrita.',
            response2='Caligrafia, uso de tintas e papiros para registro de palavras, usando elementos simbólicos ou signos, que representam letras e números.',
            response3="Pedras com símbolos esculpidos que são conhecidas como 'Runas', sendo jogadas e dependendo da ordem e sequencia que caírem significa uma informação.",
            response4='Pinturas Corporais, com hachuras, linhas e tramas, que utilizam pigmentos naturais extraídos de minérios e vegetais.',
            picture1=None, picture2=None, picture3=None, picture4=None,
            idValidation1=4, idValidation2=5, idValidation3=1, idValidation4=3
        ))

        # 4. ESCRITA (ETNIA 2)
        questions_list.append(Questions(
            idTheme=3, idQuestionType=1, idRegion=None,
            question='Nossa língua vive em palavras que muitos falam sem conhecer sua origem. Quais são as origens do coração da nossa terra?',
            response1='Mesa, Relógio, Camiseta, Hospital, Cerveja.',
            response2='Zen, Quimono, Origami, Chá, Sushi.',
            response3='Igarapé, Jabuticaba, Caiçara, Mirim, Pindorama.',
            response4='Moleque, Maracatu, Caxixi, Fubá, Dendê.',
            picture1=None, picture2=None, picture3=None, picture4=None,
            idValidation1=5, idValidation2=1, idValidation3=3, idValidation4=4
        ))

        # 5. ALIMENTAÇÃO (ETNIA)
        questions_list.append(Questions(
            idTheme=4, idQuestionType=1, idRegion=None,
            question='A terra nos sustenta e a comida que cultivamos reflete quem somos. Qual é a essência da nossa culinária, que fortalece o corpo e honra a tradição?',
            response1='Mandioca, Milho, Peixe, Frutas, Carne.',
            response2='Milho, Feijão, Mandioca, Dendê, Couve.',
            response3='Peixe, Batata, Trigo, Azeite, Ervas.',
            response4='Peixe, Arroz, Algas, Shoyu, Tofu.',
            picture1=None, picture2=None, picture3=None, picture4=None,
            idValidation1=3, idValidation2=4, idValidation3=5, idValidation4=1
        ))

        # 6. CORES (GERAL)
        questions_list.append(Questions(
            idTheme=5, idQuestionType=2, idRegion=None,
            question='Na publicidade e nas artes visuais, o uso de cores complementares é uma estratégia para criar contraste. Qual cor oferece o máximo contraste com o Azul no círculo cromático?',
            response1='Laranja, pois é a cor oposta ao azul no círculo cromático.',
            response2='Verde, pois faz parte das cores análogas ao azul.',
            response3='Violeta, por ser uma cor secundária próxima ao azul.',
            response4='Amarelo, apenas por ser uma cor primária como o azul.',
            picture1=None, picture2=None, picture3=None, picture4=None,
            idValidation1=2, idValidation2=1, idValidation3=1, idValidation4=1
        ))

        # 7. LUTAS (ETNIA 2 - ESPAÇO)
        questions_list.append(Questions(
            idTheme=2, idQuestionType=1, idRegion=None,
            question='O local onde treinamos e lutamos é sagrado. Em qual destes espaços você se sente conectado à força de sua linhagem?',
            response1='No centro da Aldeia (Terreiro), em círculo, onde o corpo toca a terra batida.',
            response2='Na Roda, ao som do berimbau, onde o corpo joga com a liberdade.',
            response3='No Ginásio ou Arena, seguindo regras de cavalaria e honra.',
            response4='No Octógono cercado por grades, foco em combate total moderno.',
            picture1=None, picture2=None, picture3=None, picture4=None,
            idValidation1=3, idValidation2=4, idValidation3=5, idValidation4=1
        ))

        # 8. INSTRUMENTOS (ETNIA 2 - FUNÇÃO)
        questions_list.append(Questions(
            idTheme=1, idQuestionType=1, idRegion=None,
            question='Qual a principal função das melodias que regem a sua cultura e organização social?',
            response1='A invocação de espíritos e a marcação de rituais de passagem pelo Pajé.',
            response2='A preservação da história oral e resistência em festejos como o Congado.',
            response3='A harmonização de missas e festas populares com canto coral.',
            response4='A produção de ondas sonoras sintéticas para batidas eletrônicas.',
            picture1=None, picture2=None, picture3=None, picture4=None,
            idValidation1=3, idValidation2=4, idValidation3=5, idValidation4=1
        ))

        # 9. LUTAS (GERAL - REGRAS)
        questions_list.append(Questions(
            idTheme=2, idQuestionType=2, idRegion=None,
            question='O que diferencia uma luta competitiva esportiva de um combate real de sobrevivência?',
            response1='A existência de um sistema de regras rígidas e árbitros para garantir a integridade.',
            response2='A obrigatoriedade de utilizar armas de fogo em competições.',
            response3='A ausência total de qualquer técnica de defesa.',
            response4='A proibição de saudações ao adversário antes da luta.',
            picture1=None, picture2=None, picture3=None, picture4=None,
            idValidation1=2, idValidation2=1, idValidation3=1, idValidation4=1
        ))

        # 10. INSTRUMENTOS (GERAL - IDIOFONES)
        questions_list.append(Questions(
            idTheme=1, idQuestionType=2, idRegion=None,
            question='Como chamamos a categoria onde o som é gerado pela vibração do próprio corpo do instrumento?',
            response1='Idiofones, pois o som é produzido pelo material sólido ao ser percutido.',
            response2='Aerofones, pois dependem exclusivamente do vácuo.',
            response3='Eletrofones, pois necessitam de cabos de fibra óptica.',
            response4='Cordofones, porque possuem cordas invisíveis.',
            picture1=None, picture2=None, picture3=None, picture4=None,
            idValidation1=2, idValidation2=1, idValidation3=1, idValidation4=1
        ))

        # 11. ESCRITA (GERAL - PRENSA)
        questions_list.append(Questions(
            idTheme=3, idQuestionType=2, idRegion=None,
            question='Qual foi a principal consequência social da invenção da prensa de Gutenberg?',
            response1='A democratização do acesso ao conhecimento e produção de livros em escala.',
            response2='O fim imediato de todas as línguas faladas.',
            response3='A proibição do uso de papel em favor de telas líquidas.',
            response4='O aumento do preço dos livros para colecionadores exclusivos.',
            picture1=None, picture2=None, picture3=None, picture4=None,
            idValidation1=2, idValidation2=1, idValidation3=1, idValidation4=1
        ))

        # 12. ALIMENTAÇÃO (GERAL - GUIA)
        questions_list.append(Questions(
            idTheme=4, idQuestionType=2, idRegion=None,
            question='Segundo o Guia Alimentar para a População Brasileira, qual deve ser a base da nossa alimentação?',
            response1='Alimentos in natura ou minimamente processados.',
            response2='Alimentos ultraprocessados, ricos em corantes.',
            response3='Suplementos vitamínicos sintéticos em cápsulas.',
            response4='Apenas alimentos líquidos e pastosos.',
            picture1=None, picture2=None, picture3=None, picture4=None,
            idValidation1=2, idValidation2=1, idValidation3=1, idValidation4=1
        ))
                        
        db.session.add_all(questions_list)

    @staticmethod
    def seed_questions_skills():
        print("Populando QuestionsSkills...")

        # Definindo a variável (Certifique-se que o nome aqui é o mesmo do 'for')
        target_series = [3, 4] 
        
        for serie_id in target_series:
            relations_batch = [
                # Usando idYearSerie conforme o seu __init__
                QuestionsSkills(idQuestion=1, idSkill=1, idYearSerie=serie_id, difficulty=1, available=True),
                QuestionsSkills(idQuestion=2, idSkill=2, idYearSerie=serie_id, difficulty=1, available=True),
                QuestionsSkills(idQuestion=3, idSkill=3, idYearSerie=serie_id, difficulty=2, available=True),
                QuestionsSkills(idQuestion=4, idSkill=3, idYearSerie=serie_id, difficulty=3, available=True),
                QuestionsSkills(idQuestion=5, idSkill=5, idYearSerie=serie_id, difficulty=3, available=True), 
                QuestionsSkills(idQuestion=6, idSkill=4, idYearSerie=serie_id, difficulty=3, available=True), 
                QuestionsSkills(idQuestion=7, idSkill=2, idYearSerie=serie_id, difficulty=2, available=True), 
                QuestionsSkills(idQuestion=8, idSkill=1, idYearSerie=serie_id, difficulty=2, available=True), 
                QuestionsSkills(idQuestion=9, idSkill=2, idYearSerie=serie_id, difficulty=1, available=True), 
                QuestionsSkills(idQuestion=10, idSkill=1, idYearSerie=serie_id, difficulty=2, available=True), 
                QuestionsSkills(idQuestion=11, idSkill=3, idYearSerie=serie_id, difficulty=3, available=True), 
                QuestionsSkills(idQuestion=12, idSkill=5, idYearSerie=serie_id, difficulty=1, available=True)
            ]
            db.session.add_all(relations_batch)
                        