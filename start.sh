#!/bin/bash

echo "========================================"
echo "   Sistema de Webhook Kolmeya"
echo "========================================"
echo

echo "[1/4] Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado! Instale o Python primeiro."
    exit 1
fi
echo "✅ Python encontrado!"

echo
echo "[2/4] Instalando dependências..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências!"
    exit 1
fi
echo "✅ Dependências instaladas!"

echo
echo "[3/4] Verificando configuração..."
if [ ! -f ".env" ]; then
    echo "⚠️  Arquivo .env não encontrado!"
    echo "📝 Copiando arquivo de exemplo..."
    cp config.env.example .env
    echo "✅ Arquivo .env criado!"
    echo "📋 Edite o arquivo .env com suas configurações do Kolmeya"
else
    echo "✅ Arquivo .env encontrado!"
fi

echo
echo "[4/4] Iniciando servidor..."
echo "🌐 Servidor será iniciado em: http://localhost:5000"
echo "📊 Dashboard: http://localhost:5000/dashboard"
echo
echo "Pressione Ctrl+C para parar o servidor"
echo

python3 webkolm.py 