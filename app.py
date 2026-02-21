from flask import Flask, render_template, jsonify, request
import sqlite3
import pandas as pd
from bot_suno import iniciar_robo 

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('banco_suno.db')
    conn.row_factory = sqlite3.Row
    
    # MÁGICA 1: Cria as tabelas para salvar o seu perfil se elas não existirem
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Meus_Ativos (
            ticker TEXT PRIMARY KEY,
            tenho INTEGER
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Configuracoes (
            chave TEXT PRIMARY KEY,
            valor TEXT
        )
    ''')
    conn.commit()
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    carteiras = {}
    tabelas = ['Valor', 'Dividendos', 'FIIs', 'Start']
    
    for tabela in tabelas:
        try:
            df = pd.read_sql_query(f"SELECT * FROM {tabela}", conn)
            carteiras[tabela] = df.to_dict(orient='records')
        except Exception:
            carteiras[tabela] = [] 
            
    # MÁGICA 2: Busca no banco quais ativos você já marcou que tem
    cur = conn.execute('SELECT ticker FROM Meus_Ativos WHERE tenho = 1')
    meus_ativos = [row['ticker'] for row in cur.fetchall()]
    
    # MÁGICA 3: Busca o seu último valor de aporte digitado
    cur = conn.execute("SELECT valor FROM Configuracoes WHERE chave = 'ultimo_aporte'")
    linha_aporte = cur.fetchone()
    ultimo_aporte = linha_aporte['valor'] if linha_aporte else ""
            
    conn.close()
    
    # Envia tudo (dados da Suno + seu perfil) para a tela
    return render_template('index.html', carteiras=carteiras, meus_ativos=meus_ativos, ultimo_aporte=ultimo_aporte)

@app.route('/atualizar', methods=['POST'])
def atualizar_dados():
    try:
        print("🤖 Botão clicado! Iniciando a extração...")
        iniciar_robo() 
        return jsonify({"status": "sucesso", "mensagem": "Base atualizada com sucesso!"})
    except Exception as e:
        print(f"Erro ao atualizar: {e}")
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

# MÁGICA 4: O "Ouvido" do servidor. Ele escuta quando você digita ou clica na tela e salva.
@app.route('/salvar_perfil', methods=['POST'])
def salvar_perfil():
    dados = request.json
    conn = get_db_connection()
    
    try:
        if dados['tipo'] == 'aporte':
            # Salva ou atualiza o valor do aporte
            conn.execute('''
                INSERT INTO Configuracoes (chave, valor) 
                VALUES ('ultimo_aporte', ?) 
                ON CONFLICT(chave) DO UPDATE SET valor = excluded.valor
            ''', (str(dados['valor']),))
        
        elif dados['tipo'] == 'ativo':
            # Salva 1 (Sim) ou 0 (Não) para a ação clicada
            estado = 1 if dados['tenho'] else 0
            conn.execute('''
                INSERT INTO Meus_Ativos (ticker, tenho) 
                VALUES (?, ?) 
                ON CONFLICT(ticker) DO UPDATE SET tenho = excluded.tenho
            ''', (dados['ticker'], estado))
            
        conn.commit()
        return jsonify({"status": "sucesso"})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    print("🚀 Servidor rodando! Acesse http://127.0.0.1:5000 no seu navegador.")
    app.run(debug=True)