# 🔗 Exemplos de Uso - API Kolmeya Webhook

Este arquivo contém exemplos práticos de como usar a API via curl.

## 📱 Enviar SMS

```bash
curl -X POST http://localhost:5000/enviar-sms \
  -H "Content-Type: application/json" \
  -d '{
    "telefone": "5511999999999",
    "nome": "João Silva",
    "cpf": "123.456.789-00",
    "mensagem": "Olá João! Acesse sua oferta exclusiva:"
  }'
```

**Resposta esperada:**
```json
{
  "status": "sucesso",
  "mensagem": "SMS enviado com sucesso",
  "link_id": "abc123-def456-ghi789",
  "link_rastreavel": "https://seudominio.com/clique?id=abc123-def456-ghi789",
  "resposta_kolmeya": {...}
}
```

## 🖱️ Simular Clique

```bash
curl -X GET "http://localhost:5000/clique?id=abc123-def456-ghi789"
```

**Resposta:** Redirecionamento HTTP 302

## 📡 Simular Webhook

```bash
curl -X POST http://localhost:5000/webhook-kolmeya \
  -H "Content-Type: application/json" \
  -d '{
    "evento": "sms_clicado",
    "telefone": "5511999999999",
    "link_id": "abc123-def456-ghi789",
    "timestamp": "2024-01-15T10:30:00Z",
    "dados_adicionais": {
      "plataforma": "whatsapp",
      "tipo_clique": "link"
    }
  }'
```

**Resposta esperada:**
```json
{
  "status": "ok",
  "mensagem": "Webhook processado com sucesso"
}
```

## 📊 Acessar Dashboard

```bash
curl -X GET http://localhost:5000/dashboard
```

**Resposta:** HTML do dashboard

## 🏠 Página Inicial

```bash
curl -X GET http://localhost:5000/
```

**Resposta esperada:**
```json
{
  "mensagem": "Sistema de Webhook Kolmeya",
  "endpoints": {
    "POST /enviar-sms": "Enviar SMS com link rastreável",
    "GET /clique?id=...": "Rastrear cliques",
    "POST /webhook-kolmeya": "Receber webhooks do Kolmeya",
    "GET /dashboard": "Dashboard de estatísticas"
  }
}
```

## 🔧 Exemplos com Dados Reais

### Enviar SMS para Maria
```bash
curl -X POST http://localhost:5000/enviar-sms \
  -H "Content-Type: application/json" \
  -d '{
    "telefone": "5511888888888",
    "nome": "Maria Santos",
    "cpf": "987.654.321-00",
    "mensagem": "Maria, sua fatura está disponível para consulta:"
  }'
```

### Enviar SMS para Pedro
```bash
curl -X POST http://localhost:5000/enviar-sms \
  -H "Content-Type: application/json" \
  -d '{
    "telefone": "5511777777777",
    "nome": "Pedro Oliveira",
    "cpf": "456.789.123-00",
    "mensagem": "Pedro, confira sua oferta especial:"
  }'
```

### Webhook de Entrega
```bash
curl -X POST http://localhost:5000/webhook-kolmeya \
  -H "Content-Type: application/json" \
  -d '{
    "evento": "sms_entregue",
    "telefone": "5511999999999",
    "link_id": "abc123-def456-ghi789",
    "timestamp": "2024-01-15T10:35:00Z"
  }'
```

### Webhook de Erro
```bash
curl -X POST http://localhost:5000/webhook-kolmeya \
  -H "Content-Type: application/json" \
  -d '{
    "evento": "sms_erro",
    "telefone": "5511999999999",
    "link_id": "abc123-def456-ghi789",
    "erro": "Número inválido",
    "timestamp": "2024-01-15T10:30:00Z"
  }'
```

## 🧪 Teste Completo

Execute este script para testar todo o fluxo:

```bash
# 1. Enviar SMS
RESPONSE=$(curl -s -X POST http://localhost:5000/enviar-sms \
  -H "Content-Type: application/json" \
  -d '{
    "telefone": "5511999999999",
    "nome": "Teste Usuario",
    "cpf": "111.222.333-44",
    "mensagem": "Teste de webhook:"
  }')

# 2. Extrair link_id
LINK_ID=$(echo $RESPONSE | grep -o '"link_id":"[^"]*"' | cut -d'"' -f4)

# 3. Simular clique
curl -X GET "http://localhost:5000/clique?id=$LINK_ID"

# 4. Simular webhook
curl -X POST http://localhost:5000/webhook-kolmeya \
  -H "Content-Type: application/json" \
  -d "{
    \"evento\": \"sms_clicado\",
    \"telefone\": \"5511999999999\",
    \"link_id\": \"$LINK_ID\",
    \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
  }"

echo "✅ Teste completo executado!"
```

## 📋 Dicas de Uso

1. **Substitua os telefones** pelos números reais dos seus clientes
2. **Use CPFs válidos** para testes mais realistas
3. **Personalize as mensagens** conforme sua necessidade
4. **Monitore os logs** do servidor para debug
5. **Acesse o dashboard** para ver as estatísticas em tempo real

## 🔍 Debug

Para ver detalhes das requisições, adicione `-v`:

```bash
curl -v -X POST http://localhost:5000/enviar-sms \
  -H "Content-Type: application/json" \
  -d '{"telefone": "5511999999999", "nome": "Teste", "cpf": "123.456.789-00", "mensagem": "Teste"}'
``` 