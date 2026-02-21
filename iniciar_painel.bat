@echo off
title Painel de Aportes Suno
echo =========================================
echo Iniciando o Servidor do Painel Suno...
echo =========================================

:: Entra na pasta atual do arquivo
cd /d "%~dp0"

:: Ativa o ambiente virtual
call venv\Scripts\activate

:: Pede para o Windows abrir o seu navegador padrão neste endereço
start http://127.0.0.1:5000

:: Inicia o servidor Python
python app.py

pause