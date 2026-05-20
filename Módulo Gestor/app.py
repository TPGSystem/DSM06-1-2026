from flask import Flask,render_template, jsonify
from Controllers import routes
app = Flask(__name__, template_folder='Views')

routes.init_app(app)

alunos = [
    {"nome": "Carlos", "nota": 100, "turma": "Turma A", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Renato", "nota": 80, "turma": "Turma A", "questoes": [20, 0, 20, 20, 20]},
    {"nome": "Pedro", "nota": 60, "turma": "Turma A", "questoes": [20, 20, 0, 0, 20]},
    {"nome": "Lissia", "nota": 60, "turma": "Turma A", "questoes": [20, 0, 20, 0, 20]},
    {"nome": "Liamara", "nota": 40, "turma": "Turma A", "questoes": [0, 0, 0, 20, 20]},
    {"nome": "Leandro", "nota": 100, "turma": "Turma A", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "João", "nota": 100, "turma": "Turma A", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Julia", "nota": 80, "turma": "Turma A", "questoes": [0, 20, 20, 20, 20]},
    {"nome": "Carol", "nota": 80, "turma": "Turma A", "questoes": [20, 0, 20, 20, 20]},
    {"nome": "Ana", "nota": 100, "turma": "Turma A", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Miguel", "nota": 80, "turma": "Turma A", "questoes": [0, 20, 20, 20, 20]},
    {"nome": "Samuel", "nota": 100, "turma": "Turma A", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Luiz", "nota": 100, "turma": "Turma A", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Sergio", "nota": 100, "turma": "Turma A", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Cleber", "nota": 100, "turma": "Turma A", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Cristoffer", "nota": 0, "turma": "Turma A", "questoes": [0, 0, 0, 0, 0]},
    {"nome": "Vinicius", "nota": 100, "turma": "Turma A", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Vanessa", "nota": 80, "turma": "Turma A", "questoes": [20, 20, 0, 20, 20]},
    {"nome": "Sheila", "nota": 100, "turma": "Turma A", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Marina", "nota": 100, "turma": "Turma A", "questoes": [20, 20, 20, 20, 20]},

    {"nome": "Victor", "nota": 40, "turma": "Turma B", "questoes": [0, 0, 20, 20, 0]},
    {"nome": "Bruno", "nota": 100, "turma": "Turma B", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Gilberto", "nota": 80, "turma": "Turma B", "questoes": [0, 20, 20, 20, 20]},
    {"nome": "Rafael", "nota": 100, "turma": "Turma B", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Maria", "nota": 100, "turma": "Turma B", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Fernando", "nota": 100, "turma": "Turma B", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Adriana", "nota": 100, "turma": "Turma B", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Rebeca", "nota": 80, "turma": "Turma B", "questoes": [0, 20, 20, 20, 20]},
    {"nome": "José", "nota": 80, "turma": "Turma B", "questoes": [0, 20, 20, 20, 20]},
    {"nome": "Jonathan", "nota": 100, "turma": "Turma B", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Luiza", "nota": 40, "turma": "Turma B", "questoes": [20, 20, 0, 0, 0]},
    {"nome": "Silvana", "nota": 80, "turma": "Turma B", "questoes": [20, 20, 0, 20, 20]},
    {"nome": "Vitoria", "nota": 60, "turma": "Turma B", "questoes": [20, 20, 0, 20, 0]},
    {"nome": "Ronaldo", "nota": 20, "turma": "Turma B", "questoes": [0, 0, 0, 20, 0]},
    {"nome": "Natalia", "nota": 100, "turma": "Turma B", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Rafaela", "nota": 100, "turma": "Turma B", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Kauã", "nota": 100, "turma": "Turma B", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Murilo", "nota": 80, "turma": "Turma B", "questoes": [0, 20, 20, 20, 20]},
    {"nome": "Davi", "nota": 0, "turma": "Turma B", "questoes": [0, 0, 0, 0, 0]},
    {"nome": "Elis", "nota": 80, "turma": "Turma B", "questoes": [20, 20, 0, 20, 20]},

    {"nome": "Amanda", "nota": 100, "turma": "Turma C", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Alana", "nota": 80, "turma": "Turma C", "questoes": [20, 20, 20, 20, 0]},
    {"nome": "Douglas", "nota": 100, "turma": "Turma C", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Roberto", "nota": 100, "turma": "Turma C", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Elias", "nota": 100, "turma": "Turma C", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Helena", "nota": 80, "turma": "Turma C", "questoes": [20, 20, 20, 20, 0]},
    {"nome": "Laura", "nota": 60, "turma": "Turma C", "questoes": [0, 20, 0, 20, 20]},
    {"nome": "Paulo", "nota": 80, "turma": "Turma C", "questoes": [20, 20, 20, 20, 0]},
    {"nome": "Henrique", "nota": 100, "turma": "Turma C", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Isabela", "nota": 80, "turma": "Turma C", "questoes": [20, 20, 20, 20, 0]},
    {"nome": "Ivan", "nota": 100, "turma": "Turma C", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Eduardo", "nota": 80, "turma": "Turma C", "questoes": [20, 20, 0, 20, 20]},
    {"nome": "Junior", "nota": 0, "turma": "Turma C", "questoes": [0, 0, 0, 0, 0]},
    {"nome": "Larissa", "nota": 100, "turma": "Turma C", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Manuela", "nota": 100, "turma": "Turma C", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Virginia", "nota": 80, "turma": "Turma C", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Beatriz", "nota": 100, "turma": "Turma C", "questoes": [20, 20, 20, 20, 20]},
    {"nome": "Calebe", "nota": 80, "turma": "Turma C", "questoes": [0, 20, 20, 20, 20]},
    {"nome": "Vagner", "nota": 80, "turma": "Turma C", "questoes": [0, 20, 20, 20, 20]},
    {"nome": "Walter", "nota": 40, "turma": "Turma C", "questoes": [0, 20, 20, 0, 0]},
]

META = 70

@app.route("/dados")
def dados():
    return jsonify(alunos)

@app.route("/dados/<turma>")
def dados_por_turma(turma):
    turma = turma.title()
    filtrados = [a for a in alunos if a["turma"] == turma]
    return jsonify(filtrados)

@app.route("/medias")
def medias():
    turmas = {}
    for aluno in alunos:
        turma = aluno["turma"]
        if turma not in turmas:
            turmas[turma] = {"soma": 0, "qtd": 0}
        turmas[turma]["soma"] += aluno["nota"]
        turmas[turma]["qtd"] += 1

    medias_turmas = [
        {"turma": t, "media": turmas[t]["soma"] / turmas[t]["qtd"]}
        for t in turmas
    ]
    return jsonify({"turmas": medias_turmas, "meta": META})

app.config['SECRET_KEY'] = 'tpgsystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600

if __name__ == '__main__':
    app.run(host='localhost', port=4000, debug=True)