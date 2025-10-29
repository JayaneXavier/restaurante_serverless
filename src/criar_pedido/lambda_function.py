# src/criar_pedido/lambda_function.py
import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:4566')
sqs = boto3.client('sqs', endpoint_url='http://localhost:4566')
table = dynamodb.Table('Pedidos')

def lambda_handler(event, context):
    try:
        # Validar corpo da requisição
        body = json.loads(event['body'])
        
        # Validar campos obrigatórios
        required_fields = ['cliente', 'itens', 'mesa']
        for field in required_fields:
            if field not in body:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': f'Campo {field} é obrigatório'})
                }
        
        # Criar pedido
        pedido_id = str(uuid.uuid4())
        pedido = {
            'id': pedido_id,
            'cliente': body['cliente'],
            'itens': body['itens'],
            'mesa': body['mesa'],
            'status': 'RECEBIDO',
            'data_criacao': datetime.now().isoformat()
        }
        
        # Salvar no DynamoDB
        table.put_item(Item=pedido)
        
        # Enviar para fila SQS
        sqs.send_message(
            QueueUrl='http://localhost:4566/000000000000/pedidos-queue',
            MessageBody=json.dumps({
                'pedido_id': pedido_id,
                'acao': 'PROCESSAR_PEDIDO'
            })
        )
        
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Pedido criado com sucesso',
                'pedido_id': pedido_id,
                'pedido': pedido
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }