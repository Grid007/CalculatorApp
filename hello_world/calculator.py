import json

def lambda_handler(event, context):
    operation = event['pathParameters']['operation']
    a = int(event['pathParameters']['a'])
    b = int(event['pathParameters']['b'])

    if operation == 'add':
        result = add(a, b)
    elif operation == 'subtract':
        result = subtract(a, b)
    elif operation == 'multiply':
        result = multiply(a, b)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid operation'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'result': result})
    }

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b
