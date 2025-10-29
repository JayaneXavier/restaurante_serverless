#!/bin/bash
# scripts/deploy.sh

echo "Fazendo deploy das Lambdas..."

# Criar arquivos ZIP das Lambdas
cd src/criar_pedido && zip -r ../../criar_pedido.zip . && cd ../..
cd src/processar_pedido && zip -r ../../processar_pedido.zip . && cd ../..

# Criar funções Lambda
awslocal lambda create-function \
    --function-name criar-pedido \
    --runtime python3.9 \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://criar_pedido.zip \
    --role arn:aws:iam::000000000000:role/lambda-role

awslocal lambda create-function \
    --function-name processar-pedido \
    --runtime python3.9 \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://processar_pedido.zip \
    --role arn:aws:iam::000000000000:role/lambda-role

# Criar API Gateway
awslocal apigateway create-rest-api --name "api-pedidos"

# Obter API ID
API_ID=$(awslocal apigateway get-rest-apis --query "items[?name=='api-pedidos'].id" --output text)

# Criar recurso e método
awslocal apigateway create-resource \
    --rest-api-id $API_ID \
    --parent-id $(awslocal apigateway get-resources --rest-api-id $API_ID --query "items[?path=='/'].id" --output text) \
    --path-part "pedidos"

RESOURCE_ID=$(awslocal apigateway get-resources --rest-api-id $API_ID --query "items[?path=='/pedidos'].id" --output text)

awslocal apigateway put-method \
    --rest-api-id $API_ID \
    --resource-id $RESOURCE_ID \
    --http-method POST \
    --authorization-type NONE

# Integração com Lambda
awslocal apigateway put-integration \
    --rest-api-id $API_ID \
    --resource-id $RESOURCE_ID \
    --http-method POST \
    --type AWS_PROXY \
    --integration-http-method POST \
    --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:000000000000:function:criar-pedido/invocations

# Configurar SQS como trigger da Lambda de processamento
awslocal lambda create-event-source-mapping \
    --function-name processar-pedido \
    --event-source-arn arn:aws:sqs:us-east-1:000000000000:pedidos-queue

echo "Deploy concluído!"