@echo off
echo ========================================
echo    Preparando Deploy no Render
echo ========================================
echo.

echo [1/4] Verificando arquivos necessários...
if not exist "webkolm.py" (
    echo ❌ webkolm.py não encontrado!
    pause
    exit /b 1
)
if not exist "requirements.txt" (
    echo ❌ requirements.txt não encontrado!
    pause
    exit /b 1
)
if not exist "render.yaml" (
    echo ❌ render.yaml não encontrado!
    pause
    exit /b 1
)
if not exist "runtime.txt" (
    echo ❌ runtime.txt não encontrado!
    pause
    exit /b 1
)
echo ✅ Todos os arquivos necessários encontrados!

echo.
echo [2/4] Verificando .gitignore...
if not exist ".gitignore" (
    echo ⚠️  .gitignore não encontrado! Criando...
    echo # Arquivos de ambiente > .gitignore
    echo .env >> .gitignore
    echo *.db >> .gitignore
    echo __pycache__/ >> .gitignore
    echo ✅ .gitignore criado!
) else (
    echo ✅ .gitignore encontrado!
)

echo.
echo [3/4] Preparando para GitHub...
if not exist ".git" (
    echo 📝 Inicializando repositório Git...
    git init
    git add .
    git commit -m "Sistema de Webhook Kolmeya - Deploy inicial"
    echo ✅ Repositório Git inicializado!
) else (
    echo ✅ Repositório Git já existe!
)

echo.
echo [4/4] Instruções para Deploy...
echo.
echo 🚀 PRÓXIMOS PASSOS:
echo.
echo 1. Crie um repositório no GitHub:
echo    - Acesse: https://github.com/new
echo    - Nome: kolmeya-webhook
echo    - Público ou Privado
echo.
echo 2. Conecte ao GitHub:
echo    git remote add origin https://github.com/SEU-USUARIO/kolmeya-webhook.git
echo    git push -u origin main
echo.
echo 3. Deploy no Render:
echo    - Acesse: https://render.com
echo    - New + > Web Service
echo    - Conecte ao repositório
echo    - Configure variáveis de ambiente
echo.
echo 4. Variáveis de ambiente no Render:
echo    KOLMEYA_API_KEY=sua_api_key_real
echo    WEBHOOK_BASE_URL=https://seu-app.onrender.com
echo    PORT=10000
echo    DEBUG=False
echo.
echo 📋 Documentação completa: DEPLOY_RENDER.md
echo.

pause 