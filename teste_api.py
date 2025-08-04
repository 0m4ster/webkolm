#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para a API de Webhook Kolmeya
Demonstra como usar os endpoints principais
"""

import requests
import json
import time

# Configurações
BASE_URL = "http://localhost:5000"

def testar_envio_sms():
    """Testa o envio de SMS"""
    print("🔗 Testando envio de SMS...")
    
    dados = {
        "telefone": "5511999999999",
        "nome": "João Silva",
        "cpf": "123.456.789-00",
        "mensagem": "Olá João! Acesse sua oferta exclusiva:"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/enviar-sms",
            json=dados,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            resultado = response.json()
            print("✅ SMS enviado com sucesso!")
            print(f"📱 Link ID: {resultado.get('link_id')}")
            print(f"🔗 Link rastreável: {resultado.get('link_rastreavel')}")
            return resultado.get('link_id')
        else:
            print(f"❌ Erro ao enviar SMS: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Erro na requisição: {str(e)}")
        return None

def testar_clique(link_id):
    """Testa o rastreamento de clique"""
    if not link_id:
        print("❌ Link ID não fornecido")
        return
    
    print(f"\n🖱️ Testando clique no link: {link_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/clique?id={link_id}")
        
        if response.status_code == 302:  # Redirecionamento
            print("✅ Clique registrado com sucesso!")
            print(f"🔄 Redirecionado para: {response.headers.get('Location', 'N/A')}")
        else:
            print(f"❌ Erro ao registrar clique: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Erro na requisição: {str(e)}")

def testar_webhook():
    """Testa o recebimento de webhook"""
    print("\n📡 Testando recebimento de webhook...")
    
    dados_webhook = {
        "evento": "sms_clicado",
        "telefone": "5511999999999",
        "link_id": "teste-123",
        "timestamp": "2024-01-15T10:30:00Z",
        "dados_adicionais": {
            "plataforma": "whatsapp",
            "tipo_clique": "link"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/webhook-kolmeya",
            json=dados_webhook,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("✅ Webhook recebido com sucesso!")
            resultado = response.json()
            print(f"📊 Resposta: {resultado}")
        else:
            print(f"❌ Erro ao receber webhook: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Erro na requisição: {str(e)}")

def testar_dashboard():
    """Testa o acesso ao dashboard"""
    print("\n📊 Testando acesso ao dashboard...")
    
    try:
        response = requests.get(f"{BASE_URL}/dashboard")
        
        if response.status_code == 200:
            print("✅ Dashboard acessível!")
            print("🌐 Acesse: http://localhost:5000/dashboard")
        else:
            print(f"❌ Erro ao acessar dashboard: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {str(e)}")

def testar_endpoints():
    """Testa todos os endpoints disponíveis"""
    print("\n🔧 Testando endpoints disponíveis...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        
        if response.status_code == 200:
            dados = response.json()
            print("✅ Endpoints disponíveis:")
            for endpoint, descricao in dados.get('endpoints', {}).items():
                print(f"  - {endpoint}: {descricao}")
        else:
            print(f"❌ Erro ao listar endpoints: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {str(e)}")

def main():
    """Função principal de teste"""
    print("🚀 Iniciando testes da API Kolmeya Webhook")
    print("=" * 50)
    
    # Teste 1: Verificar se o servidor está rodando
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("❌ Servidor não está respondendo. Certifique-se de que está rodando em http://localhost:5000")
            return
    except:
        print("❌ Não foi possível conectar ao servidor. Certifique-se de que está rodando em http://localhost:5000")
        return
    
    print("✅ Servidor está rodando!")
    
    # Teste 2: Listar endpoints
    testar_endpoints()
    
    # Teste 3: Enviar SMS
    link_id = testar_envio_sms()
    
    # Teste 4: Simular clique (se o SMS foi enviado)
    if link_id:
        testar_clique(link_id)
    
    # Teste 5: Simular webhook
    testar_webhook()
    
    # Teste 6: Acessar dashboard
    testar_dashboard()
    
    print("\n" + "=" * 50)
    print("🎉 Testes concluídos!")
    print("\n📋 Próximos passos:")
    print("1. Configure suas credenciais do Kolmeya no arquivo .env")
    print("2. Acesse o dashboard em: http://localhost:5000/dashboard")
    print("3. Teste com dados reais de clientes")
    print("4. Configure webhooks no painel do Kolmeya")

if __name__ == "__main__":
    main() 