import os
import time
import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from sqlalchemy import create_engine # <-- NOVO IMPORT PARA O BANCO DE DADOS
from selenium.webdriver.chrome.options import Options

load_dotenv()

EMAIL = os.getenv("SUNO_EMAIL")
SENHA = os.getenv("SUNO_SENHA")

# MAPA EXATO DE CADA CARTEIRA
CARTEIRAS = [
    {
        "nome": "Valor",
        "url": "https://investidor.suno.com.br/carteiras/valor",
        "ignorar_indices": [1],
        "cabecalhos": ["Rank", "Ticker", "Entrada", "Preço Atual", "Preço Teto", "Alocação", "Rentabilidade", "Viés"]
    },
    {
        "nome": "Dividendos",
        "url": "https://investidor.suno.com.br/carteiras/dividendos",
        "ignorar_indices": [1],
        "cabecalhos": ["Rank", "Ticker", "DY Esperado", "Entrada", "Preço Atual", "Preço Teto", "Alocação", "Rentabilidade", "Viés"]
    },
    {
        "nome": "FIIs",
        "url": "https://investidor.suno.com.br/carteiras/fiis",
        "ignorar_indices": [9], 
        "cabecalhos": ["Rank", "Ticker", "Setor", "DY Esperado", "Entrada", "Preço Atual", "Preço Teto", "Alocação", "Rentabilidade", "Viés"]
    },
    {
        "nome": "Start",
        "url": "https://investidor.suno.com.br/carteiras/suno-start",
        "ignorar_indices": [1],
        "cabecalhos": ["Rank", "Ticker", "Entrada", "Preço Atual", "Preço Teto", "Alocação", "Rentabilidade", "Viés"]
    }
]

def iniciar_robo():
    if not EMAIL or not SENHA:
        print("❌ ERRO: E-mail ou senha não encontrados no arquivo .env")
        return

    print("Iniciando o navegador...")
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)
    
    # A MÁGICA AQUI: Minimiza a janela logo após abrir
    navegador.minimize_window()
    
    try:
        # --- ETAPA 1: LOGIN ---
        navegador.get("https://investidor.suno.com.br/")
        wait = WebDriverWait(navegador, 15)
        wait.until(EC.url_contains("login.suno.com.br"))
        
        xpath_email = '//*[@id="user_email_wrapper"]//input'
        campo_email = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_email)))
        campo_email.send_keys(EMAIL)
        
        xpath_senha = '//*[@id="user_password"]'
        campo_senha = navegador.find_element(By.XPATH, xpath_senha)
        campo_senha.send_keys(SENHA)
        
        botao_entrar = navegador.find_element(By.XPATH, '//*[@id="login_button"]')
        navegador.execute_script("arguments[0].click();", botao_entrar)
        
        wait.until(EC.url_contains("investidor.suno.com.br"))
        print("✅ Login realizado com sucesso!")
        
        # --- ETAPA 2: EXTRAÇÃO DIRETO PARA O BANCO DE DADOS ---
        
        # Cria a conexão com o banco local SQLite
        engine = create_engine('sqlite:///banco_suno.db')
        
        for carteira in CARTEIRAS:
            print(f"\nExtraindo dados da carteira: {carteira['nome']}...")
            navegador.get(carteira['url'])
            
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr")))
                time.sleep(3) 
            except TimeoutException:
                print(f"⚠️ Tabela não encontrada para {carteira['nome']}. Pulando...")
                continue
            
            todas_as_tabelas = navegador.find_elements(By.TAG_NAME, "table")
            dados_extraidos = []
            
            for tabela in todas_as_tabelas:
                linhas = tabela.find_elements(By.CSS_SELECTOR, "tbody tr")
                
                if len(linhas) > 0:
                    colunas_teste = linhas[0].find_elements(By.TAG_NAME, "td")
                    qtd_esperada = len(carteira["cabecalhos"]) + len(carteira["ignorar_indices"])
                    
                    if len(colunas_teste) >= qtd_esperada - 1:
                        print(f"✅ Tabela principal de {carteira['nome']} identificada!")
                        
                        for linha in linhas:
                            colunas = linha.find_elements(By.TAG_NAME, "td")
                            
                            if len(colunas) >= 2:
                                linha_limpa = []
                                for idx, coluna in enumerate(colunas):
                                    if idx in carteira["ignorar_indices"]:
                                        continue
                                    texto_bruto = coluna.text.strip()
                                    texto_principal = texto_bruto.split('\n')[0] 
                                    linha_limpa.append(texto_principal)
                                    
                                linha_limpa = linha_limpa[:len(carteira["cabecalhos"])]
                                while len(linha_limpa) < len(carteira["cabecalhos"]):
                                    linha_limpa.append("")
                                    
                                dados_extraidos.append(linha_limpa)
                        break 
                    
            if len(dados_extraidos) > 0:
                df = pd.DataFrame(dados_extraidos, columns=carteira["cabecalhos"])
                
                # MÁGICA AQUI: Salva direto no Banco de Dados!
                # if_exists='replace' garante que ele atualiza a tabela toda vez que roda
                df.to_sql(carteira['nome'], con=engine, if_exists='replace', index=False)
                
                print(f"✅ Dados de {carteira['nome']} salvos no Banco de Dados!")
            else:
                print(f"❌ Não foi possível extrair {carteira['nome']}.")

        print(f"\n🎉 EXCELENTE! Banco de dados 'banco_suno.db' atualizado com sucesso!")

    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        
    finally:
        print("Fechando o navegador...")
        navegador.quit()

if __name__ == "__main__":
    iniciar_robo()