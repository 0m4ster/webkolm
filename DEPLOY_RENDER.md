# 🚀 Deploy no Render - Sistema Kolmeya Webhook

Este guia mostra como fazer o deploy do sistema no Render de forma simples e rápida.

## 📋 Pré-requisitos

1. **Conta no Render** (gratuita)
2. **Conta no GitHub** (para hospedar o código)
3. **Credenciais do Kolmeya** (API key)

## 🔧 Passo a Passo

### 1. Preparar o Código

1. **Faça upload dos arquivos para o GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Sistema de Webhook Kolmeya"
   git branch -M main
   git remote add origin https://github.com/seu-usuario/kolmeya-webhook.git
   git push -u origin main
   ```

2. **Verifique se todos os arquivos estão incluídos:**
   - ✅ `webkolm.py` (sistema principal)
   - ✅ `requirements.txt` (dependências)
   - ✅ `render.yaml` (configuração do Render)
   - ✅ `runtime.txt` (versão do Python)
   - ✅ `.gitignore` (arquivos ignorados)

### 2. Criar Conta no Render

1. Acesse [render.com](https://render.com)
2. Faça login com sua conta GitHub
3. Clique em "New +" → "Web Service"

### 3. Configurar o Deploy

1. **Conectar ao GitHub:**
   - Selecione o repositório `kolmeya-webhook`
   - Clique em "Connect"

2. **Configurações do Serviço:**
   - **Name:** `kolmeya-webhook`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python webkolm.py`
   - **Plan:** `Free`

3. **Variáveis de Ambiente:**
   Clique em "Environment" e adicione:
   ```
   KOLMEYA_API_KEY=sua_api_key_real_aqui
   KOLMEYA_API_URL=https://api.kolmeya.com.br
   WEBHOOK_BASE_URL=https://seu-app.onrender.com
   PORT=10000
   DEBUG=False
   ```

4. **Clicar em "Create Web Service"**

### 4. Configurar Webhook no Kolmeya

Após o deploy, configure no painel do Kolmeya:

- **URL do Webhook:** `https://seu-app.onrender.com/webhook-kolmeya`
- **Eventos:** Envio, entrega, clique, erro

## 🌐 URLs Importantes

Após o deploy, você terá acesso a:

- **Dashboard:** `https://seu-app.onrender.com/dashboard`
- **API:** `https://seu-app.onrender.com/`
- **Webhook:** `https://seu-app.onrender.com/webhook-kolmeya`

## 🔧 Configurações Avançadas

### Variáveis de Ambiente no Render

No painel do Render, vá em "Environment" e configure:

```env
# Obrigatórias
KOLMEYA_API_KEY=sua_api_key_real
WEBHOOK_BASE_URL=https://seu-app.onrender.com

# Opcionais
KOLMEYA_API_URL=https://api.kolmeya.com.br
PORT=10000
DEBUG=False
```

### Configurar Domínio Personalizado (Opcional)

1. No Render, vá em "Settings"
2. Clique em "Custom Domains"
3. Adicione seu domínio
4. Configure DNS conforme instruções

## 🧪 Testar o Deploy

### 1. Testar Dashboard
```bash
curl https://seu-app.onrender.com/dashboard
```

### 2. Testar API
```bash
curl https://seu-app.onrender.com/
```

### 3. Testar Envio de SMS
```bash
curl -X POST https://seu-app.onrender.com/enviar-sms \
  -H "Content-Type: application/json" \
  -d '{
    "telefone": "5511999999999",
    "nome": "Teste",
    "cpf": "123.456.789-00",
    "mensagem": "Teste de deploy:"
  }'
```

## 📊 Monitoramento

### Logs no Render
1. No painel do Render, clique no seu serviço
2. Vá na aba "Logs"
3. Monitore erros e performance

### Dashboard
- Acesse: `https://seu-app.onrender.com/dashboard`
- Veja estatísticas em tempo real
- Monitore cliques e webhooks

## 🔒 Segurança

### HTTPS Automático
- O Render fornece HTTPS automaticamente
- Certificados SSL gratuitos
- URLs seguras para webhooks

### Variáveis Sensíveis
- Nunca commite credenciais no GitHub
- Use variáveis de ambiente no Render
- Mantenha `.env` no `.gitignore`

## 🐛 Troubleshooting

### Erro de Build
```bash
# Verifique logs no Render
# Confirme se requirements.txt está correto
# Verifique se runtime.txt está correto
```

### Erro de Deploy
```bash
# Verifique variáveis de ambiente
# Confirme se PORT=10000
# Teste localmente primeiro
```

### Webhook não funciona
```bash
# Confirme URL no Kolmeya
# Teste endpoint manualmente
# Verifique logs no Render
```

## 💰 Custos

### Plano Gratuito
- ✅ 750 horas/mês
- ✅ 512MB RAM
- ✅ 0.1 CPU
- ✅ HTTPS incluído
- ✅ Deploy automático

### Plano Pago (se necessário)
- $7/mês para mais recursos
- Sem limites de horas
- Mais RAM e CPU

## 🔄 Atualizações

### Deploy Automático
- Push para `main` = deploy automático
- Sem configuração adicional
- Rollback fácil no painel

### Deploy Manual
```bash
# No Render, vá em "Manual Deploy"
# Selecione branch/commit
# Clique em "Deploy"
```

## 📞 Suporte

### Render
- [Documentação Render](https://render.com/docs)
- [Status do Serviço](https://status.render.com)

### Sistema
- Logs no painel do Render
- Dashboard em tempo real
- Testes via curl

## ✅ Checklist de Deploy

- [ ] Código no GitHub
- [ ] Conta no Render criada
- [ ] Serviço configurado
- [ ] Variáveis de ambiente definidas
- [ ] Deploy realizado com sucesso
- [ ] Dashboard acessível
- [ ] API funcionando
- [ ] Webhook configurado no Kolmeya
- [ ] Testes realizados

## 🎉 Próximos Passos

1. **Configure suas credenciais do Kolmeya**
2. **Teste o envio de SMS**
3. **Configure webhooks no painel do Kolmeya**
4. **Monitore via dashboard**
5. **Integre com seus sistemas**

O sistema estará 100% funcional no Render! 🚀 