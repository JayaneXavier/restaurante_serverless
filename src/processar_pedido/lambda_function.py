# src/processar_pedido/lambda_function.py
import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:4566')
s3 = boto3.client('s3', endpoint_url='http://localhost:4566')
sns = boto3.client('sns', endpoint_url='http://localhost:4566')
table = dynamodb.Table('Pedidos')

def gerar_comprovante_pdf(pedido):
    """Simula a geração de um comprovante em PDF"""
    comprovante = f"""
    COMPROVANTE DE PEDIDO
    =====================
    
    Pedido ID: {pedido['id']}
    Cliente: {pedido['cliente']}
    Mesa: {pedido['mesa']}
    Data: {pedido['data_criacao']}
    
    Itens:
    {chr(10).join(f'  - {item}' for item in pedido['itens'])}
    
    Status: {pedido['status']}
    
    Obrigado pela preferência!
    """
    
    return comprovante.encode('utf-8')

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            # Processar mensagem da fila
            message_body = json.loads(record['body'])
            pedido_id = message_body['pedido_id']
            
            # Buscar pedido no DynamoDB
            response = table.get_item(Key={'id': pedido_id})
            pedido = response.get('Item')
            
            if not pedido:
                print(f"Pedido {pedido_id} não encontrado")
                continue
            
            # Atualizar status do pedido
            table.update_item(
                Key={'id': pedido_id},
                UpdateExpression='SET #status = :status',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={':status': 'EM_PREPARO'}
            )
            
            # Gerar comprovante (simulado)
            comprovante = gerar_comprovante_pdf(pedido)
            
            # Salvar no S3
            s3_key = f"comprovantes/{pedido_id}.txt"
            s3.put_object(
                Bucket='comprovantes-pedidos',
                Key=s3_key,
                Body=comprovante,
                ContentType='text/plain'
            )
            
            # Enviar notificação via SNS
            sns.publish(
                TopicArn='arn:aws:sns:us-east-1:000000000000:PedidosConcluidos',
                Message=f'Novo pedido concluído: {pedido_id}',
                Subject='Pedido Pronto!'
            )
            
            print(f"Pedido {pedido_id} processado com sucesso")
            
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Pedidos processados'})
        }
        
    except Exception as e:
        print(f"Erro ao processar pedido: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }