# 1. Primeiro, vamos criar um README.md profissional
cat > README.md << 'EOF'
# 🍕 Sistema de Pedidos Restaurante - Serverless

Sistema completo de gerenciamento de pedidos para restaurantes usando arquitetura serverless com LocalStack.

## 🚀 Tecnologias Utilizadas

- **AWS Lambda** - Funções serverless
- **API Gateway** - Endpoint REST
- **DynamoDB** - Banco de dados NoSQL
- **SQS** - Filas de mensagens
- **S3** - Armazenamento de comprovantes
- **SNS** - Sistema de notificações
- **LocalStack** - Ambiente AWS local

## 📋 Funcionalidades

- ✅ **Criar pedidos** via API REST
- ✅ **Validar dados** do pedido
- ✅ **Armazenar** pedidos no DynamoDB
- ✅ **Processar pedidos** assincronamente via SQS
- ✅ **Gerar comprovantes** em PDF (simulado)
- ✅ **Salvar comprovantes** no S3
- ✅ **Enviar notificações** via SNS
- ✅ **Ambiente local** completo com LocalStack

## 🏗️ Arquitetura
