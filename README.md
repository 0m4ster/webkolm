# 🔗 Sistema de Webhook Kolmeya

Sistema completo para integração com a API do Kolmeya, incluindo envio de SMS, rastreamento de cliques e recebimento de webhooks.

## ✨ Funcionalidades

- ✅ **Envio de SMS** com link rastreável único
- ✅ **Rastreamento de cliques** com dados do cliente (nome, CPF, telefone)
- ✅ **Recebimento de webhooks** do Kolmeya
- ✅ **Dashboard** com estatísticas em tempo real
- ✅ **Banco de dados SQLite** para armazenamento local
- ✅ **API REST** completa

## 🚀 Instalação

### 1. Clone ou baixe os arquivos
```bash
cd kolm_webhook
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
Copie o arquivo `config.env.example` para `.env` e configure:

```bash
# Windows
copy config.env.example .env

# Linux/Mac
cp config.env.example .env
```

Edite o arquivo `.env` com suas configurações:
```env
KOLMEYA_API_KEY=sua_api_key_real_aqui
KOLMEYA_API_URL=https://api.kolmeya.com.br
WEBHOOK_BASE_URL=https://seudominio.com
PORT=5000
DEBUG=True
```

### 4. Execute o servidor
```bash
python webkolm.py
```

O servidor estará disponível em: `http://localhost:5000`

## 📊 Dashboard

Acesse o dashboard em: `http://localhost:5000/dashboard`

O dashboard inclui:
- Estatísticas gerais (clientes, cliques, webhooks)
- Formulário para testar envio de SMS
- Tabela com últimos cliques
- Lista de endpoints disponíveis

## 🔧 Endpoints da API

### 1. Enviar SMS
```http
POST /enviar-sms
Content-Type: application/json

{
  "telefone": "5511999999999",
  "nome": "João Silva",
  "cpf": "123.456.789-00",
  "mensagem": "Olá João, acesse sua oferta exclusiva!"
}
```

**Resposta:**
```json
{
  "status": "sucesso",
  "mensagem": "SMS enviado com sucesso",
  "link_id": "abc123-def456-ghi789",
  "link_rastreavel": "https://seudominio.com/clique?id=abc123-def456-ghi789",
  "resposta_kolmeya": {...}
}
```

### 2. Rastrear Clique
```http
GET /clique?id=abc123-def456-ghi789
```

**Ação:** Registra o clique e redireciona para a página de destino

### 3. Receber Webhook
```http
POST /webhook-kolmeya
Content-Type: application/json

{
  "evento": "sms_clicado",
  "telefone": "5511999999999",
  "link_id": "abc123-def456-ghi789"
}
```

### 4. Dashboard
```http
GET /dashboard
```

## 🔄 Fluxo Completo

1. **Envio de SMS:**
   - Cliente envia dados via `/enviar-sms`
   - Sistema gera link único e salva dados no banco
   - SMS é enviado via API Kolmeya com link rastreável

2. **Rastreamento de Clique:**
   - Cliente clica no link no SMS
   - Sistema registra clique com dados do cliente
   - Redireciona para página de destino

3. **Webhook do Kolmeya:**
   - Kolmeya envia webhook para `/webhook-kolmeya`
   - Sistema processa e armazena dados do evento

4. **Monitoramento:**
   - Dashboard mostra estatísticas em tempo real
   - Histórico de cliques e webhooks

## 📁 Estrutura do Projeto

```
kolm_webhook/
├── webkolm.py              # Sistema principal
├── requirements.txt         # Dependências Python
├── config.env.example      # Exemplo de configuração
├── README.md              # Este arquivo
└── kolmeya_webhook.db     # Banco de dados (criado automaticamente)
```

## 🗄️ Banco de Dados

O sistema usa SQLite com 3 tabelas:

### `clientes`
- Armazena dados dos clientes (telefone, nome, CPF)
- Cada cliente tem um `link_id` único

### `cliques`
- Registra cada clique com dados do cliente
- Inclui IP, User-Agent e timestamp

### `webhooks`
- Armazena todos os webhooks recebidos do Kolmeya
- Dados em formato JSON

## 🔒 Configuração de Produção

### 1. Servidor com URL Pública
Para receber webhooks do Kolmeya, você precisa de uma URL pública:
- Use serviços como Heroku, Railway, ou VPS
- Configure HTTPS (obrigatório para webhooks)
- Atualize `WEBHOOK_BASE_URL` no `.env`

### 2. Configuração do Kolmeya
No painel do Kolmeya, configure o webhook:
- **URL:** `https://seudominio.com/webhook-kolmeya`
- **Eventos:** Envio, entrega, clique, erro

### 3. Segurança
- Use HTTPS em produção
- Configure firewall adequado
- Monitore logs de acesso
- Use variáveis de ambiente para credenciais

## 🐛 Troubleshooting

### Erro ao enviar SMS
- Verifique se a API key do Kolmeya está correta
- Confirme se a URL da API está correta
- Verifique logs do servidor

### Webhook não recebido
- Confirme se a URL está acessível publicamente
- Verifique se o Kolmeya está configurado corretamente
- Teste com ferramentas como ngrok para desenvolvimento

### Banco de dados não criado
- Verifique permissões de escrita no diretório
- Execute o script manualmente para criar tabelas

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs do servidor
2. Confirme configurações no arquivo `.env`
3. Teste endpoints individualmente
4. Verifique documentação da API do Kolmeya

## 🔄 Próximas Melhorias

- [ ] Interface web mais elaborada
- [ ] Relatórios em PDF
- [ ] Integração com outros provedores SMS
- [ ] Sistema de notificações
- [ ] API para consulta de estatísticas
- [ ] Backup automático do banco
- [ ] Logs mais detalhados
- [ ] Rate limiting
- [ ] Autenticação de API 