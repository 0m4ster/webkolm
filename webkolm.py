#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Webhook para Kolmeya
Integração completa para disparo de SMS e rastreamento de cliques
"""

import os
import json
import sqlite3
import requests
from datetime import datetime
from flask import Flask, request, jsonify, redirect, render_template_string
from flask_cors import CORS
import uuid
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configurações do Kolmeya (substitua pelos seus dados reais)
KOLMEYA_API_KEY = os.getenv('KOLMEYA_API_KEY', 'sua_api_key_aqui')
KOLMEYA_API_URL = os.getenv('KOLMEYA_API_URL', 'https://api.kolmeya.com.br')
WEBHOOK_BASE_URL = os.getenv('WEBHOOK_BASE_URL', 'https://seudominio.com')

# Configuração para Render
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env se existir
load_dotenv()

# Inicialização do banco de dados
def init_database():
    """Inicializa o banco de dados SQLite"""
    conn = sqlite3.connect('kolmeya_webhook.db')
    cursor = conn.cursor()
    
    # Tabela para armazenar dados dos clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telefone TEXT NOT NULL,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL,
            link_id TEXT UNIQUE NOT NULL,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela para armazenar cliques
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cliques (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link_id TEXT NOT NULL,
            telefone TEXT,
            nome TEXT,
            cpf TEXT,
            ip_address TEXT,
            user_agent TEXT,
            data_clique TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (link_id) REFERENCES clientes (link_id)
        )
    ''')
    
    # Tabela para armazenar webhooks recebidos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS webhooks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evento TEXT NOT NULL,
            dados TEXT NOT NULL,
            data_recebimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Banco de dados inicializado com sucesso")

def gerar_link_rastreavel(link_id):
    """Gera um link rastreável único"""
    return f"{WEBHOOK_BASE_URL}/clique?id={link_id}"

def enviar_sms_kolmeya(telefone, mensagem):
    """
    Envia SMS via API do Kolmeya
    Retorna: (sucesso, resposta)
    """
    try:
        headers = {
            'Authorization': f'Bearer {KOLMEYA_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'telefone': telefone,
            'mensagem': mensagem
        }
        
        response = requests.post(
            f"{KOLMEYA_API_URL}/sms/enviar",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            logger.info(f"SMS enviado com sucesso para {telefone}")
            return True, response.json()
        else:
            logger.error(f"Erro ao enviar SMS: {response.status_code} - {response.text}")
            return False, response.text
            
    except Exception as e:
        logger.error(f"Exceção ao enviar SMS: {str(e)}")
        return False, str(e)

@app.route('/enviar-sms', methods=['POST'])
def enviar_sms():
    """
    Endpoint para enviar SMS com link rastreável
    """
    try:
        # Aceitar tanto JSON quanto form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        # Validação dos dados
        required_fields = ['telefone', 'nome', 'cpf', 'mensagem']
        for field in required_fields:
            if field not in data:
                return jsonify({'erro': f'Campo obrigatório não encontrado: {field}'}), 400
        
        # Gerar ID único para o link
        link_id = str(uuid.uuid4())
        
        # Salvar dados do cliente no banco
        conn = sqlite3.connect('kolmeya_webhook.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO clientes (telefone, nome, cpf, link_id)
            VALUES (?, ?, ?, ?)
        ''', (data['telefone'], data['nome'], data['cpf'], link_id))
        
        conn.commit()
        conn.close()
        
        # Gerar link rastreável
        link_rastreavel = gerar_link_rastreavel(link_id)
        
        # Adicionar link à mensagem
        mensagem_com_link = f"{data['mensagem']}\n\nAcesse: {link_rastreavel}"
        
        # Enviar SMS via Kolmeya
        sucesso, resposta = enviar_sms_kolmeya(data['telefone'], mensagem_com_link)
        
        if sucesso:
            return jsonify({
                'status': 'sucesso',
                'mensagem': 'SMS enviado com sucesso',
                'link_id': link_id,
                'link_rastreavel': link_rastreavel,
                'resposta_kolmeya': resposta
            })
        else:
            return jsonify({
                'status': 'erro',
                'mensagem': 'Erro ao enviar SMS',
                'erro': resposta
            }), 500
            
    except Exception as e:
        logger.error(f"Erro no endpoint enviar-sms: {str(e)}")
        return jsonify({'erro': str(e)}), 500

@app.route('/clique')
def rastrear_clique():
    """
    Endpoint para rastrear cliques nos links
    """
    try:
        link_id = request.args.get('id')
        if not link_id:
            return jsonify({'erro': 'ID do link não fornecido'}), 400
        
        # Buscar dados do cliente
        conn = sqlite3.connect('kolmeya_webhook.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT telefone, nome, cpf FROM clientes 
            WHERE link_id = ?
        ''', (link_id,))
        
        cliente = cursor.fetchone()
        
        if not cliente:
            return jsonify({'erro': 'Cliente não encontrado'}), 404
        
        telefone, nome, cpf = cliente
        
        # Registrar o clique
        cursor.execute('''
            INSERT INTO cliques (link_id, telefone, nome, cpf, ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            link_id, 
            telefone, 
            nome, 
            cpf,
            request.remote_addr,
            request.headers.get('User-Agent', '')
        ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Clique registrado - Cliente: {nome} ({cpf}) - Link ID: {link_id}")
        
        # Redirecionar para a página de destino (substitua pela sua URL)
        return redirect("https://sua-pagina-de-destino.com")
        
    except Exception as e:
        logger.error(f"Erro no endpoint clique: {str(e)}")
        return jsonify({'erro': str(e)}), 500

@app.route('/webhook-kolmeya', methods=['POST'])
def receber_webhook():
    """
    Endpoint para receber webhooks do Kolmeya
    """
    try:
        # Aceitar tanto JSON quanto form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        # Salvar webhook no banco
        conn = sqlite3.connect('kolmeya_webhook.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO webhooks (evento, dados)
            VALUES (?, ?)
        ''', ('webhook_recebido', json.dumps(data)))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Webhook recebido: {json.dumps(data, indent=2)}")
        
        # Processar diferentes tipos de eventos
        evento = data.get('evento', 'desconhecido')
        
        if evento == 'sms_enviado':
            logger.info("SMS enviado com sucesso")
        elif evento == 'sms_entregue':
            logger.info("SMS entregue ao destinatário")
        elif evento == 'sms_clicado':
            logger.info("Link no SMS foi clicado")
        elif evento == 'sms_erro':
            logger.error(f"Erro no envio do SMS: {data.get('erro', 'Erro desconhecido')}")
        
        return jsonify({'status': 'ok', 'mensagem': 'Webhook processado com sucesso'})
        
    except Exception as e:
        logger.error(f"Erro no endpoint webhook: {str(e)}")
        return jsonify({'erro': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    """
    Dashboard para visualizar estatísticas
    """
    try:
        conn = sqlite3.connect('kolmeya_webhook.db')
        cursor = conn.cursor()
        
        # Estatísticas gerais
        cursor.execute('SELECT COUNT(*) FROM clientes')
        total_clientes = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM cliques')
        total_cliques = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM webhooks')
        total_webhooks = cursor.fetchone()[0]
        
        # Últimos cliques
        cursor.execute('''
            SELECT nome, cpf, telefone, data_clique 
            FROM cliques 
            ORDER BY data_clique DESC 
            LIMIT 10
        ''')
        ultimos_cliques = cursor.fetchall()
        
        conn.close()
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard Kolmeya Webhook</title>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; }
                .card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .stats { display: flex; gap: 20px; margin-bottom: 20px; }
                .stat-card { flex: 1; text-align: center; padding: 20px; background: #007bff; color: white; border-radius: 8px; }
                .stat-number { font-size: 2em; font-weight: bold; }
                .stat-label { font-size: 0.9em; opacity: 0.9; }
                table { width: 100%; border-collapse: collapse; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background-color: #f8f9fa; font-weight: bold; }
                .btn { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Dashboard Kolmeya Webhook</h1>
                
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">{{ total_clientes }}</div>
                        <div class="stat-label">Total de Clientes</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{{ total_cliques }}</div>
                        <div class="stat-label">Total de Cliques</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{{ total_webhooks }}</div>
                        <div class="stat-label">Webhooks Recebidos</div>
                    </div>
                </div>
                
                <div class="card">
                    <h2>🔗 Testar Envio de SMS</h2>
                    <form action="/enviar-sms" method="post" style="display: flex; gap: 10px; flex-wrap: wrap;">
                        <input type="text" name="telefone" placeholder="Telefone (5511999999999)" required style="padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                        <input type="text" name="nome" placeholder="Nome" required style="padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                        <input type="text" name="cpf" placeholder="CPF" required style="padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                        <input type="text" name="mensagem" placeholder="Mensagem" required style="padding: 8px; border: 1px solid #ddd; border-radius: 4px; flex: 1;">
                        <button type="submit" class="btn">Enviar SMS</button>
                    </form>
                    <div style="margin-top: 15px; padding: 10px; background: #f8f9fa; border-radius: 4px;">
                        <strong>💡 Dica:</strong> Este formulário usa form data. Para usar JSON, envie uma requisição POST com Content-Type: application/json
                    </div>
                </div>
                
                <div class="card">
                    <h2>📈 Últimos Cliques</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Nome</th>
                                <th>CPF</th>
                                <th>Telefone</th>
                                <th>Data do Clique</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for clique in ultimos_cliques %}
                            <tr>
                                <td>{{ clique[0] }}</td>
                                <td>{{ clique[1] }}</td>
                                <td>{{ clique[2] }}</td>
                                <td>{{ clique[3] }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                
                <div class="card">
                    <h2>🔧 Endpoints Disponíveis</h2>
                    <p><strong>POST /enviar-sms</strong> - Enviar SMS com link rastreável</p>
                    <p><strong>GET /clique?id=...</strong> - Rastrear cliques</p>
                    <p><strong>POST /webhook-kolmeya</strong> - Receber webhooks do Kolmeya</p>
                    <p><strong>GET /dashboard</strong> - Dashboard de estatísticas</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return render_template_string(html_template, 
                                   total_clientes=total_clientes,
                                   total_cliques=total_cliques,
                                   total_webhooks=total_webhooks,
                                   ultimos_cliques=ultimos_cliques)
        
    except Exception as e:
        logger.error(f"Erro no dashboard: {str(e)}")
        return jsonify({'erro': str(e)}), 500

@app.route('/')
def home():
    """Página inicial"""
    return jsonify({
        'mensagem': 'Sistema de Webhook Kolmeya',
        'endpoints': {
            'POST /enviar-sms': 'Enviar SMS com link rastreável',
            'GET /clique?id=...': 'Rastrear cliques',
            'POST /webhook-kolmeya': 'Receber webhooks do Kolmeya',
            'GET /dashboard': 'Dashboard de estatísticas'
        }
    })

if __name__ == '__main__':
    # Inicializar banco de dados
    init_database()
    
    # Configurações do servidor
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Iniciando servidor na porta {port}")
    logger.info(f"Dashboard disponível em: http://localhost:{port}/dashboard")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
