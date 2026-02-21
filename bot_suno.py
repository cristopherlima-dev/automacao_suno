import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

load_dotenv()

EMAIL = os.getenv("SUNO_EMAIL")
SENHA = os.getenv("SUNO_SENHA")

def iniciar_robo():
    if not EMAIL or not SENHA:
        print("❌ ERRO: E-mail ou senha não encontrados no arquivo .env")
        return

    print("Iniciando o navegador...")
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)
    
    try:
        print("Acessando investidor.suno.com.br...")
        navegador.get("https://investidor.suno.com.br/")
        
        wait = WebDriverWait(navegador, 15)
        
        print("Aguardando redirecionamento para a tela de login...")
        wait.until(EC.url_contains("login.suno.com.br"))
        
        print("Preenchendo credenciais...")
        
        xpath_email = '//*[@id="user_email_wrapper"]//input'
        campo_email = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_email)))
        campo_email.send_keys(EMAIL)
        
        xpath_senha = '//*[@id="user_password"]'
        campo_senha = navegador.find_element(By.XPATH, xpath_senha)
        campo_senha.send_keys(SENHA)
        
        print("Clicando em entrar...")
        xpath_botao = '//*[@id="login_button"]'
        botao_entrar = navegador.find_element(By.XPATH, xpath_botao)
        
        # SOLUÇÃO: Clique via JavaScript para ignorar o banner de cookies
        navegador.execute_script("arguments[0].click();", botao_entrar)
        
        print("Aguardando o painel principal carregar...")
        wait.until(EC.url_contains("investidor.suno.com.br"))
        print("✅ Login realizado com sucesso!")
        
        time.sleep(5)
        
    except TimeoutException:
        print("\n❌ ERRO DE RASTREAMENTO: O robô não encontrou os elementos na tela.")
        
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        
    finally:
        print("Fechando o navegador...")
        navegador.quit()

if __name__ == "__main__":
    iniciar_robo()