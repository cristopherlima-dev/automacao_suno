# 💼 Painel de Aportes Suno

Um Web App Full-Stack local construído em Python para automatizar a extração e o gerenciamento das carteiras recomendadas da Suno Research. O sistema coleta as cotações atualizadas, consolida em um banco de dados local e fornece uma interface web interativa para calcular a distribuição de aportes mensais.

## ✨ Funcionalidades

- **Automação (Web Scraping):** Um robô invisível em Selenium faz login no site da Suno e extrai as tabelas das carteiras (Valor, Dividendos, FIIs e Start).
- **Banco de Dados Local:** Armazenamento seguro dos dados em SQLite, sem dependência de planilhas de terceiros.
- **Interface Web Moderna:** Dashboard responsivo criado com Flask, Bootstrap 5 e DataTables.
- **Calculadora de Aportes:** Insira o valor do seu aporte mensal e o painel calcula automaticamente a Quantidade Possível de compra e a Sobra (troco) para cada ativo.
- **Persistência de Perfil:** O sistema lembra quais ativos você já tem na carteira (checkbox) e o seu último valor de aporte.
- **Filtros e Buscas:** Ordenação dinâmica por qualquer coluna (Rank, Qtd. Possível, Viés, etc.) e barra de pesquisa em tempo real.
- **Atualização em Um Clique:** Botão na própria interface web para disparar o robô e buscar cotações atualizadas sem precisar abrir o terminal.

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3, Flask, SQLAlchemy.
- **Web Scraping & Dados:** Selenium, Pandas, BeautifulSoup4, HTML5lib.
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, jQuery DataTables.
- **Banco de Dados:** SQLite.

## ⚙️ Pré-requisitos

Antes de começar, você precisará ter instalado em sua máquina:

- [Python 3.x](https://www.python.org/downloads/)
- Google Chrome (O Webdriver é gerenciado automaticamente).
- Git

## 🚀 Como Instalar e Configurar

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/cristopherlima-dev/automacao_suno.git
   cd automacao_suno
   ```
2. **Crie e ative um Ambiente Virtual:**

   ```bash
   # Criar
   python -m venv venv

    # Ativar - No Windows:
    venv\Scripts\activate

    # Ativar - No Linux/Mac:
    source venv/bin/activate
   ```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Configure as suas credenciais:**
   Crie um arquivo chamado `.env` na raiz do projeto (este arquivo é ignorado pelo Git por segurança) e adicione seu login da Suno:

```text
SUNO_EMAIL=seu_email@exemplo.com
SUNO_SENHA=sua_senha_secreta
```

## 💻 Como Usar

A forma mais fácil de iniciar o painel no Windows é dando um duplo clique no arquivo:
`iniciar_painel.bat`

Ele irá abrir o terminal, ativar o ambiente, iniciar o servidor Flask e abrir a página automaticamente no seu navegador padrão (http://127.0.0.1:5000).

Para rodar manualmente via terminal:

```bash
python app.py
```

## 📂 Estrutura do Projeto

```text
automacao_suno/
├── app.py                 # Servidor Web (Flask) e rotas de salvamento
├── bot_suno.py            # Robô de extração (Selenium + Pandas)
├── iniciar_painel.bat     # Script de inicialização rápida (Windows)
├── requirements.txt       # Lista de bibliotecas do Python
├── .env                   # Suas variáveis de ambiente (Senhas)
├── .gitignore             # Arquivos ignorados pelo Git (ex: banco de dados)
├── banco_suno.db          # Banco de dados SQLite (Gerado automaticamente)
└── templates/
    └── index.html         # Interface Frontend (Dashboard)
```

## ⚠️ Aviso Legal

Este projeto foi criado para fins educacionais e de uso pessoal para organização financeira. As senhas ficam salvas exclusivamente na sua máquina local. O desenvolvedor deste código não tem relação com a Suno Research. Utilize com responsabilidade e proteja seu arquivo `.env`.
