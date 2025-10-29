#!/bin/bash
# scripts/init-localstack.sh

echo "Inicializando recursos no LocalStack..."

# Criar tabela DynamoDB
awslocal dynamodb create-table \
    --table-name Pedidos \
    --attribute-definitions AttributeName=id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST

# Criar fila SQS
awslocal sqs create-queue \
    --queue-name pedidos-queue

# Criar bucket S3
awslocal s3 mb s3://comprovantes-pedidos

# Criar tópico SNS
awslocal sns create-topic \
    --name PedidosConcluidos

echo "Recursos criados com sucesso!"