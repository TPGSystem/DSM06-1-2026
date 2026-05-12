from flask import render_template, request, redirect, url_for, flash, session
import urllib
import json
import requests
from werkzeug.security import generate_password_hash,check_password_hash
from markupsafe import Markup

def init_app(app):
    @app.before_request
    def check_auth():
        # Rotas que não precisaram de autenticação
        routes = ['login','caduser','home']
        # Se a rota atual não requisitar autenticação, permitir acesso
        if request.endpoint in routes or request.path.startswith('/static/'):
            return
        # Se o usuário não estiver autenticado redireciona para página de login
        if 'teacher_id' not in session:
           return redirect(url_for('login')) 
    @app.route('/')
    def home():
        return render_template('index.html')


    # ROTA PARA PROFESSOR
    @app.route('/cadastro', methods=['GET', 'POST'])
    def caduser():
        if request.method == 'POST':
            name = request.form.get('name')
            eMail = request.form.get('eMail')
            password = request.form.get('password')

            teacher_data = json.dumps({
                'name': name,
                'eMail': eMail,
                'password': password
            })

            req = urllib.request.Request(
                url='http://127.0.0.1:5000/teachers',
                data=teacher_data.encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST'
            )

            try:
                with urllib.request.urlopen(req) as resp:
                    if resp.status == 201:
                        return redirect(url_for('login'))
            except Exception as e:
                print('Erro ao cadastrar o professor:', e)

            return redirect(url_for('caduser'))

        return render_template('cadUser.html')


    # ROTA PARA GRAFICO
    @app.route('/graphics')
    def graphics():
        with urllib.request.urlopen('http://127.0.0.1:5000/students') as resp:
            students = json.loads(resp.read().decode())
        with urllib.request.urlopen('http://127.0.0.1:5000/classes') as resp:
            classes = json.loads(resp.read().decode())
        return render_template('graphic.html',students=students,classes=classes)


    # ROTAS PARA ALUNO
    # Get
    @app.route('/Student')
    def student():
        with urllib.request.urlopen('http://127.0.0.1:5000/students') as resp:
            students = json.loads(resp.read().decode())
        return render_template('Student.html',students=students)
    # Create
    @app.route('/cadStudent', methods=['GET','POST'])
    def cadstudent():
        if request.method == 'POST':
            name = request.form.get('name')
            ra = request.form.get('ra')
            password = request.form.get('senha')
            birth = request.form.get('birth')
            idClass = request.form.get('classe')

            student_data = json.dumps({
                'name': name,
                'ra': ra,
                'password': password,
                'birth': birth,
                'idClass': idClass
            })

            req = urllib.request.Request(
                url='http://127.0.0.1:5000/students',
                data=student_data.encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST'
            )

            try:
                with urllib.request.urlopen(req) as resp:
                    if resp.status == 201:
                        return redirect(url_for('student'))
            except Exception as e:
                print('Erro ao cadastrar o aluno:', e)

        with urllib.request.urlopen('http://127.0.0.1:5000/classes') as resp:
            classes = json.loads(resp.read().decode())

        return render_template('cadStudent.html',classes=classes)
    # Get - ID
    @app.route('/editStudent/<int:id>')
    def editStudent(id):
        with urllib.request.urlopen(f'http://127.0.0.1:5000/students/{id}') as resp:
            student = json.loads(resp.read().decode())
        with urllib.request.urlopen('http://127.0.0.1:5000/classes') as resp:
            classes = json.loads(resp.read().decode())
        return render_template('editStudent.html',student=student,classes=classes)
    # Update
    @app.route('/updateStudent/<int:id>', methods=['POST'])
    def updatestudent(id):
        data = {
            'name': request.form['name'],
            'ra': request.form['ra'],
            'password': request.form['senha'],
            'birth': request.form['birth'],
            'idClass': request.form['classe']
        }

        requests.put(f'http://127.0.0.1:5000/students/{id}', json=data)
        return redirect(url_for('student'))
    # Delete   
    @app.route('/delStudent/<int:id>')
    def dstudent(id):
        api_url = f'http://1227.0.0.1:5000/students/{id}'

        response = requests.delete(api_url)

        return redirect(url_for('student'))

    # ROTAS PARA TURMA
    # Get
    @app.route('/Class')
    def cclass():
        with urllib.request.urlopen('http://127.0.0.1:5000/classes') as resp:
            classes = json.loads(resp.read().decode())
        return render_template('Class.html',classes=classes)
    # Create
    @app.route('/cadClass', methods=['GET', 'POST'])
    def cadclass():
        teacher_id = session.get('teacher_id')

        if request.method == 'POST':
            schoolYear = request.form.get('yearRegist')
            idYearSerie = request.form.get('name')
            idComponent = request.form.get('component')

            class_data = json.dumps({
                'schoolYear': int(schoolYear),
                'idYearSerie': int(idYearSerie),
                'idComponent': int(idComponent),
                'idTeacher': teacher_id
            })

            print(class_data)

            req = urllib.request.Request(
                url='http://127.0.0.1:5000/classes',
                data=class_data.encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST'
            )

            try:
                with urllib.request.urlopen(req) as resp:
                    if resp.status == 201:
                        return redirect(url_for('cclass'))
            except Exception as e:
                print('Erro ao cadastrar a turma:', e)

        with urllib.request.urlopen('http://127.0.0.1:5000/yearsSeries') as resp:
            yearsSeries = json.loads(resp.read().decode())

        with urllib.request.urlopen('http://127.0.0.1:5000/components') as resp:
            components = json.loads(resp.read().decode())
        return render_template('cadClass.html',yearsSeries=yearsSeries,components=components)
    # Get - ID
    @app.route('/editClass/<int:id>',methods=['GET','POST'])
    def editClass(id):
        with urllib.request.urlopen(f'http://127.0.0.1:5000/classes/{id}') as resp:
            classS = json.loads(resp.read().decode())
        with urllib.request.urlopen('http://127.0.0.1:5000/yearsSeries') as resp:
            yearsSeries = json.loads(resp.read().decode())
        with urllib.request.urlopen('http://127.0.0.1:5000/components') as resp:
            components = json.loads(resp.read().decode())
        return render_template('editClass.html',yearsSeries=yearsSeries,components=components,classS=classS)
    # Update
    @app.route('/updateClass/<int:id>', methods=['POST'])
    def updateclass(id):
        data = {
            'schoolYear': request.form['yearRegist'],
            'idYearSerie': request.form['name'],
            'idComponent': request.form['component'],
            'idTeacher': session['teacher_id']
        }

        requests.put(f'http://127.0.0.1:5000/classes/{id}', json=data)

        return redirect(url_for('cclass'))
    # Delete   
    @app.route('/delClass/<int:id>')
    def dclass(id):
        api_url = f'http://localhost:5000/classes/{id}'

        response = requests.delete(api_url)

        return redirect(url_for('cclass'))


    # Rotas para Questões
    # Get
    @app.route('/Quest')
    def quest():
        with urllib.request.urlopen('http://127.0.0.1:5000/questions') as resp:
            questions = json.loads(resp.read().decode())
        return render_template('Quest.html',questions=questions)
    # Create
    @app.route('/cadQuest', methods=['GET','POST'])
    def cadquest():
        if request.method == 'POST':
            qtype = request.form.get('questionType')
            region = request.form.get('region')
            theme = request.form.get('theme')
            question = request.form.get('question')
            awnser1 = request.form.get('response1')
            awnser2 = request.form.get('response2')
            awnser3 = request.form.get('response3')
            awnser4 = request.form.get('response4')
            img1 = request.form.get('picture1')
            img2 = request.form.get('picture2')
            img3 = request.form.get('picture3')
            img4 = request.form.get('picture4')
            validation1 = request.form.get('validation1')
            validation2 = request.form.get('validation2')
            validation3 = request.form.get('validation3')
            validation4 = request.form.get('validation4')

            quest_data = json.dumps({
                'idQuestionType': int(qtype),
                'idRegion': int(region),
                'idTheme': int(theme),
                'question': question,
                'response1': awnser1,
                'response2': awnser2,
                'response3': awnser3,
                'response4': awnser4,
                'picture1' : img1,
                'picture2' : img2,
                'picture3' : img3,
                'picture4' : img4,
                'idValidation1' : int(validation1),
                'idValidation2' : int(validation2),
                'idValidation3' : int(validation3),
                'idValidation4' : int(validation4)
            })

            req = urllib.request.Request(
                url='http://127.0.0.1:5000/questions',
                data=quest_data.encode('utf-8'),
                headers={'Content-Type':'application/json'},
                method='POST'
            )

            try:
                with urllib.request.urlopen(req) as resp:
                    if resp.status == 201:
                        return redirect(url_for('quest'))
            except Exception as e:
                print('Erro ao cadastrar a Questão:', e)

        with urllib.request.urlopen('http://127.0.0.1:5000/themes') as resp:
            themes = json.loads(resp.read().decode())
        with urllib.request.urlopen('http://127.0.0.1:5000/questionstypes') as resp:
            questTypes = json.loads(resp.read().decode())
        with urllib.request.urlopen('http://127.0.0.1:5000/regions') as resp:
            regions = json.loads(resp.read().decode())
        with urllib.request.urlopen('http://127.0.0.1:5000/validations') as resp:
            validations = json.loads(resp.read().decode())
        return render_template('cadQuest.html',themes=themes,questTypes=questTypes,regions=regions,validations=validations)
    # Get - ID
    @app.route('/editQuest/<int:id>')
    def editQuest(id):
        with urllib.request.urlopen(f'http://127.0.0.1:5000/questions/{id}') as resp:
            question = json.loads(resp.read().decode())
        with urllib.request.urlopen('http://127.0.0.1:5000/themes') as resp:
            themes = json.loads(resp.read().decode())
        with urllib.request.urlopen('http://127.0.0.1:5000/questionstypes') as resp:
            questTypes = json.loads(resp.read().decode())
        with urllib.request.urlopen('http://127.0.0.1:5000/regions') as resp:
            regions = json.loads(resp.read().decode())
        with urllib.request.urlopen('http://127.0.0.1:5000/validations') as resp:
            validations = json.loads(resp.read().decode())
        return render_template('editQuest.html',themes=themes,questTypes=questTypes,regions=regions,validations=validations,question=question)
    # Update
    @app.route('/updateQuestion/<int:id>', methods=['POST'])
    def updatequestion(id):
        data={
            'idQuestionType': request.form.get('questionType',type=int),
            'idRegion': request.form.get('region',type=int),
            'idTheme': request.form.get('theme',type=int),
            'question': request.form.get('question'),
            'response1': request.form.get('response1'),
            'response2': request.form.get('response2'),
            'response3': request.form.get('response3'),
            'response4': request.form.get('response4'),
            'picture1' : request.form.get('picture1'),
            'picture2' : request.form.get('picture2'),
            'picture3' : request.form.get('picture3'),
            'picture4' : request.form.get('picture4'),
            'idValidation1' : request.form.get('validation1',type=int),
            'idValidation2' : request.form.get('validation2',type=int),
            'idValidation3' : request.form.get('validation3',type=int),
            'idValidation4' : request.form.get('validation4',type=int)
        }

        requests.put(f'http://127.0.0.1:5000/questions/{id}', json=data)

        return redirect(url_for('quest'))
    # Delete   
    @app.route('/delQuest/<int:id>')
    def dquest(id):
        api_url = f'http://127.0.0.1:5000/questions/{id}'

        response = requests.delete(api_url)

        return redirect(url_for('quest'))


    # Rotas para QuestionsSkill
    # Get
    @app.route('/questionSkill')
    def qskill():
        with urllib.request.urlopen('http://127.0.0.1:5000/questionsSkills') as resp:
            qskills = json.loads(resp.read().decode())
        return render_template('questSkill.html',qskills=qskills)
    # Create
    @app.route('/cadQskill', methods=['GET','POST'])
    def cadQskill():
        if request.method == 'POST':
            idQuest = request.form.get('question')
            idSkill = request.form.get('skill')
            yearSerie = request.form.get('yearSerie')
            difficulty = request.form.get('difficulty')
            available = 'available' in request.form

            qSkilldata = json.dumps({
                'idQuestion': int(idQuest),
                'idSkill': int(idSkill),
                'idYearSerie': int(yearSerie),
                'difficulty': int(difficulty),
                'available': available
            })
            
            req = urllib.request.Request(
                url='http://127.0.0.1:5000/questionsSkills',
                data=qSkilldata.encode('utf-8'),
                headers={'Content-Type':'application/json'},
                method='POST'
            )

            try:
                with urllib.request.urlopen(req) as resp:
                    if resp.status == 201:
                        return redirect(url_for('qskill'))
            except Exception as e:
                print('Erro ao Cadastrar Habilidade Questão:', e)

        with urllib.request.urlopen('http://127.0.0.1:5000//questions') as resp:
            questions = json.loads(resp.read().decode())
        with urllib.request.urlopen('http://127.0.0.1:5000/skills') as resp:
            skills = json.loads(resp.read().decode())
        with urllib.request.urlopen('http://127.0.0.1:5000/yearsSeries') as resp:
            yearsSeries = json.loads(resp.read().decode())
        return render_template('cadQuestSkill.html',questions=questions,skills=skills,yearsSeries=yearsSeries)
    # Get - ID
    @app.route('/editQskill/<int:id>')
    def editQskill(id):
        with urllib.request.urlopen(f'http://127.0.0.1:5000/questionsSkills/{id}') as resp:
            qskill = json.loads(resp.read().decode())
        with urllib.request.urlopen('http://127.0.0.1:5000//questions') as resp:
            questions = json.loads(resp.read().decode())
        with urllib.request.urlopen('http://127.0.0.1:5000/skills') as resp:
            skills = json.loads(resp.read().decode())
        with urllib.request.urlopen('http://127.0.0.1:5000/yearsSeries') as resp:
            yearsSeries = json.loads(resp.read().decode())
        return render_template('editQuestSkill.html',qskill=qskill,questions=questions,skills=skills,yearsSeries=yearsSeries)
    
    # Update
    @app.route('/updateqSkill/<int:id>', methods=['POST'])
    def updateQskill(id):
        data = {
            'idQuestion': request.form.get('question',type=int),
            'idSkill': request.form.get('skill',type=int),
            'idYearSerie': request.form.get('yearSerie',type=int),
            'difficulty': request.form.get('difficulty',type=int),
            'available': 'available' in request.form
        }
        requests.put(f'http://127.0.0.1:5000/questionsSkills/{id}', json=data)
        return redirect(url_for('qskill'))
    # Delete
    @app.route('/delqSkill/<int:id>')
    def dQskill(id):
        api_url=f'http://127.0.0.1:5000/questionsSkills/{id}'

        response = requests.delete(api_url)

        return redirect(url_for('qskill'))



    # Rotas para login/logout
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if session.get('teacher_id'):
            return redirect(url_for('graphics'))
        if request.method == 'POST':
            data = {
                'eMail': request.form.get('email'),
                'password': request.form.get('senha')
            }
            try:
                resp = requests.post(
                    'http://127.0.0.1:5000/teachers/login',
                    json=data
                )
            except requests.exceptions.RequestException as e:
                return render_template('login.html')
            if resp.status_code == 200:
                user = resp.json()
                session['teacher_id'] = user['id']
                session['teacher_name'] = user['name']
                return redirect(url_for('graphics'))
            elif resp.status_code == 401:
                return render_template('login.html')
            else:
                return render_template('login.html')
        return render_template('login.html')

    @app.route('/logout', methods=['GET','POST'])
    def logout():
        # Desrtroi a sessão do usuário
        session.clear()
        return redirect(url_for('home'))