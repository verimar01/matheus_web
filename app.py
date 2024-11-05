from flask import Flask, request, render_template, redirect, url_for, send_from_directory, flash
import json
import os

app = Flask(__name__)
app.secret_key = "chave_secreta_para_flash"

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def salvar_dados(data):
    with open("inscricoes.json", "a") as f:
        json.dump(data, f)
        f.write("\n")

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Página do formulário de inscrição (Discente)
@app.route('/inscricao')
def formulario():
    return render_template('formulario.html')

# Rota para processar a inscrição
@app.route('/inscricao', methods=['POST'])
def inscricao():
    nome = request.form['nome']
    data_nascimento = request.form['data_nascimento']
    responsavel = request.form['responsavel']
    email = request.form['email']

    rg_aluno = request.files['rg_aluno']
    rg_pais = request.files['rg_pais']
    historico = request.files['historico']

    rg_aluno_path = os.path.join(app.config['UPLOAD_FOLDER'], rg_aluno.filename)
    rg_aluno.save(rg_aluno_path)
    rg_pais_path = os.path.join(app.config['UPLOAD_FOLDER'], rg_pais.filename)
    rg_pais.save(rg_pais_path)
    historico_path = os.path.join(app.config['UPLOAD_FOLDER'], historico.filename)
    historico.save(historico_path)

    inscricao_data = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'responsavel': responsavel,
        'email': email,
        'rg_aluno': rg_aluno.filename,
        'rg_pais': rg_pais.filename,
        'historico': historico.filename
    }
    salvar_dados(inscricao_data)
    return redirect(url_for('confirmacao'))

# Página de confirmação de inscrição
@app.route('/confirmacao')
def confirmacao():
    return render_template('confirmacao.html')

# Página de login (Docente)
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'fernando' and password == 'Teste123':
            return redirect(url_for('visualizar_inscricoes'))
        else:
            error = 'Usuário ou senha incorretos. Tente novamente.'
    return render_template('login.html', error=error)

# Página para visualizar as inscrições
@app.route('/visualizar')
def visualizar_inscricoes():
    try:
        with open("inscricoes.json", "r") as f:
            inscricoes = [json.loads(line) for line in f]
    except FileNotFoundError:
        inscricoes = []
    
    return render_template('visualizar.html', inscricoes=inscricoes)

# Rota para servir os arquivos enviados
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
