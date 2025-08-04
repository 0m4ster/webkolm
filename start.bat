@echo off
echo ========================================
echo    Sistema de Webhook Kolmeya
echo ========================================
echo.

echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! Instale o Python primeiro.
    pause
    exit /b 1
)
echo ✅ Python encontrado!

echo.
echo [2/4] Instalando dependências...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Erro ao instalar dependências!
    pause
    exit /b 1
)
echo ✅ Dependências instaladas!

echo.
echo [3/4] Verificando configuração...
if not exist ".env" (
    echo ⚠️  Arquivo .env não encontrado!
    echo 📝 Copiando arquivo de exemplo...
    copy config.env.example .env
    echo ✅ Arquivo .env criado!
    echo 📋 Edite o arquivo .env com suas configurações do Kolmeya
) else (
    echo ✅ Arquivo .env encontrado!
)

echo.
echo [4/4] Iniciando servidor...
echo 🌐 Servidor será iniciado em: http://localhost:5000
echo 📊 Dashboard: http://localhost:5000/dashboard
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

python webkolm.py

pause 